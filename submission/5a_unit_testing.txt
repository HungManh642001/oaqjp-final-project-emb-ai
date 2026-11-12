"""Năm ca kiểm thử theo đề IBM, bắt buộc dùng dịch vụ Watson thật trong lab."""

import os
import unittest

from EmotionDetection import emotion_detector


@unittest.skipUnless(
    os.environ.get("RUN_WATSON_INTEGRATION") == "1",
    "Requires the real Watson API in Skills Network; set RUN_WATSON_INTEGRATION=1",
)
class TestEmotionDetection(unittest.TestCase):
    """Kiểm tra cảm xúc chủ đạo của năm câu do đề bài quy định."""

    def test_joy(self) -> None:
        """Câu diễn đạt sự vui mừng phải có cảm xúc chủ đạo joy."""
        self.assertEqual(
            emotion_detector("I am glad this happened")["dominant_emotion"], "joy"
        )

    def test_anger(self) -> None:
        """Câu diễn đạt tức giận phải có cảm xúc chủ đạo anger."""
        self.assertEqual(
            emotion_detector("I am really mad about this")["dominant_emotion"], "anger"
        )

    def test_disgust(self) -> None:
        """Câu diễn đạt ghê tởm phải có cảm xúc chủ đạo disgust."""
        self.assertEqual(
            emotion_detector("I feel disgusted just hearing about this")[
                "dominant_emotion"
            ],
            "disgust",
        )

    def test_sadness(self) -> None:
        """Câu diễn đạt buồn bã phải có cảm xúc chủ đạo sadness."""
        self.assertEqual(
            emotion_detector("I am so sad about this")["dominant_emotion"], "sadness"
        )

    def test_fear(self) -> None:
        """Câu diễn đạt sợ hãi phải có cảm xúc chủ đạo fear."""
        self.assertEqual(
            emotion_detector("I am really afraid that this will happen")[
                "dominant_emotion"
            ],
            "fear",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
