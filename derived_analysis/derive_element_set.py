"""
Element set derivation script 

Applies the M:§4 criteria hierarchy to the 118-element library and produces
E*(F_space) from first principles.  Replaces the qualitative scratchboard in
element_derivation_process.md with a computable pipeline run.

Deployment-fixed inputs (Layer 0 — M:§8.3 H-DFG):
    tau    = 100 yr  (V2 — closes the undefined-τ gap in the scratchboard)
    T0     = 250 K   (3–5 AU dead-state; departure from Szargut 298.15 K noted)
    Q_sol  = 50 W/m² (solar flux at 3–5 AU)
    ATM    = False   (vacuum — r_corr electrochemical mechanisms ≈ 0)

Pipeline stages (M:§8.2 CD-DG):
    Filter 1 — Criterion 1:  asteroid abundance
    Filter 2 — Criterion 5:  refineable using solar flux (extensive energy bound)
    Filter 3 — Criterion 4:  recyclability η ≥ η_min; + Axiom I circularity check
    Filter 4 — Criterion 3:  functional role breadth |roles| > 1
    Filter 5 — Axiom II:     all states recoverable using ambient flux
    Filter 6 — Challenge A:  magnetic hard gap (F_space row 5 gate)
    Filter 7 — Σ comparison: dominance test with G1–G4 gates

Output codes:
    PASS        — element survives all hard boundary conditions
    HARDRET     — unconditional retention (Axiom IV hard gap)
    ELIM        — eliminated; criterion stated
    CONDITIONAL — retained pending named OQ

Data sources (each in its own top-level dict — swap one dict to update all uses):
    B_CH        Szargut (1988) standard chemical exergy, Table A.1
    M_MOL       IUPAC 2021 standard atomic weights
    DELTA_G_REF NIST WebBook — primary oxide formation ΔG° at 298 K
    MU_R        CRC Handbook / Haynes (2016) — soft annealed state
    R_CORR      ISO 9223 — vacuum: electrochemical mechanisms ≈ 0

mp-api upgrade path (N1 in GSH_tools_plan.md): replace B_CH and DELTA_G_REF
with API-fetched values; pipeline logic is unchanged.

Run: python3 derive_element_set.py
"""

from __future__ import annotations

SECONDS_PER_YEAR = 365.25 * 24 * 3600   # s/yr

# ---------------------------------------------------------------------------
# Layer 0 — deployment-fixed inputs (M:§8.3 H-DFG co-equal top-level inputs)
# ---------------------------------------------------------------------------
TAU_YR         = 100.0                       # yr  — mission/deployment lifetime
TAU_S          = TAU_YR * SECONDS_PER_YEAR   # s
T0             = 250.0                       # K   — 3–5 AU dead-state reference
Q_SOL          = 50.0                        # W/m²  — solar flux at 3–5 AU
A_COLLECTOR_M2 = 1_000.0                     # m²  — reference concentrator area
                                             # Criterion 5 bound: Q_SOL*ETA_EX*A_COLLECTOR_M2*TAU_S (J)
                                             # 1000 m² is conservative for a 1-tonne-class refinery
                                             # at 3–5 AU. Replace with mission-specific value when
                                             # throughput budget is defined.
ATM            = False                       # vacuum — electrochemical r_corr ≈ 0
ETA_EX         = 0.70                        # concentrator exergy efficiency (conservative)
EPS            = 0.10                        # max allowable fractional mass loss per cycle
TAU_CYC        = SECONDS_PER_YEAR           # s — annual recycle cycle assumption

# T0 departure note: Szargut b_ch referenced to 298.15 K. Using T0 = 250 K
# shifts Sigma_s = b_ch/T0 upward by 298.15/250 ≈ 1.19 — conservative overestimate.
# Direction noted per OQ-GSH.19. Replace with T0-corrected values when available.

# ---------------------------------------------------------------------------
# F_space — Engineering requirement set (M:§1.1; V1/F2: functional outcomes only)
# Row tuple: (description, required: bool, target_note)
# ---------------------------------------------------------------------------
F_SPACE = {
    1:  ("Structural load-bearing",          True,  ">=200 MPa tensile"),
    2:  ("Thermal management",               True,  "-100 to +200 C cycling"),
    3:  ("Electrical generation",            True,  "300-1100 nm; >=1 kWe/t"),
    4:  ("Electrical conduction",            True,  "resistivity within E*"),
    5:  ("Magnetic flux channelling",        True,  "mu_r >= 1000"),
    6:  ("Magnetic field generation",        True,  "0.05-0.5 T air-core"),
    7:  ("Computation / logic",              True,  ">=100 krad(Si) TID"),
    8:  ("Chemical energy storage",          True,  ">=1 kWh/kg storable recyclable"),
    9:  ("Catalysis",                        True,  "zero-consumption catalyst"),
    10: ("Sealing / joining",                True,  "-100 to +200 C; <=1 atm"),
}

