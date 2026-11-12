# Submission checklist — Option 1

## Ready source artifacts

The submission files and real lab evidence below are prepared. Submission and the learner's personal Honor Code attestation are separate steps; no course grade is claimed.

| Task/activity | File or URL |
| --- | --- |
| 1 | https://github.com/HungManh642001/oaqjp-final-project-emb-ai/blob/feat/emotion-detector/README.md |
| 2a | `submission/2a_emotion_detection.py` — raw response.text version required by Task 2 |
| 3a | `EmotionDetection/emotion_detection.py` — formatted output |
| 4a | https://github.com/HungManh642001/oaqjp-final-project-emb-ai/blob/feat/emotion-detector/EmotionDetection/__init__.py |
| 5a | `test_emotion_detection.py` — five required live API cases |
| 6a | `server.py` |
| 7a | `EmotionDetection/emotion_detection.py` — HTTP 400 handling |
| 7b | `server.py` — invalid text handling |
| 8a | `server.py` |
| 8b | `evidence/local/8b_static_code_analysis.txt` — real local Pylint result |

## Verified live lab evidence

`bash lab_verify.sh` finished successfully **inside Skills Network Theia** on 2026-11-12. It used the real Watson endpoint, with no response mocking.

- `evidence/live/2b_application_creation.txt`
- `evidence/live/3b_formatted_output_test.txt`
- `evidence/live/4b_packaging_test.txt`
- `evidence/live/5b_unit_testing_result.txt` — all five live cases passed
- `evidence/live/7_blank_input_api.txt` — verifies the API's actual HTTP 400 behavior
- `evidence/live/8b_static_code_analysis.txt`

The application was started with `python3 server.py`, launched on port 5000 through the Skills Network proxy, and checked through the provided frontend. Actual browser screenshots:

- `evidence/live/6b_deployment_test.png`: input `I think I am having fun` with dominant emotion `joy` (joy score `0.876574`).
- `evidence/live/7c_error_handling_interface.png`: blank input and `Invalid text! Please try again!`.

## Verification limits

Local fixture tests are in `evidence/local/contract_tests.txt`; they are **not** replacements for the live Task 2–5 outputs. Use `evidence/live/` for the actual course lab results. The live service is only reachable from the Skills Network lab. Passing these checks does not establish a Coursera grade or course completion state.

The code was prepared with AI assistance. Do not attest otherwise. The course submission page's personal Honor Code acknowledgement has not been selected by the assistant.
