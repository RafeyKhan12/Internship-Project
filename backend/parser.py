import re

# ---------------------------------------------------------------------------
# Abbreviation / phrase lookup tables
# ---------------------------------------------------------------------------

# Common frequency abbreviations -> plain English
FREQUENCY_ABBREVIATIONS = {
    "QD": "once daily",
    "BID": "twice daily",
    "TID": "three times daily",
    "QID": "four times daily",
    "PRN": "as needed",
    "HS": "at bedtime",
    "QHS": "at bedtime",
}

# Plain-English frequency phrases that might appear instead of abbreviations.
# Checked in order, so longer/more-specific phrases come first to avoid a
# shorter phrase matching inside a longer one.
FREQUENCY_PHRASES = [
    ("four times daily", "four times daily"),
    ("four times a day", "four times daily"),
    ("three times daily", "three times daily"),
    ("three times a day", "three times daily"),
    ("twice daily", "twice daily"),
    ("twice a day", "twice daily"),
    ("once daily", "once daily"),
    ("once a day", "once daily"),
    ("as needed", "as needed"),
    ("at bedtime", "at bedtime"),
]

# Common route abbreviations -> plain English
ROUTE_ABBREVIATIONS = {
    "PO": "oral",
    "IV": "intravenous",
    "IM": "intramuscular",
    "SC": "subcutaneous",
    "SL": "sublingual",
    "PR": "rectal",
}

# Plain-English route phrases
ROUTE_PHRASES = [
    ("by mouth", "oral"),
    ("orally", "oral"),
    ("topically", "topical"),
    ("topical", "topical"),
    ("by injection", "injection"),
    ("intravenously", "intravenous"),
]

# Units recognized as part of a dose (e.g. "500mg", "10 units")
DOSE_UNITS = r"(?:mg|mcg|g|ml|units?|iu)"

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

DOSE_RE = re.compile(r"(\d+\.?\d*)\s*(" + DOSE_UNITS + r")\b", re.IGNORECASE)

# "of <DrugName>" pattern for plain-English sentences, e.g. "... of Aspirin 81mg ..."
OF_DRUGNAME_RE = re.compile(r"\bof\s+([A-Za-z][A-Za-z\-]*)\b", re.IGNORECASE)

# Frequency/route abbreviations as whole words only (so "QD" doesn't match inside another word)
FREQ_ABBR_RE = re.compile(
    r"\b(" + "|".join(FREQUENCY_ABBREVIATIONS.keys()) + r")\b", re.IGNORECASE
)
ROUTE_ABBR_RE = re.compile(
    r"\b(" + "|".join(ROUTE_ABBREVIATIONS.keys()) + r")\b", re.IGNORECASE
)

# Duration patterns: "x30d", "x 30 days", "for 90 days"
DURATION_X_RE = re.compile(
    r"\bx\s*(\d+)\s*(d|days?|w|weeks?|mo|months?)\b", re.IGNORECASE
)
DURATION_FOR_RE = re.compile(
    r"\bfor\s+(\d+)\s*(d|days?|w|weeks?|mo|months?)\b", re.IGNORECASE
)


def _normalize_duration_unit(unit: str, amount: str) -> str:
    """Map a raw duration unit (d, days, w, weeks, mo, months) to a
    normalized, correctly-pluralized word."""
    unit = unit.lower()
    if unit.startswith("d"):
        base = "day"
    elif unit.startswith("w"):
        base = "week"
    elif unit.startswith("mo"):
        base = "month"
    else:
        base = unit  # fallback, shouldn't happen given the regex

    return base if amount == "1" else base + "s"


def _split_into_entries(text: str) -> list:
    """Split raw prescription text into individual per-drug chunks.

    Splits first on newlines, then splits each line on commas. Empty
    or whitespace-only chunks are discarded.
    """
    entries = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        # Split on commas that are followed by more text (heuristic for
        # separating multiple drugs listed on one line).
        for part in re.split(r",\s*(?=[A-Za-z])", line):
            part = part.strip()
            if part:
                entries.append(part)
    return entries


def _extract_drug_name(entry: str, dose_match) -> str:
    """Best-effort extraction of the drug name from a single drug entry."""
    # Prefer the "of <DrugName>" pattern used in plain-English phrasing.
    of_match = OF_DRUGNAME_RE.search(entry)
    if of_match:
        return of_match.group(1).capitalize()

    # Otherwise, fall back to the word immediately before the dose number.
    if dose_match:
        pre_dose_text = entry[: dose_match.start()].strip()
        words = pre_dose_text.split()
        if words:
            return words[-1].strip(",.").capitalize()

    # Last resort: first word of the entry.
    words = entry.split()
    if words:
        return words[0].strip(",.").capitalize()

    return None


