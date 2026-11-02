import requests

RXNORM_BASE_URL = "https://rxnav.nlm.nih.gov/REST/rxcui.json"

# Keep the request snappy so a slow/unreachable API doesn't stall the UI.
REQUEST_TIMEOUT_SECONDS = 5


def get_rxcui(drug_name: str):
    if not drug_name or not drug_name.strip():
        return None

    try:
        response = requests.get(
            RXNORM_BASE_URL,
            params={"name": drug_name.strip()},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()  # raises for 4xx/5xx status codes

        data = response.json()
        # Expected shape: {"idGroup": {"rxnormId": ["12345"], "name": "..."}}
        # If the drug isn't recognized, "rxnormId" is absent or empty.
        rxcui_list = data.get("idGroup", {}).get("rxnormId")
        if rxcui_list:
            return rxcui_list[0]
        return None

    except requests.exceptions.Timeout:
        # API took too long to respond -- treat as "not found" for the caller.
        print(f"[rxnorm_api] Timeout while looking up '{drug_name}'.")
        return None
    except requests.exceptions.RequestException as e:
        # Covers connection errors, DNS failures, bad status codes, etc.
        print(f"[rxnorm_api] Request error while looking up '{drug_name}': {e}")
        return None
    except (ValueError, KeyError, AttributeError) as e:
        # Covers malformed/unexpected JSON response shape.
        print(f"[rxnorm_api] Unexpected response while looking up '{drug_name}': {e}")
        return None


# ---------------------------------------------------------------------------
# Demo / manual test entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_drug_names = [
        "Metformin",
        "Aspirin",
        "Warfarin",
        "Lisinopril",
        "Fakedrugxyz123",  # deliberately not a real drug, to test "not found"
    ]

    print("Testing get_rxcui() against the RxNorm API...\n")
    for name in test_drug_names:
        rxcui = get_rxcui(name)
        if rxcui:
            print(f"  {name!r:20} -> RxCUI: {rxcui}")
        else:
            print(f"  {name!r:20} -> NOT FOUND (or lookup failed)")
