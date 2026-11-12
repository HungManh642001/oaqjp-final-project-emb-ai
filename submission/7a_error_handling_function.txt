"""Giao tiếp với dịch vụ nhận diện cảm xúc Watson của lab IBM."""

import os

import requests

WATSON_URL = os.environ.get(
    "WATSON_EMOTION_URL",
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict",
)
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze: str) -> dict[str, float | str | None]:
    """Gửi văn bản tới Watson và trả năm điểm cùng cảm xúc chủ đạo.

    Args:
        text_to_analyze: Văn bản tiếng Anh cần phân tích.

    Returns:
        Điểm cảm xúc và dominant_emotion; toàn bộ giá trị là None nếu HTTP 400.

    Raises:
        requests.RequestException: Dịch vụ không truy cập được hoặc báo lỗi HTTP.
        ValueError: Dữ liệu phản hồi không có cấu trúc cảm xúc mong đợi.
    """
    response = requests.post(
        WATSON_URL,
        json={"raw_document": {"text": text_to_analyze}},
        headers={
            "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        },
        timeout=30,
    )
    if response.status_code == 400:
        return dict.fromkeys((*EMOTIONS, "dominant_emotion"))
    response.raise_for_status()
    try:
        emotion = response.json()["emotionPredictions"][0]["emotion"]
        scores = {name: emotion[name] for name in EMOTIONS}
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("Invalid Watson emotion response") from exc
    if any(
        isinstance(score, bool)
        or not isinstance(score, (int, float))
        or not 0 <= score <= 1
        for score in scores.values()
    ):
        raise ValueError("Invalid Watson emotion scores")
    return {**scores, "dominant_emotion": max(scores, key=scores.get)}