def _extract_frequency(entry: str) -> str:
    """Best-effort extraction of dosing frequency (abbreviation or phrase)."""
    abbr_match = FREQ_ABBR_RE.search(entry)
    if abbr_match:
        return FREQUENCY_ABBREVIATIONS[abbr_match.group(1).upper()]

    entry_lower = entry.lower()
    for phrase, meaning in FREQUENCY_PHRASES:
        if phrase in entry_lower:
            return meaning

    return None


def _extract_route(entry: str) -> str:
    """Best-effort extraction of administration route (abbreviation or phrase)."""
    abbr_match = ROUTE_ABBR_RE.search(entry)
    if abbr_match:
        return ROUTE_ABBREVIATIONS[abbr_match.group(1).upper()]

    entry_lower = entry.lower()
    for phrase, meaning in ROUTE_PHRASES:
        if phrase in entry_lower:
            return meaning

    return None


def _extract_duration(entry: str) -> str:
    """Best-effort extraction of treatment duration, e.g. 'x30d' or 'for 90 days'."""
    match = DURATION_X_RE.search(entry) or DURATION_FOR_RE.search(entry)
    if not match:
        return None

    amount, unit = match.group(1), match.group(2)
    return f"{amount} {_normalize_duration_unit(unit, amount)}"


def parse_prescription(text: str) -> list:
    """Parse raw prescription text into a list of structured drug dicts.

    Args:
        text: Raw prescription text, possibly containing multiple drugs
              separated by newlines and/or commas.

    Returns:
        A list of dicts, one per drug, each with keys:
        drug_name, dose, frequency, route, duration.
        Any field that couldn't be confidently extracted is set to None.
    """
    if not text or not text.strip():
        return []

    results = []
    for entry in _split_into_entries(text):
        dose_match = DOSE_RE.search(entry)

        drug_info = {
            "drug_name": _extract_drug_name(entry, dose_match),
            "dose": (dose_match.group(1) + dose_match.group(2).lower())
            if dose_match
            else None,
            "frequency": _extract_frequency(entry),
            "route": _extract_route(entry),
            "duration": _extract_duration(entry),
        }

        # Only keep entries where we found at least a drug name -- otherwise
        # it's likely not a real drug line (e.g. a stray blank fragment).
        if drug_info["drug_name"]:
            results.append(drug_info)

    return results


def summarize_drug(drug_dict: dict) -> str:
    """Convert a single parsed drug dict into a plain-English sentence.

    Any field that is missing (None) is gracefully omitted from the
    sentence rather than printing "None", so partially-parsed entries
    still produce a readable (if less complete) summary.

    Example:
        {"drug_name": "Metformin", "dose": "500mg", "frequency": "twice daily",
         "route": "oral", "duration": "30 days"}
        -> "Take 500mg of Metformin by mouth twice daily for 30 days."
    """
    drug_name = drug_dict.get("drug_name")
    if not drug_name:
        return "Unable to summarize: no drug name found."

    dose = drug_dict.get("dose")
    route = drug_dict.get("route")
    frequency = drug_dict.get("frequency")
    duration = drug_dict.get("duration")

    # Build up the sentence piece by piece, skipping any parts we don't have.
    sentence = "Take"
    sentence += f" {dose}" if dose else ""
    sentence += f" of {drug_name}" if dose else f" {drug_name}"

    # Route is phrased as "by mouth" for oral, otherwise "via <route>".
    if route:
        sentence += " by mouth" if route == "oral" else f" via {route}"

    sentence += f" {frequency}" if frequency else ""
    sentence += f" for {duration}" if duration else ""
    sentence += "."

    return sentence


# ---------------------------------------------------------------------------
# Demo / manual test entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from sample_data import SAMPLE_PRESCRIPTIONS

    for i, sample_text in enumerate(SAMPLE_PRESCRIPTIONS, start=1):
        print(f"\n=== Sample {i} ===")
        print(f"Raw text: {sample_text!r}")
        parsed = parse_prescription(sample_text)
        for j, drug in enumerate(parsed, start=1):
            print(f"  Drug {j} (raw):     {drug}")
            print(f"  Drug {j} (summary): {summarize_drug(drug)}")