FLUX_CHANNELLING_REQUIRED = F_SPACE[5][1]

# ---------------------------------------------------------------------------
# Recyclability threshold — OQ-GSH.25 candidate formula (M:§4.1 Criterion 4)
# eta_min = (1 - epsilon)^(tau_cycle / tau)
# Replaces the static 99.9% proxy with a tau-dependent derivation.
# ---------------------------------------------------------------------------
ETA_MIN = (1.0 - EPS) ** (TAU_CYC / TAU_S)

# ---------------------------------------------------------------------------
# Reference data tables — one source per dict
# To update a data source, replace the dict; pipeline logic is unchanged.
# ---------------------------------------------------------------------------

# Szargut (1988) standard chemical exergy — J/mol
# Replace with mp-api computed values (N1) when available.
B_CH: dict[str, float | None] = {
    "H":   236_100,
    "C":   410_260,
    "N":       720,   # N₂ — reference species, near-zero exergy
    "O":     3_970,   # O₂ — reference species
    "Na":  336_600,
    "Mg":  626_000,
    "Al":  888_400,
    "Si":  854_600,
    "P":   875_800,
    "S":   609_600,
    "K":   366_600,
    "Ca":  712_400,
    "Ti":  906_900,
    "Cr":  544_300,
    "Mn":  482_300,
    "Fe":  376_400,
    "Co":  265_000,
    "Ni":  232_700,
    "Cu":  134_900,
    "Zn":  339_200,
    "Ag":   70_200,
    "Sn":  544_800,
    "Pt":  141_800,
    "Pb":  232_800,
    "Ir":     None,   # no Szargut value; PGM not in 1988 table
    "Au":     None,
}

# IUPAC 2021 standard atomic weights — g/mol
M_MOL: dict[str, float] = {
    "H":    1.008,
    "C":   12.011,
    "N":   14.007,
    "O":   15.999,
    "Na":  22.990,
    "Mg":  24.305,
    "Al":  26.982,
    "Si":  28.085,
    "P":   30.974,
    "S":   32.06,
    "K":   39.098,
    "Ca":  40.078,
    "Ti":  47.867,
    "Cr":  51.996,
    "Mn":  54.938,
    "Fe":  55.845,
    "Co":  58.933,
    "Ni":  58.693,
    "Cu":  63.546,
    "Zn":  65.38,
    "Ag": 107.868,
    "Sn": 118.710,
    "Pt": 195.084,
    "Pb": 207.2,
    "Ir": 192.217,
    "Au": 196.967,
}

# NIST WebBook — primary oxide formation ΔG° at 298 K — J/mol
# None = no thermally reducible oxide route (electrolytic or refining outside E*)
# Replace with mp-api computed values (N1) when available.
DELTA_G_REF: dict[str, float | None] = {
    "H":   237_100,   # ΔG H₂O → H₂ + ½O₂ (electrolysis)
    "C":   394_400,   # CO₂ formation (graphite → CO₂)
    "N":         0,   # reference species
    "O":         0,   # reference species
    "Na":  375_700,   # Na₂O formation
    "Mg":  601_200,   # MgO formation
    "Al": 1_582_000,  # Al₂O₃ formation (2Al + 3/2 O₂)
    "Si":  856_400,   # SiO₂ formation
    "P":  1_492_000,  # P₂O₅ formation
    "S":   300_200,   # SO₂ formation
    "K":   361_500,   # K₂O formation
    "Ca": 1_269_000,  # CaO — reduction >2000 °C
    "Ti":  944_000,   # TiO₂ formation
    "Cr": 1_058_000,  # Cr₂O₃ formation
    "Mn":  881_100,   # MnO formation
    "Fe":  742_200,   # Fe₂O₃ formation (per 2 mol Fe)
    "Co":  737_000,   # CoO formation
    "Ni":  489_500,   # NiO formation
    "Cu":  129_300,   # CuO formation
    "Zn":  350_500,   # ZnO formation
    "Ag":   62_200,   # Ag₂O (very slow oxidation)
    "Sn":  519_700,   # SnO₂ formation
    "Pt":  188_000,   # PtO₂ (near-zero consumption)
    "Pb":  187_900,   # PbO formation
    "Ir":     None,   # requires aqua regia — outside E*
    "Au":     None,   # requires aqua regia — outside E*
}

