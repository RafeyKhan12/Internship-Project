import { InteractionResult } from "@/lib/api";
import SeverityBadge from "./SeverityBadge";

const BORDER_BY_SEVERITY: Record<string, string> = {
  major: "border-l-major",
  moderate: "border-l-moderate",
  minor: "border-l-minor",
};

export default function InteractionWarnings({ interactions }: { interactions: InteractionResult[] }) {
  return (
    <section className="animate-fade-up flex flex-col gap-3">
      <h2 className="font-mono text-xs uppercase tracking-widest text-muted">
        Interaction Warnings
      </h2>

      {interactions.length === 0 ? (
        <div className="flex items-center gap-2 rounded-md border border-border bg-surface px-4 py-3">
          <span className="h-1.5 w-1.5 rounded-full bg-success" aria-hidden />
          <span className="text-sm text-ink">No known interactions found among the entered drugs.</span>
        </div>
      ) : (
        <ul className="flex flex-col gap-2">
          {interactions.map((match, i) => (
            <li
              key={i}
              className={`rounded-r-md border-l-2 bg-surface px-4 py-3 ${BORDER_BY_SEVERITY[match.severity] ?? "border-l-muted"}`}
            >
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="text-sm text-ink">
                  {titleCase(match.drug_1)} + {titleCase(match.drug_2)}
                </span>
                <SeverityBadge severity={match.severity} />
              </div>
              <p className="mt-1 text-sm text-muted">{match.explanation}</p>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

function titleCase(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1);
}
