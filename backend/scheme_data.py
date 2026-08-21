# scheme_data.py

scheme_matrix = {
    "PMFBY": {
        "category": "event-matched",
        "purpose": "Crop Insurance",
        "eligibility": "All farmers growing notified crops in notified areas, including tenant farmers and sharecroppers.",
        "financial_aid": "Comprehensive risk cover. Premium: 2% Kharif, 1.5% Rabi, 5% Commercial/Horticulture.",
        "exclusions": "Non-notified crops, war/theft losses, claims reported after 72 hrs of localized event.",
        "required_documents": ["RoR/Lease deed", "Sowing Certificate", "Bank Passbook", "Aadhaar Card"]
    },
    "PMKSY": {
        "category": "event-matched",
        "purpose": "Micro-Irrigation",
        "eligibility": "Landowning farmers & long-term tenants (min 7-10 yr lease) with assured water source.",
        "financial_aid": "55% subsidy for Small & Marginal (Drip/Sprinkler); 45% subsidy for others.",
        "exclusions": "Plots without water source, plots subsidized within last 7 years.",
        "required_documents": ["Land Title (7/12)", "Water Source proof", "Aadhaar & Bank A/C", "Irrigation Field Map"]
    },
    "PM-KISAN": {
        "category": "standing reference",
        "purpose": "Income Support",
        "eligibility": "All landholder farmer families with cultivable land in revenue records.",
        "financial_aid": "6,000/year in 3 equal tranches of 2,000 via DBT.",
        "exclusions": "Institutional landholders, Govt/PSU staff (excl. Class IV), Pensioners >= 10k/mo, Income tax payers & Professionals.",
        "required_documents": ["Land Records (RoR)", "Aadhaar & eKYC", "Aadhaar-linked Bank A/C", "Mobile No."]
    },
    "KCC": {
        "category": "standing reference",
        "purpose": "Farm Credit",
        "eligibility": "Owner cultivators, tenant farmers, sharecroppers, SHGs/JLGs. Priority for Small & Marginal.",
        "financial_aid": "Loans up to ₹3L-₹5L. Net rate of 4%.",
        "exclusions": "Defaulters with active NPA status, non-agricultural commercial use.",
        "required_documents": ["ID/Address Proof", "7/12 Land Extract/Lease", "Photo & Sowing Proof"]
    },
    "SMAM": {
        "category": "standing reference",
        "purpose": "Mechanisation",
        "eligibility": "Small, marginal, medium & large farmers. Priority: Women, SC/ST, Hill state farmers, FPOs & Cooperatives.",
        "financial_aid": "40%-50% for General; 50%-80% for SC/ST/Women/Small farmers. Up to 80% grant for CHCs.",
        "exclusions": "Subsidy availed on same equipment type in last 3-5 years, non-empanelled brands.",
        "required_documents": ["Aadhaar & Bank Passbook", "Land Records (RoR)", "Caste Certificate", "Dealer Quotation"]
    },
    "Soil Health Card": {
        "category": "standing reference",
        "purpose": "Diagnostic",
        "eligibility": "Universal: All farmers (owners, tenants, sharecroppers) across all states and crop categories.",
        "financial_aid": "100% Free / Subsidized 12-parameter soil report card every 3 years with dosage advisory.",
        "exclusions": "None (Universal coverage).",
        "required_documents": ["Aadhaar Card", "Land Survey/Khasra No.", "Mobile Number"]
    }
}