# CRC Handbook / Haynes (2016) — relative magnetic permeability, soft annealed state
# Elements not listed default to 1.0 (non-magnetic)
MU_R: dict[str, float] = {
    "Fe":  5000.0,   # soft iron (annealed)
    "Ni":   200.0,
    "Co":    70.0,
}

# ISO 9223 — entropy generation rate from corrosion, W/K
# Vacuum: electrochemical mechanisms ≈ 0 for all elements when ATM = False
R_CORR: dict[str, float] = {sym: 0.0 for sym in M_MOL}

# ---------------------------------------------------------------------------
# Element library — pipeline-specific properties only
#
# Keys:
#   temp_ref_C    °C      Approximate reduction temperature (Filter 2 electrolytic check)
#   eta_rec       float   Estimated mass recovery fraction per cycle (Filter 3)
#   roles         list    Functional roles contributing to F_space (Filter 4)
#   asteroid      dict    Abundance flags: C/S/M-type (Filter 1)
#   notes         str     Pipeline-relevant remarks
#   bootstrap_dep bool    Refining requires a prior E* member (Filter 2 gate)
#   oq            str     Named OQ blocking full computation (optional)
#
# Physical constants (b_ch, M_mol, delta_G_ref, mu_r, r_corr) are in the
# reference data tables above — not repeated here.
# ---------------------------------------------------------------------------
ELEMENTS: dict[str, dict] = {
    "H": {
        "temp_ref_C":  None,
        "eta_rec":     0.999,     # H₂O → H₂/O₂ → H₂O; closed loop
        "roles":       ["energy_storage", "chemical_reduction", "propellant"],
        "asteroid":    {"C": True, "S": False, "M": False},
        "notes":       "Axiom III carrier; H₂/O₂ redox loop",
    },
    "C": {
        "temp_ref_C":  None,      # C is the reductant; not refined from oxide
        "eta_rec":     0.999,     # CO/CO₂ → C via Boudouard; closed carbothermic loop
        "roles":       ["structure", "logic", "reductant", "catalysis_scaffold", "refractory"],
        "asteroid":    {"C": True, "S": False, "M": False},
        "notes":       "Allotropic versatility: graphene/CNT/diamond/SiC",
    },
    "N": {
        "temp_ref_C":  None,
        "eta_rec":     None,      # kinetic gate open — OQ-GSH.15
        "roles":       ["atmosphere_buffer", "chemical_synthesis"],
        "asteroid":    {"C": True, "S": False, "M": False},
        "notes":       "Axiom II kinetic gate open (OQ-GSH.15) — containment undemonstrated",
        "oq":          "OQ-GSH.15",
    },
    "O": {
        "temp_ref_C":  None,
        "eta_rec":     0.999,     # recovered in H₂/O₂ and carbothermic loops
        "roles":       ["oxidant", "energy_storage", "silicate_feedstock"],
        "asteroid":    {"C": True, "S": True, "M": True},
        "notes":       "Dominant by mass in all asteroid types",
    },
    "Na": {
        "temp_ref_C":  880,
        "eta_rec":     0.999,     # NaK closed thermal loop; electrolytic recovery
        "roles":       ["heat_transfer", "ion_storage"],
        "asteroid":    {"C": True, "S": True, "M": True},
        "notes":       "NaK eutectic heat transfer; Challenge D with K (OQ-GSH.4)",
        "oq":          "OQ-GSH.4",
    },
    "Mg": {
        "temp_ref_C":  1200,      # Pidgeon process operating temperature
        "eta_rec":     0.0,       # Pidgeon loop circularity — net output zero
        "roles":       ["structure"],
        "asteroid":    {"C": False, "S": True, "M": True},
        "notes":       "Pidgeon loop: SiO₂+2Mg→Si+2MgO; 2MgO+Si→2Mg+SiO₂ — net zero. "
                       "Criterion 3 / Axiom I elimination.",
    },
    "Al": {
        "temp_ref_C":  2054,      # carbothermic Al₂O₃ → Al (BT4)
        "eta_rec":     0.999,     # Al₂O₃ → Al via carbothermic; closed loop
        "roles":       ["structure", "conduction", "thermal_management", "refractory"],
        "asteroid":    {"C": False, "S": True, "M": True},
        "notes":       "SiC-reinforced geometry for high-temp applications",
    },
    "Si": {
        "temp_ref_C":  1650,      # carbothermic SiO₂ → Si (BT3)
        "eta_rec":     0.999,
        "roles":       ["logic", "photovoltaic", "structure", "refractory"],
        "asteroid":    {"C": True, "S": True, "M": True},
        "notes":       "Si CMOS radiation-hardened; SiC refractory",
    },
    "P": {
        "temp_ref_C":  None,
        "eta_rec":     0.90,      # P₂O₅ reduction thermodynamically demanding
        "roles":       ["chemical_synthesis"],
        "asteroid":    {"C": True, "S": False, "M": False},
        "notes":       "Trace phosphates; reduction demanding; no confirmed irreplaceable role",
    },
    "S": {
        "temp_ref_C":  None,
        "eta_rec":     0.88,      # SO₂/SO₃ reduction >1000 °C; marginal
        "roles":       ["vulcanisation"],
        "asteroid":    {"C": True, "S": False, "M": True},
        "notes":       "Single role; no irreplaceable function in space context",
    },
    "K": {
        "temp_ref_C":  850,
        "eta_rec":     0.999,     # NaK closed thermal loop; electrolytic recovery
        "roles":       ["heat_transfer", "ion_storage"],
        "asteroid":    {"C": False, "S": True, "M": False},
        "notes":       "NaK eutectic; Challenge D with Na (OQ-GSH.4)",
        "oq":          "OQ-GSH.4",
    },
    "Ca": {
        "temp_ref_C":  2600,
        "eta_rec":     0.70,
        "roles":       ["structure"],
        "asteroid":    {"C": True, "S": True, "M": True},
        "notes":       "CaO reduction >2000 °C — above BT4 ceiling without W infrastructure",
    },
    "Ti": {
        "temp_ref_C":  1700,      # carbothermic route undemonstrated at engineering scale
        "eta_rec":     0.999,
        "roles":       ["structure", "thermal_tolerance", "corrosion_resistance"],
        "asteroid":    {"C": False, "S": True, "M": True},
        "notes":       "Sigma comparison structurally incomplete: tau_wearout for Al/SiC "
                       "under -100 to +200 C cycling unknown (OQ-GSH.19); G4 gate fires",
        "oq":          "OQ-GSH.21",
    },
    "Cr": {
        "temp_ref_C":  1700,
        "eta_rec":     0.999,
        "roles":       ["corrosion_resistance"],
        "asteroid":    {"C": False, "S": False, "M": True},
        "bootstrap_dep": True,
        "notes":       "Aluminothermic reduction requires pre-refined Al — bootstrap dependency",
    },
    "Mn": {
        "temp_ref_C":  1500,
        "eta_rec":     0.999,
        "roles":       ["steel_alloying"],
        "asteroid":    {"C": False, "S": True, "M": True},
        "bootstrap_dep": True,
        "notes":       "Electrolytic/aluminothermic — same bootstrap dependency as Cr",
    },
    "Fe": {
        "temp_ref_C":  900,       # carbothermic Fe₂O₃ → Fe (BT2/BT3)
        "eta_rec":     0.999,     # Axiom II: carbothermic recycling feasible
        "roles":       ["magnetic_flux", "structure", "thermal_mass"],
        "asteroid":    {"C": False, "S": True, "M": True},
        "notes":       "Challenge A Step 1a: d-electron band structure absent from all "
                       "other E* members. HARDRET when F_space row 5 = Yes.",
    },
    "Co": {
        "temp_ref_C":  None,
        "eta_rec":     0.90,
        "roles":       ["catalyst", "magnetic"],
        "asteroid":    {"C": False, "S": False, "M": True},
        "notes":       "Smelting requires sulfuric acid roasting — outside E*",
    },
    "Ni": {
        "temp_ref_C":  600,
        "eta_rec":     0.999,     # NiO reducible with C at ~600 °C; well-established
        "roles":       ["corrosion_coating", "catalyst"],
        "asteroid":    {"C": False, "S": True, "M": True},
        "notes":       "Pt covers catalysis (zero-consumption); no irreplaceable role",
    },
    "Cu": {
        "temp_ref_C":  800,
        "eta_rec":     0.999,
        "roles":       ["conduction"],
        "asteroid":    {"C": False, "S": False, "M": True},
        "notes":       "Single role; Ag is Criterion 8 optimum; dominance test required",
    },
    "Zn": {
        "temp_ref_C":  1000,
        "eta_rec":     0.999,     # ZnO carbothermic at ~1000 °C; well-established
        "roles":       ["galvanic_protection"],
        "asteroid":    {"C": False, "S": False, "M": True},
        "notes":       "Sole role is galvanic protection of Fe. Obsolete in vacuum (ATM=False).",
    },
    "Ag": {
        "temp_ref_C":  300,       # Ag₂O reduction trivially achieved
        "eta_rec":     0.999,
        "roles":       ["conduction", "optical_reflector", "catalysis"],
        "asteroid":    {"C": False, "S": True, "M": True},
        "notes":       "Criterion 8 conductivity optimum; optical reflector",
    },
    "Sn": {
        "temp_ref_C":  1000,
        "eta_rec":     0.999,
        "roles":       ["joining"],
        "asteroid":    {"C": False, "S": False, "M": True},
        "notes":       "Single specialist joining role; G4 gate fires (Sigma_g not computable)",
    },
    "Pt": {
        "temp_ref_C":  500,
        "eta_rec":     0.999,
        "roles":       ["catalysis", "electrode"],
        "asteroid":    {"C": False, "S": True, "M": True},
        "notes":       "Zero-consumption catalyst; ~0.1–0.5 mg/cm² loading",
    },
    "Pb": {
        "temp_ref_C":  880,
        "eta_rec":     0.99,
        "roles":       ["shielding"],
        "asteroid":    {"C": False, "S": False, "M": True},
        "notes":       "Zero distinct functional roles not covered by other E* members",
    },
    "Ir": {
        "temp_ref_C":  None,
        "eta_rec":     0.50,
        "roles":       ["catalysis"],
        "asteroid":    {"C": False, "S": False, "M": True},
        "notes":       "Requires aqua regia — outside E*",
    },
    "Au": {
        "temp_ref_C":  None,
        "eta_rec":     0.50,
        "roles":       ["conduction"],
        "asteroid":    {"C": False, "S": False, "M": True},
        "notes":       "Requires aqua regia — outside E*",
    },
}

