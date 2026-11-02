SAMPLE_PRESCRIPTIONS = [
    # 1. Shorthand clinical notation, one drug per line
    "Metformin 500mg PO BID x30d\nLisinopril 10mg PO QD x90d",

    # 2. Fully spelled-out, plain English style
    "Take 1 tablet of Aspirin 81mg by mouth once daily for 90 days.",

    # 3. Comma-separated multiple drugs on a single line
    "Amoxicillin 500mg PO TID x10d, Ibuprofen 200mg PO PRN x5d",

    # 4. Mixed-case abbreviations and inconsistent spacing
    "atorvastatin   20mg   po   qd   x 60d\nOmeprazole 20mg po qd x 30 days",

    # 5. Known interacting pair (warfarin + aspirin) to test interaction checker
    "Warfarin 5mg PO QD x30d\nAspirin 81mg PO QD x30d\nAmoxicillin 500mg PO TID x7d",
]
