import itertools

# ---------------------------------------------------------------------------
# Interaction dataset (~40 well-known drug-drug interaction pairs)
# ---------------------------------------------------------------------------
# Each key is a frozenset of the two (lowercase) drug names involved.
# Each value records the drug names again (for easy display), a severity
# rating (minor / moderate / major), and a short plain-English explanation.

INTERACTIONS = {
    frozenset({"warfarin", "aspirin"}): {
        "drug_1": "warfarin",
        "drug_2": "aspirin",
        "severity": "major",
        "explanation": "Combining these significantly increases the risk of serious bleeding.",
    },
    frozenset({"warfarin", "ibuprofen"}): {
        "drug_1": "warfarin",
        "drug_2": "ibuprofen",
        "severity": "major",
        "explanation": "NSAIDs like ibuprofen increase bleeding risk when combined with warfarin.",
    },
    frozenset({"warfarin", "naproxen"}): {
        "drug_1": "warfarin",
        "drug_2": "naproxen",
        "severity": "major",
        "explanation": "NSAIDs like naproxen increase bleeding risk when combined with warfarin.",
    },
    frozenset({"warfarin", "amiodarone"}): {
        "drug_1": "warfarin",
        "drug_2": "amiodarone",
        "severity": "major",
        "explanation": "Amiodarone increases warfarin's blood-thinning effect, raising bleeding risk.",
    },
    frozenset({"warfarin", "fluconazole"}): {
        "drug_1": "warfarin",
        "drug_2": "fluconazole",
        "severity": "major",
        "explanation": "Fluconazole raises warfarin levels, increasing the risk of bleeding.",
    },
    frozenset({"warfarin", "cimetidine"}): {
        "drug_1": "warfarin",
        "drug_2": "cimetidine",
        "severity": "moderate",
        "explanation": "Cimetidine can increase warfarin's anticoagulant effect.",
    },
    frozenset({"warfarin", "acetaminophen"}): {
        "drug_1": "warfarin",
        "drug_2": "acetaminophen",
        "severity": "moderate",
        "explanation": "Regular high-dose acetaminophen use may increase INR and bleeding risk.",
    },
    frozenset({"warfarin", "amoxicillin"}): {
        "drug_1": "warfarin",
        "drug_2": "amoxicillin",
        "severity": "moderate",
        "explanation": "Antibiotics like amoxicillin can potentiate warfarin's anticoagulant effect.",
    },
    frozenset({"warfarin", "phenytoin"}): {
        "drug_1": "warfarin",
        "drug_2": "phenytoin",
        "severity": "moderate",
        "explanation": "Phenytoin and warfarin can each alter the other's blood levels unpredictably.",
    },
    frozenset({"warfarin", "clarithromycin"}): {
        "drug_1": "warfarin",
        "drug_2": "clarithromycin",
        "severity": "major",
        "explanation": "Clarithromycin can significantly raise warfarin levels, increasing bleeding risk.",
    },
    frozenset({"warfarin", "vitamin k"}): {
        "drug_1": "warfarin",
        "drug_2": "vitamin k",
        "severity": "moderate",
        "explanation": "Vitamin K can reduce warfarin's anticoagulant effectiveness.",
    },
    frozenset({"phenelzine", "sertraline"}): {
        "drug_1": "phenelzine",
        "drug_2": "sertraline",
        "severity": "major",
        "explanation": "Combining an MAOI with an SSRI carries a serious risk of serotonin syndrome.",
    },
    frozenset({"phenelzine", "fluoxetine"}): {
        "drug_1": "phenelzine",
        "drug_2": "fluoxetine",
        "severity": "major",
        "explanation": "Combining an MAOI with an SSRI carries a serious risk of serotonin syndrome.",
    },
    frozenset({"tranylcypromine", "meperidine"}): {
        "drug_1": "tranylcypromine",
        "drug_2": "meperidine",
        "severity": "major",
        "explanation": "This combination can cause a life-threatening reaction including serotonin syndrome.",
    },
    frozenset({"fluoxetine", "tramadol"}): {
        "drug_1": "fluoxetine",
        "drug_2": "tramadol",
        "severity": "major",
        "explanation": "Both increase serotonin activity, raising the risk of serotonin syndrome.",
    },
    frozenset({"sertraline", "tramadol"}): {
        "drug_1": "sertraline",
        "drug_2": "tramadol",
        "severity": "major",
        "explanation": "Both increase serotonin activity, raising the risk of serotonin syndrome.",
    },
    frozenset({"lisinopril", "potassium chloride"}): {
        "drug_1": "lisinopril",
        "drug_2": "potassium chloride",
        "severity": "moderate",
        "explanation": "ACE inhibitors combined with potassium supplements can cause dangerous hyperkalemia.",
    },
    frozenset({"lisinopril", "spironolactone"}): {
        "drug_1": "lisinopril",
        "drug_2": "spironolactone",
        "severity": "moderate",
        "explanation": "Both raise potassium levels, increasing the risk of hyperkalemia together.",
    },
    frozenset({"enalapril", "potassium chloride"}): {
        "drug_1": "enalapril",
        "drug_2": "potassium chloride",
        "severity": "moderate",
        "explanation": "ACE inhibitors combined with potassium supplements can cause dangerous hyperkalemia.",
    },
    frozenset({"lisinopril", "ibuprofen"}): {
        "drug_1": "lisinopril",
        "drug_2": "ibuprofen",
        "severity": "moderate",
        "explanation": "NSAIDs can reduce the blood-pressure-lowering effect of ACE inhibitors and stress the kidneys.",
    },
    frozenset({"simvastatin", "clarithromycin"}): {
        "drug_1": "simvastatin",
        "drug_2": "clarithromycin",
        "severity": "major",
        "explanation": "Clarithromycin raises simvastatin levels, increasing the risk of muscle damage (rhabdomyolysis).",
    },
    frozenset({"atorvastatin", "clarithromycin"}): {
        "drug_1": "atorvastatin",
        "drug_2": "clarithromycin",
        "severity": "major",
        "explanation": "Clarithromycin raises atorvastatin levels, increasing the risk of muscle damage (rhabdomyolysis).",
    },
    frozenset({"simvastatin", "gemfibrozil"}): {
        "drug_1": "simvastatin",
        "drug_2": "gemfibrozil",
        "severity": "major",
        "explanation": "This combination significantly raises the risk of severe myopathy and rhabdomyolysis.",
    },
    frozenset({"digoxin", "amiodarone"}): {
        "drug_1": "digoxin",
        "drug_2": "amiodarone",
        "severity": "major",
        "explanation": "Amiodarone raises digoxin levels, increasing the risk of digoxin toxicity.",
    },
    frozenset({"digoxin", "furosemide"}): {
        "drug_1": "digoxin",
        "drug_2": "furosemide",
        "severity": "moderate",
        "explanation": "Furosemide can cause low potassium, which increases the risk of digoxin toxicity.",
    },
    frozenset({"lithium", "ibuprofen"}): {
        "drug_1": "lithium",
        "drug_2": "ibuprofen",
        "severity": "moderate",
        "explanation": "NSAIDs can reduce lithium clearance, raising lithium levels toward toxicity.",
    },
    frozenset({"lithium", "hydrochlorothiazide"}): {
        "drug_1": "lithium",
        "drug_2": "hydrochlorothiazide",
        "severity": "major",
        "explanation": "Thiazide diuretics can significantly raise lithium levels, risking lithium toxicity.",
    },
    frozenset({"metformin", "cimetidine"}): {
        "drug_1": "metformin",
        "drug_2": "cimetidine",
        "severity": "moderate",
        "explanation": "Cimetidine can increase metformin levels in the blood.",
    },
    frozenset({"clopidogrel", "omeprazole"}): {
        "drug_1": "clopidogrel",
        "drug_2": "omeprazole",
        "severity": "moderate",
        "explanation": "Omeprazole may reduce clopidogrel's antiplatelet effectiveness.",
    },
    frozenset({"alprazolam", "oxycodone"}): {
        "drug_1": "alprazolam",
        "drug_2": "oxycodone",
        "severity": "major",
        "explanation": "Combining a benzodiazepine with an opioid raises the risk of severe respiratory depression.",
    },
    frozenset({"diazepam", "oxycodone"}): {
        "drug_1": "diazepam",
        "drug_2": "oxycodone",
        "severity": "major",
        "explanation": "Combining a benzodiazepine with an opioid raises the risk of severe respiratory depression.",
    },
    frozenset({"lorazepam", "morphine"}): {
        "drug_1": "lorazepam",
        "drug_2": "morphine",
        "severity": "major",
        "explanation": "Combining a benzodiazepine with an opioid raises the risk of severe respiratory depression.",
    },
    frozenset({"sildenafil", "nitroglycerin"}): {
        "drug_1": "sildenafil",
        "drug_2": "nitroglycerin",
        "severity": "major",
        "explanation": "This combination can cause a severe, potentially life-threatening drop in blood pressure.",
    },
    frozenset({"tadalafil", "nitroglycerin"}): {
        "drug_1": "tadalafil",
        "drug_2": "nitroglycerin",
        "severity": "major",
        "explanation": "This combination can cause a severe, potentially life-threatening drop in blood pressure.",
    },
    frozenset({"theophylline", "ciprofloxacin"}): {
        "drug_1": "theophylline",
        "drug_2": "ciprofloxacin",
        "severity": "moderate",
        "explanation": "Ciprofloxacin can raise theophylline levels, increasing the risk of toxicity.",
    },
    frozenset({"methotrexate", "ibuprofen"}): {
        "drug_1": "methotrexate",
        "drug_2": "ibuprofen",
        "severity": "major",
        "explanation": "NSAIDs can reduce methotrexate clearance, increasing the risk of serious toxicity.",
    },
    frozenset({"methotrexate", "trimethoprim"}): {
        "drug_1": "methotrexate",
        "drug_2": "trimethoprim",
        "severity": "major",
        "explanation": "Both affect folate metabolism, raising the risk of bone marrow suppression.",
    },
    frozenset({"metoprolol", "verapamil"}): {
        "drug_1": "metoprolol",
        "drug_2": "verapamil",
        "severity": "major",
        "explanation": "Combining a beta-blocker with verapamil can cause severe bradycardia or heart block.",
    },
    frozenset({"insulin", "propranolol"}): {
        "drug_1": "insulin",
        "drug_2": "propranolol",
        "severity": "moderate",
        "explanation": "Beta-blockers like propranolol can mask the warning signs of low blood sugar.",
    },
    frozenset({"spironolactone", "potassium chloride"}): {
        "drug_1": "spironolactone",
        "drug_2": "potassium chloride",
        "severity": "major",
        "explanation": "Combining a potassium-sparing diuretic with a potassium supplement can cause dangerous hyperkalemia.",
    },
}


def check_interactions(drug_list: list) -> list:
    if not drug_list or len(drug_list) < 2:
        return []

    # Normalize names (lowercase, stripped) so matching is case-insensitive
    # and ignores incidental whitespace.
    normalized = [d.strip().lower() for d in drug_list if d and d.strip()]

    matches = []
    for drug_a, drug_b in itertools.combinations(normalized, 2):
        key = frozenset({drug_a, drug_b})
        if key in INTERACTIONS:
            matches.append(INTERACTIONS[key])

    return matches


# ---------------------------------------------------------------------------
# Demo / manual test entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_drug_list = ["warfarin", "aspirin", "metformin"]

    print(f"Checking interactions for: {test_drug_list}\n")
    results = check_interactions(test_drug_list)

    if not results:
        print("No known interactions found.")
    else:
        for match in results:
            print(
                f"  [{match['severity'].upper()}] "
                f"{match['drug_1']} + {match['drug_2']}: {match['explanation']}"
            )