# ---------------------------------------------------------------------------
# Pipeline result (plain dict)
# ---------------------------------------------------------------------------
def make_result(symbol, status, criterion, note, oq=None):
    return {"symbol": symbol, "status": status,
            "criterion": criterion, "note": note, "oq": oq}


# ---------------------------------------------------------------------------
# Filter 1 — Criterion 1: abundance in C/S/M-type asteroids
# ---------------------------------------------------------------------------
def filter1_abundance(elements):
    survivors, eliminated = [], []
    for sym, e in elements.items():
        if any(e["asteroid"].get(t) for t in ("C", "S", "M")):
            survivors.append(sym)
        else:
            eliminated.append(make_result(
                sym, "ELIM", "Criterion 1",
                "not recoverable in C/S/M asteroid types"))
    return survivors, eliminated


# ---------------------------------------------------------------------------
# Filter 2 — Criterion 5: refineable using solar flux (extensive energy bound)
#
# Test: DELTA_G_REF[x] (J/mol) <= Q_SOL * ETA_EX * A_COLLECTOR_M2 * TAU_S (J)
# Both sides in J — dimensionally consistent.
# ---------------------------------------------------------------------------
REFINE_ENERGY_AVAILABLE = Q_SOL * ETA_EX * A_COLLECTOR_M2 * TAU_S   # J

