// lib/api.ts
// Typed client for the FastAPI backend (see ../prescription_summarizer/api.py).
// Every field here mirrors the Pydantic response models on the backend.

export interface DrugResult {
  drug_name: string | null;
  dose: string | null;
  frequency: string | null;
  route: string | null;
  duration: string | null;
  summary: string;
  rxcui: string | null;
}

export type Severity = "major" | "moderate" | "minor" | string;

export interface InteractionResult {
  drug_1: string;
  drug_2: string;
  severity: Severity;
  explanation: string;
}

export interface AgeWarningResult {
  drug_name: string;
  condition: "under" | "over";
  age_threshold: number;
  message: string;
}

export interface AnalyzeResponse {
  raw_text: string;
  drugs: DrugResult[];
  interactions: InteractionResult[];
  age_warnings: AgeWarningResult[];
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function analyzePrescription(params: {
  text: string;
  age: number;
  image?: File | null;
}): Promise<AnalyzeResponse> {
  const formData = new FormData();
  formData.append("text", params.text);
  formData.append("age", String(params.age));
  if (params.image) {
    formData.append("image", params.image);
  }

  const res = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new Error(`Analysis failed (${res.status}): ${detail || res.statusText}`);
  }

  return res.json();
}
