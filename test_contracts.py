"""Kiểm tra hợp đồng API bằng phản hồi mẫu, không gọi Watson thật."""

import unittest
from unittest.mock import Mock, patch

import requests

from EmotionDetection import emotion_detector
from server import app


class TestWatsonContract(unittest.TestCase):
    """Kiểm tra việc trích xuất điểm và xử lý lỗi HTTP của Watson."""

    def test_scores_and_dominant_emotion(self) -> None:
        """Đọc điểm từ phản hồi Watson và chọn cảm xúc có điểm cao nhất."""
        response = Mock(status_code=200)
        response.json.return_value = {
            "emotionPredictions": [
                {
                    "emotion": {
                        "anger": 0.05,
                        "disgust": 0.02,
                        "fear": 0.08,
                        "joy": 0.9,
                        "sadness": 0.1,
                    }
                }
            ],
        }
        with patch("requests.post", return_value=response) as post:
            result = emotion_detector("I love this new technology.")
        self.assertEqual(
            result,
            {
                "anger": 0.05,
                "disgust": 0.02,
                "fear": 0.08,
                "joy": 0.9,
                "sadness": 0.1,
                "dominant_emotion": "joy",
            },
        )
        self.assertEqual(
            post.call_args.kwargs["json"],
            {
                "raw_document": {"text": "I love this new technology."},
            },
        )
        self.assertEqual(
            post.call_args.kwargs["headers"],
            {
                "grpc-metadata-mm-model-id": (
                    "emotion_aggregated-workflow_lang_en_stock"
                ),
            },
        )
        self.assertGreater(post.call_args.kwargs["timeout"], 0)

    def test_bad_request_returns_none_before_json_decode(self) -> None:
        """HTTP 400 có thể không chứa JSON nhưng vẫn trả đủ khóa với None."""
        response = Mock(status_code=400)
        response.json.side_effect = ValueError("not JSON")
        with patch("requests.post", return_value=response):
            result = emotion_detector("")
        self.assertEqual(
            result,
            {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None,
            },
        )

    def test_upstream_http_failure_is_not_a_valid_emotion(self) -> None:
        """HTTP 503 không được diễn giải thành kết quả hợp lệ."""
        response = Mock(status_code=503)
        response.raise_for_status.side_effect = requests.HTTPError("unavailable")
        with (
            patch("requests.post", return_value=response),
            self.assertRaises(requests.HTTPError),
        ):
            emotion_detector("hello")

    def test_malformed_payload_reports_value_error(self) -> None:
        """Phản hồi thiếu emotionPredictions gây lỗi dữ liệu có kiểm soát."""
        response = Mock(status_code=200)
        response.json.return_value = {}
        with (
            patch("requests.post", return_value=response),
            self.assertRaises(ValueError),
        ):
            emotion_detector("hello")

    def test_invalid_scores_are_not_valid_predictions(self) -> None:
        """Điểm không phải số hữu hạn trong khoảng 0..1 phải bị từ chối."""
        for value in ("<script>bad</script>", None, True, float("nan"), 1.5, -0.1):
            with self.subTest(value=value):
                response = Mock(status_code=200)
                response.json.return_value = {
                    "emotionPredictions": [
                        {
                            "emotion": {
                                "anger": value,
                                "disgust": 0.1,
                                "fear": 0.1,
                                "joy": 0.8,
                                "sadness": 0.1,
                            }
                        }
                    ]
                }
                with (
                    patch("requests.post", return_value=response),
                    self.assertRaises(ValueError),
                ):
                    emotion_detector("hello")


class TestWebContract(unittest.TestCase):
    """Kiểm tra các phản hồi thực của Flask qua test client."""

    def setUp(self) -> None:
        """Khởi tạo client và bật chế độ kiểm thử."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home_serves_provided_frontend(self) -> None:
        """Trang chủ phải chứa ô nhập của giao diện IBM."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id="textToAnalyze"', response.data)
        with self.client.get("/static/mywebscript.js") as static_response:
            self.assertEqual(static_response.status_code, 200)

    def test_prediction_matches_required_display(self) -> None:
        """Route phải đọc textToAnalyze và hiển thị đủ năm điểm cảm xúc."""
        result = {
            "anger": 0.05,
            "disgust": 0.02,
            "fear": 0.08,
            "joy": 0.9,
            "sadness": 0.1,
            "dominant_emotion": "joy",
        }
        with patch("server.emotion_detector", return_value=result) as detector:
            response = self.client.get(
                "/emotionDetector",
                query_string={
                    "textToAnalyze": "I think I am having fun",
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True),
            "For the given statement, the system response is "
            "'anger': 0.05, 'disgust': 0.02, 'fear': 0.08, "
            "'joy': 0.9 and 'sadness': 0.1. "
            "The dominant emotion is <strong>joy</strong>.",
        )
        detector.assert_called_once_with("I think I am having fun")

    def test_missing_or_whitespace_input_displays_invalid_message(self) -> None:
        """Giá trị thiếu, rỗng và chỉ có khoảng trắng đều bị từ chối."""
        for query in ({}, {"textToAnalyze": ""}, {"textToAnalyze": " \t "}):
            with self.subTest(query=query):
                response = self.client.get("/emotionDetector", query_string=query)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    response.get_data(as_text=True), "Invalid text! Please try again!"
                )

    def test_null_dominant_emotion_displays_invalid_message(self) -> None:
        """Kết quả None của Watson được đổi thành thông báo theo đề."""
        with patch("server.emotion_detector", return_value={"dominant_emotion": None}):
            response = self.client.get("/emotionDetector?textToAnalyze=invalid")
        self.assertEqual(
            response.get_data(as_text=True), "Invalid text! Please try again!"
        )

    def test_network_failure_returns_retryable_error(self) -> None:
        """Lỗi mạng không được trả dưới dạng kết quả cảm xúc giả."""
        with (
            patch("server.emotion_detector", side_effect=requests.Timeout),
            self.assertLogs("server", level="ERROR"),
        ):
            response = self.client.get("/emotionDetector?textToAnalyze=hello")
        self.assertEqual(response.status_code, 503)
        self.assertIn("temporarily unavailable", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