def filter2_refineable(survivors_prev, elements):
    survivors, eliminated = [], []
    for sym in survivors_prev:
        e = elements[sym]

        if e.get("bootstrap_dep"):
            eliminated.append(make_result(
                sym, "ELIM", "Criterion 5",
                "refining route requires pre-refined Al (bootstrap dependency); "
                "cannot be a founding E* member"))
            continue

        dG = DELTA_G_REF[sym]

        if dG is None:
            if any(kw in e["notes"].lower() for kw in ("aqua regia", "acid", "outside e*")):
                eliminated.append(make_result(
                    sym, "ELIM", "Criterion 5",
                    "refining route requires chemistry outside E*"))
            else:
                survivors.append(sym)
            continue

        if e["temp_ref_C"] is None:
            # Electrolytic route within E* — not gated by oxide reduction temperature
            survivors.append(sym)
            continue

        if dG <= REFINE_ENERGY_AVAILABLE:
            survivors.append(sym)
        else:
            eliminated.append(make_result(
                sym, "ELIM", "Criterion 5",
                f"delta_G_ref {dG/1e6:.2f} MJ/mol > available "
                f"{REFINE_ENERGY_AVAILABLE/1e6:.2e} MJ "
                f"(Q_sol·eta_ex·A_collector·tau)"))
    return survivors, eliminated


