import json

import streamlit as st

import model
import schema


TRANSCRIPT_CHAR_LIMIT = 1500


st.set_page_config(page_title="Clinical Extraction Demo", layout="centered")

st.title("Clinical Extraction Demo")
st.info("First run may take ~10–20 seconds while model loads.")


@st.cache_resource(show_spinner=False)
def _preload_model():
    model.extract("test")
    return True


_preload_model()


def _is_empty_output(result: dict) -> bool:
    return result == schema.empty_clinical_note()


transcript = st.text_area(
    "Paste clinical transcript",
    height=260,
    placeholder=(
        "Patient reports cough and fever for three days. BP 120/80, HR 88, "
        "temperature 100.4 F, SpO2 98%. Taking acetaminophen 500 mg by mouth "
        "as needed. Diagnosis: viral URI. Plan: fluids and rest. Follow up in 7 days."
    ),
)
input_too_long = len(transcript) > TRANSCRIPT_CHAR_LIMIT

if input_too_long:
    st.warning("Input too long, please shorten")

if st.button("Extract", type="primary", disabled=input_too_long):
    if not transcript.strip():
        st.warning("Please paste a clinical transcript before extracting.")
    else:
        try:
            with st.spinner("Extracting..."):
                raw_output = model.extract(transcript)
                result = schema.validate_output(raw_output)

            if _is_empty_output(result):
                st.warning("Model could not extract structured data")
            else:
                st.success("Structured data extracted")

            st.subheader("Formatted JSON")
            st.json(result)

            st.subheader("Chief Complaint")
            st.write(result["chief_complaint"] or "Not found")

            st.subheader("Vitals")
            st.json(result["vitals"])

            st.subheader("Medications")
            if result["medications"]:
                st.dataframe(result["medications"], use_container_width=True)
            else:
                st.write("None found")

            st.subheader("Diagnoses")
            if result["diagnoses"]:
                st.dataframe(result["diagnoses"], use_container_width=True)
            else:
                st.write("None found")

            st.subheader("Plan")
            if result["plan"]:
                for item in result["plan"]:
                    st.write(f"- {item}")
            else:
                st.write("None found")

            st.subheader("Follow Up")
            st.json(result["follow_up"])

            with st.expander("Raw JSON"):
                st.code(json.dumps(result, indent=2), language="json")

        except Exception as exc:
            st.error(f"Model extraction failed: {exc}")
