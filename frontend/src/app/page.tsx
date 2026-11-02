"use client";

import { useState } from "react";
import PrescriptionForm from "@/components/PrescriptionForm";
import DrugSummaryList from "@/components/DrugSummaryList";
import InteractionWarnings from "@/components/InteractionWarnings";
import AgeWarnings from "@/components/AgeWarnings";
import Disclaimer from "@/components/Disclaimer";
import { analyzePrescription, AnalyzeResponse } from "@/lib/api";

export default function Home() {
  const [text, setText] = useState("");
  const [image, setImage] = useState<File | null>(null);
  const [age, setAge] = useState(40);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyzePrescription({ text, age, image });
      setResult(data);
      if (data.drugs.length === 0) {
        setError("Couldn't detect any drugs in that input. Try a different format or a clearer image.");
      }
    } catch (err) {
      setResult(null);
      setError(err instanceof Error ? err.message : "Something went wrong. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto max-w-3xl px-6 py-16 md:py-24">
      {/* Hero */}
      <section className="mb-14">
        <span className="font-mono text-xs uppercase tracking-widest text-accent">
          Prescription Reader
        </span>
        <h1 className="mt-3 text-balance text-4xl font-semibold leading-[1.1] text-ink md:text-5xl">
          Decode the script.
          <br />
          Catch the risk.
        </h1>
        <p className="mt-4 max-w-xl text-balance text-base leading-relaxed text-muted">
          Paste prescription text or upload a label photo. We&apos;ll translate the
          shorthand into plain English and flag anything worth a second look.
        </p>
      </section>

      {/* Input form */}
      <section className="rounded-lg border border-border bg-surface2/40 p-6 md:p-8">
        <PrescriptionForm
          text={text}
          onTextChange={setText}
          image={image}
          onImageChange={setImage}
          age={age}
          onAgeChange={setAge}
          onSubmit={handleSubmit}
          loading={loading}
        />
      </section>

      {/* Error state */}
      {error && (
        <div className="mt-6 rounded-md border-l-2 border-l-major bg-surface px-4 py-3">
          <p className="text-sm text-ink">{error}</p>
        </div>
      )}

      {/* Results */}
      {result && result.drugs.length > 0 && (
        <div className="mt-10 flex flex-col gap-8">
          <DrugSummaryList drugs={result.drugs} age={age} />
          <InteractionWarnings interactions={result.interactions} />
          <AgeWarnings warnings={result.age_warnings} age={age} />
        </div>
      )}

      <Disclaimer />
    </main>
  );
}