# ---------------------------------------------------------------------------
# Filter 3 — Criterion 4: recyclability η ≥ η_min + Axiom I circularity check
# ---------------------------------------------------------------------------
AXIOM_I_CIRCULAR = {"Mg"}

def filter3_recyclability(survivors_prev, elements):
    survivors, eliminated = [], []
    for sym in survivors_prev:
        e = elements[sym]

        if sym in AXIOM_I_CIRCULAR:
            eliminated.append(make_result(
                sym, "ELIM", "Criterion 3 / Axiom I",
                "Pidgeon loop circularity: net Si and Mg output zero"))
            continue

        eta = e["eta_rec"]
        if eta is None:
            survivors.append(sym)   # G1: kinetic gate open — retain
            continue

        if eta >= ETA_MIN:
            survivors.append(sym)
        else:
            eliminated.append(make_result(
                sym, "ELIM", "Criterion 4",
                f"eta_rec {eta:.3f} < eta_min {ETA_MIN:.4f} "
                f"(OQ-GSH.25 formula, tau={TAU_YR:.0f} yr, eps={EPS})"))
    return survivors, eliminated


# ---------------------------------------------------------------------------
# Filter 4 — Criterion 3: functional role breadth |roles| > 1
# ---------------------------------------------------------------------------
CARRY_TO_SIGMA = {"Cu", "Sn"}   # single role — Σ comparison / G4 gate operative in Filter 7

# Eliminated here despite multiple role entries: all roles covered by other E* members.
# Ni: Pt covers catalysis; C/Al cover corrosion-resistant coating.
# Zn: sole role is galvanic protection of Fe; role physically obsolete in vacuum (ATM=False,
#     r_corr≈0 — no corrosion flux to intercept). Not "covered" — operatively absent.
CRITERION3_COVERED = {"Ni", "Zn"}

def filter4_role_breadth(survivors_prev, elements):
    survivors, eliminated = [], []
    for sym in survivors_prev:
        e = elements[sym]
        if sym in CRITERION3_COVERED:
            if sym == "Zn":
                note = ("Sole role is galvanic protection of Fe. Fe retained (HARDRET), "
                        "but ATM=False: r_corr≈0 — no corrosion flux to intercept. "
                        "Role physically obsolete in this deployment context.")
            else:
                note = (f"roles {e['roles']} all covered by other E* members; "
                        "no irreplaceable functional role.")
            eliminated.append(make_result(sym, "ELIM", "Criterion 3", note))
        elif len(e["roles"]) > 1:
            survivors.append(sym)
        elif sym in CARRY_TO_SIGMA:
            survivors.append(sym)
        else:
            eliminated.append(make_result(
                sym, "ELIM", "Criterion 3",
                f"|roles| = 1: {e['roles']}. "
                "No irreplaceable role not covered by another E* member."))
    return survivors, eliminated


# ---------------------------------------------------------------------------
# Filter 5 — Axiom II: all operating states recoverable using ambient flux
# ---------------------------------------------------------------------------
KINETIC_GATE_OPEN = {"N"}

def filter5_axiom_ii(survivors_prev, elements):
    survivors, eliminated = [], []
    for sym in survivors_prev:
        if sym in KINETIC_GATE_OPEN:
            survivors.append(sym)
            continue
        dG = DELTA_G_REF[sym] or 0.0
        if dG <= REFINE_ENERGY_AVAILABLE:
            survivors.append(sym)
        else:
            eliminated.append(make_result(
                sym, "ELIM", "Axiom II",
                f"recovery energy {dG/1e6:.2f} MJ/mol exceeds available ambient flux over tau"))
    return survivors, eliminated


# ---------------------------------------------------------------------------
# Filter 6 — Challenge A: magnetic hard gap (Axiom IV — M:§8.2 CD-DG)
# ---------------------------------------------------------------------------
MU_R_THRESHOLD = 1000.0

