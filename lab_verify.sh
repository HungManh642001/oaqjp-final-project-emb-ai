#!/usr/bin/env bash
# Chạy trong terminal Skills Network, không dùng phản hồi giả lập.
set -euo pipefail
cd -- "$(dirname -- "$0")"
mkdir -p evidence/live

python3 - <<'PY' | tee evidence/live/2b_application_creation.txt
import runpy

module = runpy.run_path("submission/2a_emotion_detection.py")
print('Task 2: raw Watson response for "I love this new technology."')
print(module["emotion_detector"]("I love this new technology."))
PY

python3 - <<'PY' | tee evidence/live/3b_formatted_output_test.txt
from EmotionDetection import emotion_detector

result = emotion_detector("I am so happy I am doing this")
print(result)
assert result["dominant_emotion"] == "joy", result
PY

python3 - <<'PY' | tee evidence/live/4b_packaging_test.txt
from EmotionDetection import emotion_detector

result = emotion_detector("I hate working long hours")
print(result)
assert result["dominant_emotion"] == "anger", result
PY

RUN_WATSON_INTEGRATION=1 python3 -m unittest test_emotion_detection -v \
    2>&1 | tee evidence/live/5b_unit_testing_result.txt

python3 - <<'PY' | tee evidence/live/7_blank_input_api.txt
from EmotionDetection import emotion_detector

result = emotion_detector("")
print(result)
assert result == dict.fromkeys(
    ("anger", "disgust", "fear", "joy", "sadness", "dominant_emotion")
), result
PY

python3 -m pylint server.py | tee evidence/live/8b_static_code_analysis.txt
printf '\nLive checks passed. Run python3 server.py, then capture 6b and 7c in the browser.\n'
