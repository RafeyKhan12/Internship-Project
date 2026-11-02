import { DrugResult } from "@/lib/api";

interface DrugSummaryListProps {
  drugs: DrugResult[];
  age: number;
}

// The signature element: the results are framed like a pharmacy label
// torn from a sheet -- a dashed perforation rule under a small
// monospace meta line (the way a label prints "RX # · QTY · DATE").
// Everything below it stays quiet: plain rows, no extra ornamentation.
export default function DrugSummaryList({ drugs, age }: DrugSummaryListProps) {
  return (
    <div className="animate-fade-up overflow-hidden rounded-md border border-border bg-surface">
      <div className="label-perforation flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1 px-5 pb-3 pt-4">
        <span className="font-mono text-xs uppercase tracking-widest text-accent">
          Rx Analysis
        </span>
        <span className="font-mono text-xs uppercase tracking-wider text-muted">
          Age {age} · {drugs.length} {drugs.length === 1 ? "medication" : "medications"}
        </span>
      </div>

      <ul className="divide-y divide-border">
        {drugs.map((drug, i) => (
          <li key={i} className="flex flex-col gap-1.5 px-5 py-4">
            <p className="text-sm leading-relaxed text-ink">{drug.summary}</p>
            <div className="flex flex-wrap items-center gap-x-3 gap-y-1 font-mono text-xs text-muted">
              {drug.rxcui ? (
                <span className="text-success">RxCUI {drug.rxcui}</span>
              ) : (
                <span className="text-muted/70">RxCUI not verified</span>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
