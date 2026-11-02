import type { Metadata } from "next";
import { IBM_Plex_Mono, Inter } from "next/font/google";
import "./globals.css";

// Mono carries the "clinical label" voice: headings, data fields,
// severity tags, dosage figures -- anything that reads like it came
// off a pharmacy printout. Inter carries the body copy for readability.
const mono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  variable: "--font-mono",
});

const sans = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
});

export const metadata: Metadata = {
  title: "Rx Check — Prescription Reader & Interaction Alerts",
  description:
    "Paste prescription text or upload a label photo to get a plain-English summary and instant drug interaction / age warnings.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${mono.variable} ${sans.variable}`}>
      <body>{children}</body>
    </html>
  );
}
