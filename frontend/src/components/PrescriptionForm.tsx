"use client";

import { ChangeEvent, DragEvent, useRef, useState } from "react";

const SAMPLE_TEXT = "Warfarin 5mg PO QD x30d\nAspirin 81mg PO QD x30d\nAmoxicillin 500mg PO TID x7d";

interface PrescriptionFormProps {
  text: string;
  onTextChange: (value: string) => void;
  image: File | null;
  onImageChange: (file: File | null) => void;
  age: number;
  onAgeChange: (value: number) => void;
  onSubmit: () => void;
  loading: boolean;
}

export default function PrescriptionForm({
  text,
  onTextChange,
  image,
  onImageChange,
  age,
  onAgeChange,
  onSubmit,
  loading,
}: PrescriptionFormProps) {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] ?? null;
    onImageChange(file);
  };

  const handleDrop = (e: DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file && /image\/(jpeg|png)/.test(file.type)) {
      onImageChange(file);
    }
  };

  const canSubmit = (text.trim().length > 0 || image !== null) && !loading;

  return (
    <div className="space-y-6">
      {/* Eyebrow row with the sample-fill shortcut */}
      <div className="flex items-center justify-between">
        <span className="font-mono text-xs uppercase tracking-widest text-muted">
          Step 01 — Enter a Prescription
        </span>
        <button
          type="button"
          onClick={() => {
            onTextChange(SAMPLE_TEXT);
            onImageChange(null);
          }}
          className="font-mono text-xs uppercase tracking-wider text-accent hover:text-ink transition-colors"
        >
          Try a sample →
        </button>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {/* Paste text */}
        <div className="flex flex-col gap-2">
          <label htmlFor="rx-text" className="font-mono text-xs uppercase tracking-wider text-muted">
            Paste text
          </label>
          <textarea
            id="rx-text"
            value={text}
            onChange={(e) => onTextChange(e.target.value)}
            placeholder={"Metformin 500mg PO BID x30d\nLisinopril 10mg PO QD x90d"}
            rows={7}
            className="w-full resize-none rounded-md border border-border bg-surface px-4 py-3 font-mono text-sm text-ink placeholder-muted/60 outline-none transition-colors focus:border-accent"
          />
        </div>

        {/* Upload image */}
        <div className="flex flex-col gap-2">
          <span className="font-mono text-xs uppercase tracking-wider text-muted">
            ...or upload a label
          </span>
          <label
            htmlFor="rx-image"
            onDragOver={(e) => {
              e.preventDefault();
              setIsDragging(true);
            }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={handleDrop}
            className={`flex h-[168px] flex-col items-center justify-center gap-2 rounded-md border border-dashed px-4 text-center transition-colors cursor-pointer
              ${isDragging ? "border-accent bg-accent/5" : "border-border bg-surface hover:border-muted"}`}
          >
            {image ? (
              <div className="flex flex-col items-center gap-2 px-2">
                <span className="font-mono text-xs text-ink truncate max-w-[220px]">{image.name}</span>
                <button
                  type="button"
                  onClick={(e) => {
                    e.preventDefault();
                    onImageChange(null);
                    if (fileInputRef.current) fileInputRef.current.value = "";
                  }}
                  className="font-mono text-xs uppercase tracking-wider text-muted hover:text-major transition-colors"
                >
                  Remove
                </button>
              </div>
            ) : (
              <>
                <span className="text-sm text-ink">Drop a JPG or PNG</span>
                <span className="font-mono text-xs text-muted">or click to browse</span>
              </>
            )}
            <input
              ref={fileInputRef}
              id="rx-image"
              type="file"
              accept="image/jpeg,image/png"
              onChange={handleFileSelect}
              className="hidden"
            />
          </label>
        </div>
      </div>

      {/* Age + submit row */}
      <div className="flex flex-wrap items-end justify-between gap-4 border-t border-border pt-6">
        <div className="flex flex-col gap-2">
          <label htmlFor="rx-age" className="font-mono text-xs uppercase tracking-wider text-muted">
            Patient age (adults only)
          </label>
          <input
            id="rx-age"
            type="number"
            min={18}
            max={120}
            value={age}
            onChange={(e) => onAgeChange(Number(e.target.value))}
            className="w-28 rounded-md border border-border bg-surface px-3 py-2 font-mono text-sm text-ink outline-none transition-colors focus:border-accent"
          />
        </div>

        <button
          type="button"
          onClick={onSubmit}
          disabled={!canSubmit}
          className="rounded-md bg-accent px-6 py-2.5 font-mono text-sm uppercase tracking-wider text-bg transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-30"
        >
          {loading ? "Analyzing…" : "Analyze prescription"}
        </button>
      </div>
    </div>
  );
}
