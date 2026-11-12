"""Phiên bản Task 2 trả nguyên văn phản hồi Watson theo yêu cầu của đề."""

import requests


def emotion_detector(text_to_analyze: str) -> str:
    """Gửi văn bản và trả response.text trước bước định dạng Task 3."""
    response = requests.post(
        "https://sn-watson-emotion.labs.skills.network/v1/"
        "watson.runtime.nlp.v1/NlpService/EmotionPredict",
        json={"raw_document": {"text": text_to_analyze}},
        headers={
            "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.text
