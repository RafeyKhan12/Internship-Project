import { AgeWarningResult } from "@/lib/api";

export default function AgeWarnings({ warnings, age }: { warnings: AgeWarningResult[]; age: number }) {
  return (
    <section className="animate-fade-up flex flex-col gap-3">
      <h2 className="font-mono text-xs uppercase tracking-widest text-muted">
        Age-Related Warnings
      </h2>

      {warnings.length === 0 ? (
        <div className="flex items-center gap-2 rounded-md border border-border bg-surface px-4 py-3">
          <span className="h-1.5 w-1.5 rounded-full bg-success" aria-hidden />
          <span className="text-sm text-ink">No age-related warnings for a patient age {age}.</span>
        </div>
      ) : (
        <ul className="flex flex-col gap-2">
          {warnings.map((warning, i) => (
            <li key={i} className="rounded-r-md border-l-2 border-l-moderate bg-surface px-4 py-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="text-sm text-ink">
                  {warning.drug_name.charAt(0).toUpperCase() + warning.drug_name.slice(1)}
                </span>
                <span className="font-mono text-xs uppercase tracking-wider text-moderate">
                  Age {age}
                </span>
              </div>
              <p className="mt-1 text-sm text-muted">{warning.message}</p>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
