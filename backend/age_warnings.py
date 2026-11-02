AGE_WARNINGS = {
    "aspirin": [
        {
            "condition": "under",
            "age_threshold": 18,
            "message": "Aspirin use in children/teens with viral illness is linked to Reye's syndrome, a rare but serious condition.",
        }
    ],
    "diazepam": [
        {
            "condition": "over",
            "age_threshold": 65,
            "message": "Benzodiazepines like diazepam carry increased risk of sedation, confusion, and falls in older adults.",
        }
    ],
    "alprazolam": [
        {
            "condition": "over",
            "age_threshold": 65,
            "message": "Benzodiazepines like alprazolam carry increased risk of sedation, confusion, and falls in older adults.",
        }
    ],
    "lorazepam": [
        {
            "condition": "over",
            "age_threshold": 65,
            "message": "Benzodiazepines like lorazepam carry increased risk of sedation, confusion, and falls in older adults.",
        }
    ],
    "diphenhydramine": [
        {
            "condition": "over",
            "age_threshold": 65,
            "message": "Diphenhydramine has strong anticholinergic effects that can cause confusion and increase fall risk in older adults.",
        }
    ],
    "oxybutynin": [
        {
            "condition": "over",
            "age_threshold": 65,
            "message": "Oxybutynin's anticholinergic effects can cause cognitive impairment and confusion in older adults.",
        }
    ],
    "ibuprofen": [
        {
            "condition": "over",
            "age_threshold": 65,
            "message": "NSAIDs like ibuprofen carry increased risk of GI bleeding and kidney impairment in older adults, especially with long-term use.",
        }
    ],
    "naproxen": [
        {
            "condition": "over",
            "age_threshold": 65,
            "message": "NSAIDs like naproxen carry increased risk of GI bleeding and kidney impairment in older adults, especially with long-term use.",
        }
    ],
    "codeine": [
        {
            "condition": "under",
            "age_threshold": 12,
            "message": "Codeine is contraindicated in children under 12 due to risk of life-threatening respiratory depression.",
        }
    ],
    "tramadol": [
        {
            "condition": "under",
            "age_threshold": 18,
            "message": "Tramadol carries a risk of serious respiratory depression in children and adolescents.",
        }
    ],
    "doxycycline": [
        {
            "condition": "under",
            "age_threshold": 8,
            "message": "Doxycycline can cause permanent tooth discoloration in children under 8.",
        }
    ],
    "warfarin": [
        {
            "condition": "over",
            "age_threshold": 65,
            "message": "Older adults on warfarin have an increased bleeding risk and typically need closer monitoring.",
        }
    ],
    "zolpidem": [
        {
            "condition": "over",
            "age_threshold": 65,
            "message": "Zolpidem is associated with increased risk of falls and next-day impairment in older adults.",
        }
    ],
    "glyburide": [
        {
            "condition": "over",
            "age_threshold": 65,
            "message": "Glyburide carries an increased risk of prolonged, severe hypoglycemia in older adults.",
        }
    ],
    "amitriptyline": [
        {
            "condition": "over",
            "age_threshold": 65,
            "message": "Amitriptyline's anticholinergic and sedative effects raise the risk of confusion and falls in older adults.",
        }
    ],
}


def check_age_warnings(drug_list: list, age) -> list:
    if not drug_list or age is None:
        return []

    try:
        age = int(age)
    except (TypeError, ValueError):
        # Age wasn't a usable number -- fail safe rather than crash.
        return []

    normalized = [d.strip().lower() for d in drug_list if d and d.strip()]

    warnings = []
    for drug in normalized:
        rules = AGE_WARNINGS.get(drug)
        if not rules:
            continue

        for rule in rules:
            condition = rule["condition"]
            threshold = rule["age_threshold"]

            applies = (condition == "under" and age < threshold) or (
                condition == "over" and age > threshold
            )

            if applies:
                warnings.append(
                    {
                        "drug_name": drug,
                        "condition": condition,
                        "age_threshold": threshold,
                        "message": rule["message"],
                    }
                )

    return warnings


# ---------------------------------------------------------------------------
# Demo / manual test entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_drug_list = ["aspirin", "diazepam", "metformin"]

    for test_age in [16, 30, 70]:
        print(f"\nChecking age-based warnings for {test_drug_list} at age {test_age}:")
        results = check_age_warnings(test_drug_list, test_age)

        if not results:
            print("  No age-related warnings found.")
        else:
            for w in results:
                print(f"  [{w['drug_name'].title()}] {w['message']}")
