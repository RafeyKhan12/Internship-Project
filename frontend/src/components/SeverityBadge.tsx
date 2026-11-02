import { Severity } from "@/lib/api";

const SEVERITY_STYLES: Record<string, { dot: string; text: string; label: string }> = {
  major: { dot: "bg-major", text: "text-major", label: "Major" },
  moderate: { dot: "bg-moderate", text: "text-moderate", label: "Moderate" },
  minor: { dot: "bg-minor", text: "text-minor", label: "Minor" },
};

export default function SeverityBadge({ severity }: { severity: Severity }) {
  const style = SEVERITY_STYLES[severity] ?? {
    dot: "bg-muted",
    text: "text-muted",
    label: severity,
  };

  return (
    <span className={`inline-flex items-center gap-1.5 font-mono text-xs uppercase tracking-wider ${style.text}`}>
      <span className={`h-1.5 w-1.5 rounded-full ${style.dot}`} aria-hidden />
      {style.label}
    </span>
  );
}
