Live Working Link - [https://huggingface.co/spaces/tarun2525tej/clinical-extraction-demo]

# HealosBench

Minimal Streamlit app for extracting structured clinical JSON from a clinical transcript with a local Hugging Face model.

## Fields

- `chief_complaint`
- `vitals`: `bp`, `hr`, `temp_f`, `spo2`
- `medications`: `name`, `dose`, `frequency`, `route`
- `diagnoses`: `description`, optional `icd10`
- `plan`: array of strings
- `follow_up`: `interval_days`, `reason`

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Hugging Face Spaces

Create a new Streamlit Space and upload these files. The app uses `google/flan-t5-small` through `transformers`, so no API key is required.

## Notes

This is a minimal demo and is not intended for clinical decision-making.