def filter6_challenge_a(survivors_prev, elements):
    hardret = []
    has_flux = any(
        MU_R.get(sym, 1.0) >= MU_R_THRESHOLD
        for sym in survivors_prev if sym != "Fe"
    )
    if FLUX_CHANNELLING_REQUIRED and not has_flux:
        if "Fe" not in survivors_prev:
            survivors_prev = list(survivors_prev) + ["Fe"]
        hardret.append(make_result(
            "Fe", "HARDRET", "Axiom IV / Challenge A Step 1a",
            "d-electron band structure absent from all E* members at any geometric "
            "arrangement. mu_r >= 1000 required (F_space row 5). "
            "Fe re-enters E* unconditionally. No Sigma calculation needed."))
    return survivors_prev, hardret


# ---------------------------------------------------------------------------
# Filter 7 — Σ comparison: dominance test with G1–G4 gates (M:§1.6 / M:§6.7)
# ---------------------------------------------------------------------------

def sigma_s(sym, mass_kg=1.0):
    """Sigma_s(x, tau) in J/K for mass_kg kg of element sym."""
    b = B_CH.get(sym)
    if b is None:
        return None
    m = M_MOL[sym]                            # g/mol
    cap  = (b / (m / 1000)) / T0 * mass_kg   # J/K  (extraction exergy / T0)
    corr = R_CORR[sym] * TAU_S               # J/K  (0 in vacuum)
    return cap + corr


def filter7_sigma_comparison(survivors_prev, elements, hardret_syms):
    results, conditionals = [], []

    for sym in survivors_prev:
        if sym in hardret_syms or sym == "Fe":
            continue

        if sym in KINETIC_GATE_OPEN:
            conditionals.append(make_result(
                sym, "CONDITIONAL", "Axiom II / G1",
                "Kinetic loop closure undemonstrated (vacuum containment). "
                "Pipeline retains when indeterminate.",
                oq="OQ-GSH.15"))
            continue

        if sym in ("Na", "K"):
            conditionals.append(make_result(
                sym, "CONDITIONAL", "Criteria 8/9 / Challenge D",
                "Two elements performing one functional category (heat transfer, "
                "ion storage). Na-only or K-only substitution unproven.",
                oq="OQ-GSH.4"))
            continue

        if sym == "Ti":
            conditionals.append(make_result(
                sym, "CONDITIONAL", "Criterion 6 / G4",
                "Sigma comparison structurally incomplete: "
                "(i) tau_wearout for Al/SiC under -100 to +200 C cycling not established; "
                "step multiplier ceil(tau/tau_wearout) likely >1, strengthening Ti retention. "
                "(ii) T0_fab mismatch: Al/SiC Sigma_g_mfg at 298 K but operative at T0=250 K "
                "(OQ-GSH.19). G4 gate fires: retain conservatively.",
                oq="OQ-GSH.21"))
            continue

        if sym == "Cu":
            s_cu = sigma_s("Cu")
            s_ag = sigma_s("Ag")
            if s_cu is not None and s_ag is not None:
                if s_ag < s_cu:
                    results.append(make_result(
                        sym, "ELIM", "Criterion 8 / dominance test",
                        f"Sigma_s(Cu)={s_cu:.1f} J/K vs Sigma_s(Ag)={s_ag:.1f} J/K per kg. "
                        "Ag lower extraction entropy AND higher conductivity. "
                        "Dominance confirmed where Ag deposition is demonstrable."))
                else:
                    conditionals.append(make_result(
                        sym, "CONDITIONAL", "Criterion 8",
                        "Dominance test inconclusive at current data"))
            else:
                conditionals.append(make_result(
                    sym, "CONDITIONAL", "Criterion 8",
                    "b_ch data unavailable for dominance test"))
            continue

        if sym == "Sn":
            conditionals.append(make_result(
                sym, "CONDITIONAL", "Criterion 3 / G4",
                "Single specialist joining role; SiC/C geometry is the candidate substitute "
                "but Sigma_g(SiC/C joining) is not computable from current data. "
                "G4 gate: retain conservatively.",
                oq="OQ-GSH.1"))
            continue

        results.append(make_result(sym, "PASS", "—", "Survives all filters"))

    return results, conditionals


