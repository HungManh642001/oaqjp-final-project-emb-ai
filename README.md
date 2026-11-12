# Final project

Emotion detection web application for IBM's **Build & Deploy AI Applications with Python & Flask** course.

## Application

- `EmotionDetection/emotion_detection.py` calls the Skills Network Watson EmotionPredict API and returns the five emotion scores plus `dominant_emotion`.
- `EmotionDetection/__init__.py` exports `emotion_detector`.
- `server.py` serves the provided IBM frontend on port 5000 and handles blank input and upstream failures.
- `test_contracts.py` tests HTTP parsing and Flask behavior using fixtures at the external API boundary.
- `test_emotion_detection.py` contains the five exact statements required by the assignment and calls the real API when enabled.

## Run in Skills Network Labs

The Watson endpoint is intended for the course's Theia environment. A passing fixture suite outside the lab does **not** prove the live Watson predictions.

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -v
bash lab_verify.sh
python3 server.py
```

`lab_verify.sh` enables `RUN_WATSON_INTEGRATION=1`, calls the actual Watson service and saves real terminal results in `evidence/live/`. It stops on failure. Open port **5000** using the Skills Network application launcher.

Test the interface with **I think I am having fun** and save `6b_deployment_test.png`. Clear the input, submit again and save `7c_error_handling_interface.png`.

## Local checks

```bash
python3 -m unittest discover -v
python3 -m ruff check .
python3 -m pylint server.py
```

Without `RUN_WATSON_INTEGRATION=1`, five live Watson tests are explicitly **skipped**. The remaining tests use sample API responses, not live predictions. `evidence/local/` contains actual local test and Pylint output.

## Verified in the course lab

On 2026-11-12, `bash lab_verify.sh` completed successfully inside Skills Network Theia:

- All five required **real Watson** tests passed.
- The joy and anger packaging examples returned their expected dominant emotions.
- Blank text returned six `None` values.
- Pylint rated `server.py` **10.00/10**.
- The deployed interface returned **joy** for `I think I am having fun`, and displayed the required error for an empty input.

Actual terminal outputs and both required screenshots are saved in [`evidence/live/`](evidence/live/). These results describe the lab run, not a Coursera grade.

## Submission

See [submission/CHECKLIST.md](submission/CHECKLIST.md) for the required source files, URLs, logs and screenshots. Review the course's AI-use rules before submitting; the learner must personally decide whether they can make the Honor Code attestation.
