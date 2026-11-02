from typing import List, Optional

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from age_warnings import check_age_warnings
from interactions import check_interactions
from ocr import extract_text_from_image
from parser import parse_prescription, summarize_drug
from rxnorm_api import get_rxcui

app = FastAPI(
    title="Prescription Summarizer & Interaction Checker API",
    description="Backend for parsing prescriptions and flagging interaction/age risks.",
    version="1.0.0",
)

# Allow the Next.js dev server (and any deployed frontend URL you add later)
# to call this API from the browser. Add your production frontend URL here
# once you deploy it.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Response schemas -- these just describe the shape of what the existing
# modules already return, so FastAPI can validate + document it.
# ---------------------------------------------------------------------------
class DrugResult(BaseModel):
    drug_name: Optional[str] = None
    dose: Optional[str] = None
    frequency: Optional[str] = None
    route: Optional[str] = None
    duration: Optional[str] = None
    summary: str
    rxcui: Optional[str] = None  # None if RxNorm didn't recognize the drug


class InteractionResult(BaseModel):
    drug_1: str
    drug_2: str
    severity: str
    explanation: str


class AgeWarningResult(BaseModel):
    drug_name: str
    condition: str
    age_threshold: int
    message: str


class AnalyzeResponse(BaseModel):
    raw_text: str
    drugs: List[DrugResult]
    interactions: List[InteractionResult]
    age_warnings: List[AgeWarningResult]


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    text: str = Form(default=""),
    age: int = Form(...),
    image: Optional[UploadFile] = File(default=None),
):
    # 1. Get raw text -- OCR the image if one was uploaded, else use pasted text.
    if image is not None:
        raw_text = extract_text_from_image(image.file)
    else:
        raw_text = text

    # 2. Parse into structured drug data.
    parsed_drugs = parse_prescription(raw_text) if raw_text.strip() else []

    # 3. Attach a plain-English summary + RxNorm lookup to each drug.
    #    get_rxcui() already fails gracefully (returns None) if the API
    #    is unreachable or the drug isn't recognized, so this never
    #    breaks the response even if RxNorm is down.
    drugs_out = []
    for drug in parsed_drugs:
        drugs_out.append(
            {
                **drug,
                "summary": summarize_drug(drug),
                "rxcui": get_rxcui(drug["drug_name"]) if drug.get("drug_name") else None,
            }
        )

    # 4. Run interaction + age checks on the extracted drug names.
    drug_names = [d["drug_name"] for d in parsed_drugs if d.get("drug_name")]
    interaction_results = check_interactions(drug_names)
    age_results = check_age_warnings(drug_names, age)

    return {
        "raw_text": raw_text,
        "drugs": drugs_out,
        "interactions": interaction_results,
        "age_warnings": age_results,
    }


@app.get("/rxcui")
def rxcui_lookup(name: str):
    return {"name": name, "rxcui": get_rxcui(name)}