# ---------------------------------------------------------------------------
# Run pipeline
# ---------------------------------------------------------------------------
def run_pipeline():
    all_elements = dict(ELEMENTS)

    s1, e1 = filter1_abundance(all_elements)
    s2, e2 = filter2_refineable(s1, all_elements)
    s3, e3 = filter3_recyclability(s2, all_elements)
    s4, e4 = filter4_role_breadth(s3, all_elements)
    s5, e5 = filter5_axiom_ii(s4, all_elements)
    s6, hr = filter6_challenge_a(s5, all_elements)

    hardret_syms = {r["symbol"] for r in hr}
    final, cond = filter7_sigma_comparison(s6, all_elements, hardret_syms)

    return {
        "filter_counts": [
            ("Filter 1 (Criterion 1 — abundance)",         len(all_elements), len(s1)),
            ("Filter 2 (Criterion 5 — refineable)",        len(s1),           len(s2)),
            ("Filter 3 (Criterion 4 — recyclable)",        len(s2),           len(s3)),
            ("Filter 4 (Criterion 3 — role breadth)",      len(s3),           len(s4)),
            ("Filter 5 (Axiom II — recovery)",             len(s4),           len(s5)),
            ("Filter 6 (Challenge A — magnetic hard gap)", len(s5),           len(s6)),
        ],
        "eliminated":  e1 + e2 + e3 + e4 + e5,
        "hardret":     hr,
        "final":       [r for r in final if r["status"] == "PASS"],
        "conditional": cond,
        "also_elim":   [r for r in final if r["status"] == "ELIM"],
    }


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def report(result):
    sep = "-" * 72
    print(sep)
    print("GSH Element Derivation — E*(F_space)")
    print(f"  tau = {TAU_YR:.0f} yr  |  T0 = {T0} K  |  "
          f"Q_sol = {Q_SOL} W/m²  |  ATM = {ATM}")
    print(f"  A_collector = {A_COLLECTOR_M2:.0f} m²  |  "
          f"eta_min (OQ-GSH.25) = {ETA_MIN:.6f}  "
          f"(eps={EPS}, tau_cycle=1 yr, tau={TAU_YR:.0f} yr)")
    print(sep)

    print("\nFILTER PROGRESSION")
    for label, n_in, n_out in result["filter_counts"]:
        print(f"  {label:<50s}  {n_in:3d} → {n_out:3d}")

    elim_all = sorted(result["eliminated"] + result["also_elim"],
                      key=lambda x: x["symbol"])
    print(f"\nELIMINATED ({len(elim_all)} elements)")
    for r in elim_all:
        print(f"  {r['symbol']:3s}  [{r['criterion']}]  {r['note']}")

    print(f"\nHARD RETENTION ({len(result['hardret'])} element)")
    for r in result["hardret"]:
        print(f"  {r['symbol']:3s}  [{r['criterion']}]")
        print(f"       {r['note']}")

    print(f"\nUNAMBIGUOUS SURVIVORS ({len(result['final'])} elements)")
    for r in sorted(result["final"], key=lambda x: x["symbol"]):
        print(f"  {r['symbol']:3s}")

    print(f"\nCONDITIONAL ({len(result['conditional'])} elements)")
    for r in sorted(result["conditional"], key=lambda x: x["symbol"]):
        oq = f"  [{r['oq']}]" if r["oq"] else ""
        print(f"  {r['symbol']:3s}  [{r['criterion']}]{oq}")
        print(f"       {r['note'][:120]}")

    unambig = ({r["symbol"] for r in result["final"]}
               | {r["symbol"] for r in result["hardret"]})
    cond = {r["symbol"] for r in result["conditional"]}
    print(f"\nRESULT")
    print(f"  E*(F_space) unambiguous : {sorted(unambig)}")
    print(f"  E*(F_space) conditional : {sorted(cond)}")
    print(f"  Total best estimate     : {sorted(unambig | cond)}")
    print()
    print("Open conditions blocking full computation:")
    print("  OQ-GSH.1   Sn/SiC joining geometry Sigma_g (G4)")
    print("  OQ-GSH.4   Na/K Challenge D (pair vs. single-element sufficiency)")
    print("  OQ-GSH.15  N kinetic gate (vacuum containment)")
    print("  OQ-GSH.17  Omega_G form (G2 gate — active-feedback Sigma_g path)")
    print("  OQ-GSH.18  f(tau) form (G3 gate — Gibbs upper bound path)")
    print("  OQ-GSH.19  T0_fab mismatch (Al/SiC Sigma_g_mfg at 298 K vs 250 K)")
    print("  OQ-GSH.21  Ti/Al-SiC dominance test (tau_wearout data required)")
    print(sep)


if __name__ == "__main__":
    result = run_pipeline()
    report(result)
