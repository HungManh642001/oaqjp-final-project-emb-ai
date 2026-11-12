"""Phục vụ giao diện nhận diện cảm xúc bằng Flask."""

import logging

from flask import Flask, render_template, request
from requests import RequestException

from EmotionDetection import emotion_detector

app = Flask(__name__)
LOGGER = logging.getLogger(__name__)


@app.route("/")
def index() -> str:
    """Trả về giao diện HTML có sẵn của IBM."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route() -> str | tuple[str, int]:
    """Phân tích văn bản từ giao diện và hiển thị kết quả theo định dạng đề bài."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return "Invalid text! Please try again!"
    try:
        result = emotion_detector(text_to_analyze)
    except (RequestException, ValueError):
        LOGGER.exception("Không thể phân tích cảm xúc qua Watson")
        return "Emotion service temporarily unavailable. Please try again!", 503
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!"
    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} "
        f"and 'sadness': {result['sadness']}. "
        f"The dominant emotion is <strong>{result['dominant_emotion']}</strong>."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
