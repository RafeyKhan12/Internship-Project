import streamlit as st

# Import logic from the other modules -- no logic is reimplemented here.
from ocr import extract_text_from_image
from parser import parse_prescription, summarize_drug
from interactions import check_interactions
from age_warnings import check_age_warnings

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Prescription Summarizer & Interaction Checker",
    page_icon="💊",
    layout="wide",
)

st.title("💊 Prescription Text Summarizer & Drug Interaction Alert System")
st.caption(
    "Paste prescription text or upload a prescription image to get a "
    "plain-English summary, drug interaction warnings, and age-related warnings."
)

# ---------------------------------------------------------------------------
# Session state -- lets results persist across reruns (e.g. when the user
# adjusts the age input) without needing to re-click "Analyze" every time.
# ---------------------------------------------------------------------------
if "parsed_drugs" not in st.session_state:
    st.session_state.parsed_drugs = []
if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""
if "used_ocr" not in st.session_state:
    st.session_state.used_ocr = False

# ---------------------------------------------------------------------------
# 1 & 2. Input: text area for pasted text, file uploader for images
# ---------------------------------------------------------------------------
st.header("1. Enter a Prescription")

input_col, upload_col = st.columns(2)

with input_col:
    pasted_text = st.text_area(
        "Paste prescription text here",
        height=180,
        placeholder="e.g. Metformin 500mg PO BID x30d\nLisinopril 10mg PO QD x90d",
    )

with upload_col:
    uploaded_image = st.file_uploader(
        "...or upload a prescription image",
        type=["jpg", "jpeg", "png"],
    )
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded prescription image", width=300)

# ---------------------------------------------------------------------------
# 6. Age input (adults only -- pediatric dosing is out of scope)
# ---------------------------------------------------------------------------
st.header("2. Patient Age")
age = st.number_input(
    "Patient age (years)",
    min_value=18,
    max_value=120,
    value=40,
    step=1,
    help="This tool covers adults only. Pediatric dosing is out of scope.",
)

# ---------------------------------------------------------------------------
# Analyze button -- runs OCR (if needed) and parsing, and stores the
# result in session_state so it persists across later reruns.
# ---------------------------------------------------------------------------
analyze_clicked = st.button("🔍 Analyze Prescription", type="primary")

if analyze_clicked:
    # 2. If an image was uploaded, OCR it; otherwise use the pasted text.
    if uploaded_image is not None:
        with st.spinner("Running OCR on the uploaded image..."):
            raw_text = extract_text_from_image(uploaded_image)
        st.session_state.used_ocr = True

        if not raw_text:
            st.warning(
                "OCR couldn't extract any text from that image. "
                "Try a clearer image, or paste the prescription text instead."
            )
    else:
        raw_text = pasted_text
        st.session_state.used_ocr = False

    st.session_state.raw_text = raw_text

    # 3. Parse the text into structured drug data.
    if raw_text and raw_text.strip():
        st.session_state.parsed_drugs = parse_prescription(raw_text)
    else:
        st.session_state.parsed_drugs = []
        st.warning("Please paste some prescription text or upload an image first.")

    if raw_text and raw_text.strip() and not st.session_state.parsed_drugs:
        st.warning(
            "Couldn't detect any drugs in that text. Try a different format, "
            "e.g. 'Metformin 500mg PO BID x30d'."
        )

# ---------------------------------------------------------------------------
# Results section -- only shown once we have parsed drugs. Interaction and
# age-warning checks are recomputed live on every rerun (they're cheap
# local lookups), so adjusting the age slider updates warnings instantly
# without needing to re-click Analyze.
# ---------------------------------------------------------------------------
parsed_drugs = st.session_state.parsed_drugs

if parsed_drugs:
    # If OCR was used, show what was extracted for transparency/debugging.
    if st.session_state.used_ocr:
        with st.expander("📄 View OCR-extracted text"):
            st.text(st.session_state.raw_text)

    # -----------------------------------------------------------------
    # 4. Plain-English summary for each drug
    # -----------------------------------------------------------------
    st.header("3. Prescription Summary")
    for drug in parsed_drugs:
        st.markdown(f"- {summarize_drug(drug)}")

    with st.expander("🔧 View raw parsed data"):
        st.json(parsed_drugs)

    # Build a flat list of drug names to feed into the checkers below.
    drug_names = [d["drug_name"] for d in parsed_drugs if d.get("drug_name")]

    # -----------------------------------------------------------------
    # 7. Drug interaction warnings, color-coded by severity
    # -----------------------------------------------------------------
    st.header("4. Drug Interaction Warnings")
    interaction_results = check_interactions(drug_names)

    if not interaction_results:
        st.success("✅ No known interactions found among the entered drugs.")
    else:
        for match in interaction_results:
            drug_1 = match["drug_1"].title()
            drug_2 = match["drug_2"].title()
            severity = match["severity"]
            explanation = match["explanation"]

            message = f"**{severity.upper()}**: {drug_1} + {drug_2} — {explanation}"

            if severity == "major":
                st.error(f"🔴 {message}")
            elif severity == "moderate":
                st.warning(f"🟡 {message}")
            else:  # minor (or any other severity not explicitly color-coded)
                st.info(f"ℹ️ {message}")

    # -----------------------------------------------------------------
    # 7. Age-based warnings
    # -----------------------------------------------------------------
    st.header("5. Age-Related Warnings")
    age_results = check_age_warnings(drug_names, age)

    if not age_results:
        st.success(f"✅ No age-related warnings for a patient age {age}.")
    else:
        for warning in age_results:
            drug_label = warning["drug_name"].title()
            st.warning(f"🟡 **{drug_label}** (age {age}): {warning['message']}")

else:
    st.info("👆 Enter prescription text or upload an image, then click **Analyze Prescription**.")

# ---------------------------------------------------------------------------
# 8. Disclaimer -- always shown at the bottom of the page.
# ---------------------------------------------------------------------------
st.divider()
st.caption(
    "⚠️ For educational/demonstration purposes only. "
    "Not a substitute for professional medical advice."
)
