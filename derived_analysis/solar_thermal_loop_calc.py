"""
Solar thermal loop analysis — numeric calculator

Authoritative source for all numeric values in solar_thermal_loop_analysis.md
§4.4, §4.8, and §4.11. Numbers in the document are read from here, not the
other way round.

All arithmetic uses sympy exact rationals.  No floating-point
accumulation.  .evalf() is called only at the print layer.

Calculation coverage:
    §4.4  Conversion efficiency cascade (η_Carnot, η_cascade)
    §4.7  Round-trip efficiencies (5 storage forms) and full-chain η products (5 paths)
    §4.8  Geographic DNI scaling (A_required, Σg multiplier per location)
    §4.11 Tucson worked trace — all eight steps:
          aperture area, Al mass, Σg_mfg^CPC, buffer volume, tank Al mass,
          Σg_mfg^storage, Σg_mfg^terminal, Σg^full, Σs^annual, τ*, margin

NOT computed here (open conditions or not a pipeline):
    §4.9  τ_eff integral — λ_d is a site-specific external input
    §4.4  NaAlH₄/T2 crossover τ* — Ti catalyst quantity unspecified (T2 open)
    §1.0  C1 Q_conv = h·A·ΔT — single-equation physics, not a pipeline
    §1.3  T0 correction factor 298/250 — named scalar constant

Run: python3 solar_thermal_loop_calc.py
"""

from __future__ import annotations
from sympy import Rational, Integer


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def R(numerator, denominator=1):
    return Rational(numerator, denominator)


def _sep(title: str) -> None:
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def _row(label: str, value, unit: str = "", sigfig: int = 4) -> None:
    v = value.evalf(sigfig) if hasattr(value, "evalf") else value
    print(f"  {label:<52s}  {v}  {unit}")


# ---------------------------------------------------------------------------
# Layer 0 — deployment-fixed inputs (SI throughout)
# Physical sources noted per value.
# ---------------------------------------------------------------------------

# Energy demand and location
E_DEMAND_KWH   = R(8000)           # kWh/yr — EU average household thermal demand
DNI_REF        = R(2000)           # kWh/m²/yr — subtropical reference for multiplier table

# Efficiency parameters — mid-range from published ranges in §4.4 / §4.7
ETA_OPT        = R(7, 10)          # 0.70 — CPC optical efficiency
ETA_ORC_MID    = R(15, 100)        # 0.15 — ORC at T1 temperatures
ETA_ELEC       = R(68, 100)        # 0.68 — alkaline electrolyser (HHV basis)

# Heat engine temperatures for Carnot bound (§4.4)
T_HOT_K        = R(535)            # K — T1 output (~262 °C)
T_COLD_K       = R(298)            # K — ambient

# Fabrication reference temperature (Gutowski 2009 basis)
T0_FAB_K       = R(298)            # K

# Aluminium material properties
RHO_AL         = R(2700)           # kg/m³ — density
T_SHEET_M      = R(15, 10000)      # m  — 1.5 mm reflector sheet
AL_FRAME_MULT  = R(3)              # total Al ≈ 3× reflector mass (reflector + tube + frame)

# Gutowski (2009) — irreversible work for Al sheet metal forming, mid-range
W_FORMING_J_PER_KG = R(2_000_000) # J/kg

# Thermal storage parameters (§4.11 case: pressurised water at 80 °C)
T_STORAGE_C    = R(80)             # °C
T_AMB_C        = R(25)             # °C — ambient baseline
BUFFER_HOURS   = R(14)             # hours of daily demand the buffer must cover
# Sensible heat density of water: 0.01162 kWh per litre per 10 K rise (standard value)
# V_tank is computed for display only — sigma_g_storage uses static TANK_SURFACE_M2 below
ENERGY_DENSITY_KWH_PER_L_PER_10K = R(116, 10000)

# Storage vessel geometry (§4.11 case: ~200 L cylinder, stated assumption — not derived from V_tank)
TANK_SURFACE_M2 = R(15, 100)       # m² — outer surface area
TANK_WALL_M     = R(2, 1000)       # m  — 2 mm wall

# Fossil boiler reference for Σs (natural gas, §4.11)
ETA_BOILER     = R(85, 100)        # 0.85 efficiency
T_FLAME_K      = R(1700)           # K  — adiabatic flame temperature

# System lifetime bounds for dominance margin (§4.5)
TAU_LIFE_MIN_YR = R(10)            # yr — coated system lower bound
TAU_LIFE_MAX_YR = R(50)            # yr — bare-Al upper bound

# Round-trip efficiency components (§4.7 Node 4 table)
ETA_THERMAL_CHG  = R(95, 100)      # pressurised water charge
ETA_THERMAL_DIS  = R(90, 100)      # pressurised water discharge
ETA_NAALH4_CHG   = R(80, 100)      # NaAlH₄ — electrolyser + compression
ETA_NAALH4_DIS   = R(70, 100)      # NaAlH₄ — dehydriding + gas handling
ETA_NAION_CHG    = R(92, 100)      # Na-ion battery — charge
ETA_NAION_DIS    = R(92, 100)      # Na-ion battery — discharge
ETA_PHYD_CHG     = R(80, 100)      # pumped hydro — pump
ETA_PHYD_DIS     = R(85, 100)      # pumped hydro — turbine
ETA_NH3_CHG      = R(60, 100)      # NH₃ — Haber-Bosch synthesis
ETA_NH3_DIS      = R(75, 100)      # NH₃ — cracking at 450 °C

# End-use terminal and full-chain efficiencies (§4.7 Node 6)
ETA_HX_TERMINAL  = R(95, 100)      # terminal heat exchanger at demand point (Node 6 table)
ETA_MOTOR        = R(90, 100)      # electric motor — mid of 0.85–0.92 (Node 6 table)
ETA_COMBUSTION   = R(90, 100)      # combustion heat recovery — NaAlH₄ terminal path
ETA_TRANS_DIST   = R(93, 100)      # district heating pipe — mid of 0.90–0.95 range

# Location table for §4.8 (NREL NSRDB / literature DNI values)
LOCATIONS = {
    "Atacama":     R(2900),
    "Tucson AZ":   R(2500),
    "Portland OR": R(900),
    "N. Europe":   R(1000),
    "Polar avg":   R(600),
}


# ---------------------------------------------------------------------------
# §4.4  Conversion efficiency cascade
# ---------------------------------------------------------------------------

def section_4_4():
    _sep("§4.4  Conversion efficiency cascade")

    eta_carnot = 1 - T_COLD_K / T_HOT_K
    _row("η_Carnot  (T_hot=535 K, T_cold=298 K)", eta_carnot)

    eta_cascade = ETA_OPT * ETA_ORC_MID * ETA_ELEC
    _row("η_cascade  solar→CPC→ORC→H₂", eta_cascade)

    eta_direct = ETA_OPT
    _row("η_direct   solar→CPC→heat", eta_direct)

    _row("η_direct / η_cascade", eta_direct / eta_cascade)

    return {"eta_carnot": eta_carnot, "eta_cascade": eta_cascade, "eta_direct": eta_direct}


# ---------------------------------------------------------------------------
# §4.7  Round-trip efficiencies and full-chain η products
# ---------------------------------------------------------------------------

def section_4_7():
    _sep("§4.7  Round-trip efficiencies and full-chain η")

    # --- Node 4: RTE table ---
    rtes = [
        ("Pressurised water",      ETA_THERMAL_CHG, ETA_THERMAL_DIS),
        ("NaAlH₄ → H₂",           ETA_NAALH4_CHG,  ETA_NAALH4_DIS),
        ("Na-ion battery",         ETA_NAION_CHG,   ETA_NAION_DIS),
        ("Pumped hydro",           ETA_PHYD_CHG,    ETA_PHYD_DIS),
        ("NH₃ synthesis→cracking", ETA_NH3_CHG,     ETA_NH3_DIS),
    ]
    print("  Node 4 — RTE table:")
    rte_results = {}
    for name, chg, dis in rtes:
        rte = chg * dis
        _row(f"  {name} RTE", rte)
        rte_results[name] = {"chg": chg, "dis": dis, "rte": rte}

    # --- Node 6: full-chain η products ---
    print()
    print("  Full-chain η products (solar flux → end use):")

    # Path 1: Solar → CPC → hot water (co-located, no storage)
    p1 = ETA_OPT * ETA_HX_TERMINAL
    _row("  P1  Solar→CPC→hot water (co-located)", p1)

    # Path 2: Solar → CPC → pressurised storage → hot water
    rte_pw = rte_results["Pressurised water"]["rte"]
    p2 = ETA_OPT * rte_pw * ETA_HX_TERMINAL
    _row("  P2  Solar→CPC→pressurised storage→hot water", p2)

    # Path 3: Solar → CPC → ORC → Na-ion → electric motor
    rte_naion = rte_results["Na-ion battery"]["rte"]
    p3 = ETA_OPT * ETA_ORC_MID * rte_naion * ETA_MOTOR
    _row("  P3  Solar→CPC→ORC→Na-ion→motor", p3)

    # Path 4: Solar → CPC → ORC → electrolysis → NaAlH₄ → H₂ → combustion
    rte_h2 = rte_results["NaAlH₄ → H₂"]["rte"]
    p4 = ETA_OPT * ETA_ORC_MID * ETA_ELEC * rte_h2 * ETA_COMBUSTION
    _row("  P4  Solar→CPC→ORC→electrolysis→NaAlH₄→combustion", p4)

    # Path 5: Solar → CPC → district heating → terminal HX
    p5 = ETA_OPT * ETA_TRANS_DIST * ETA_TRANS_DIST * ETA_HX_TERMINAL
    _row("  P5  Solar→CPC→district heating→terminal HX", p5)

    return {
        "rtes": rte_results,
        "p1": p1, "p2": p2, "p3": p3, "p4": p4, "p5": p5,
    }


# ---------------------------------------------------------------------------
# §4.8  Geographic DNI scaling
# ---------------------------------------------------------------------------

def section_4_8():
    _sep("§4.8  Geographic DNI scaling")

    print(f"  DNI reference: {DNI_REF} kWh/m²/yr"
          f"  |  η_opt = {ETA_OPT}  |  E_demand = {E_DEMAND_KWH} kWh/yr")
    print()
    print(f"  {'Location':<16}  {'DNI (kWh/m²/yr)':>18}  "
          f"{'A_required (m²)':>18}  {'Σg multiplier':>16}")
    print(f"  {'-'*16}  {'-'*18}  {'-'*18}  {'-'*16}")

    results = {}
    for name, dni in LOCATIONS.items():
        a    = E_DEMAND_KWH / (ETA_OPT * dni)
        mult = DNI_REF / dni
        print(f"  {name:<16}  {float(dni):>18.0f}  "
              f"{float(a.evalf(4)):>18.2f}  {float(mult.evalf(4)):>16.3f}")
        results[name] = {"A_m2": a, "sigma_g_mult": mult}

    # Tucson vs Portland comparison (§4.10)
    a_tucson   = results["Tucson AZ"]["A_m2"]
    a_portland = results["Portland OR"]["A_m2"]
    print()
    _row("A_Tucson (m²)",          a_tucson)
    _row("A_Portland (m²)",        a_portland)
    _row("Portland/Tucson Al mass ratio", a_portland / a_tucson)

    # Polar aperture lower bound at DNI = 400 (§4.8 body)
    a_polar_floor = E_DEMAND_KWH / (ETA_OPT * R(400))
    _row("A at DNI=400 polar floor (m²)", a_polar_floor)

    return results


# ---------------------------------------------------------------------------
# §4.11  Tucson household hot water — worked parameter trace
# ---------------------------------------------------------------------------

def section_4_11():
    _sep("§4.11  Tucson worked trace — household hot water")

    # Step 1 — aperture area
    a = E_DEMAND_KWH / (ETA_OPT * LOCATIONS["Tucson AZ"])
    _row("A_required (m²)", a, "m²")

    # Step 2 — Al mass
    m_al_reflector = a * T_SHEET_M * RHO_AL
    m_al_total     = AL_FRAME_MULT * m_al_reflector
    _row("m_Al reflector (kg)", m_al_reflector, "kg")
    _row("m_Al total (kg)", m_al_total, "kg")

    # Step 3 — Σg_mfg^CPC
    w_irrev      = m_al_total * W_FORMING_J_PER_KG   # J
    sigma_g_cpc  = w_irrev / T0_FAB_K                # J/K
    _row("W_irrev_fab (MJ)", w_irrev / R(1_000_000), "MJ")
    _row("Σg_mfg^CPC (kJ/K)", sigma_g_cpc / R(1000), "kJ/K")

    # Step 4 — thermal storage vessel
    e_daily         = E_DEMAND_KWH / R(365)          # kWh/day
    e_buffer        = e_daily * BUFFER_HOURS / R(24) # kWh
    delta_t         = T_STORAGE_C - T_AMB_C          # K
    energy_density  = ENERGY_DENSITY_KWH_PER_L_PER_10K * (delta_t / R(10))  # kWh/L
    v_tank          = e_buffer / energy_density       # litres
    m_al_tank       = TANK_SURFACE_M2 * TANK_WALL_M * RHO_AL  # kg
    sigma_g_storage = m_al_tank * W_FORMING_J_PER_KG / T0_FAB_K  # J/K
    _row("Daily demand (kWh/day)", e_daily, "kWh/day")
    _row("Buffer energy (kWh)", e_buffer, "kWh")
    _row("Storage ΔT (K)", delta_t)
    _row("Energy density (kWh/L)", energy_density, "kWh/L")
    _row("V_tank (litres)", v_tank, "litres")
    _row("m_Al tank (kg)", m_al_tank, "kg")
    _row("Σg_mfg^storage (kJ/K)", sigma_g_storage / R(1000), "kJ/K")

    # Step 5 — terminal heat exchanger
    m_al_hx        = R(1, 2)                          # kg — Al plate HX
    sigma_g_terminal = m_al_hx * W_FORMING_J_PER_KG / T0_FAB_K  # J/K
    _row("m_Al HX (kg)", m_al_hx, "kg")
    _row("Σg_mfg^terminal (kJ/K)", sigma_g_terminal / R(1000), "kJ/K")

    # Step 6 — Σg^full
    sigma_g_full = sigma_g_cpc + sigma_g_storage + sigma_g_terminal
    _row("Σg^full (kJ/K)", sigma_g_full / R(1000), "kJ/K")
    _row("CPC share of Σg^full (%)", sigma_g_cpc / sigma_g_full * 100)

    # Step 7 — Σs^annual (fossil boiler displaced)
    e_demand_j    = E_DEMAND_KWH * R(3_600_000)       # J/yr  (1 kWh = 3.6 MJ)
    sigma_s_annual = e_demand_j / (ETA_BOILER * T_FLAME_K)  # J/K/yr
    _row("Σs^annual (MJ/K/yr)", sigma_s_annual / R(1_000_000), "MJ/K/yr")

    # Step 8 — τ* and dominance margin
    tau_star_yr   = sigma_g_full / sigma_s_annual
    tau_star_days = tau_star_yr * R(365)
    margin_min    = TAU_LIFE_MIN_YR / tau_star_yr
    margin_max    = TAU_LIFE_MAX_YR / tau_star_yr
    _row("τ* (years)", tau_star_yr, "yr")
    _row("τ* (days)", tau_star_days, "days")
    _row("Dominance margin τ_life_min / τ*", margin_min)
    _row("Dominance margin τ_life_max / τ*", margin_max)

    # Structural invariant checks — catch scrambled inputs, not document text
    assert sigma_g_cpc / sigma_g_full > R(95, 100), \
        "CPC must dominate Σg^full (>95%) — check inputs"
    assert tau_star_yr < R(1, 10), \
        "τ* must be well under 0.1 yr for T1 dominance claim to hold"
    assert margin_min > R(100), \
        "Dominance margin must exceed 100× for T1 claim — check inputs"

    return {
        "a_m2":             a,
        "m_al_total_kg":    m_al_total,
        "sigma_g_cpc_JK":   sigma_g_cpc,
        "sigma_g_full_JK":  sigma_g_full,
        "sigma_s_annual_JK": sigma_s_annual,
        "tau_star_yr":      tau_star_yr,
        "tau_star_days":    tau_star_days,
        "margin_min":       margin_min,
        "margin_max":       margin_max,
    }


# ---------------------------------------------------------------------------
# Computed Markdown writer
# Generates solar_thermal_loop_computed.md — transcluded by the analysis.
# Never hand-edit that file; re-run this script instead.
# ---------------------------------------------------------------------------

def f4(v) -> str:
    """4-significant-figure string from a sympy value."""
    return str(v.evalf(4))


def write_computed_md(r44: dict, r47: dict, r48: dict, r411: dict, out_path: str) -> None:
    eta_c  = r44["eta_carnot"]
    eta_ca = r44["eta_cascade"]

    # §4.7 — unpack RTE and path products
    rtes   = r47["rtes"]
    p1, p2, p3, p4, p5 = r47["p1"], r47["p2"], r47["p3"], r47["p4"], r47["p5"]

    # RTE table rows: name, chg, dis, rte, qualitative extraction note
    rte_notes = {
        "Pressurised water":      "Pump and valve wear; no conversion",
        "NaAlH₄ → H₂":           "Dehydriding vessel; gas regulator; Ti catalyst (cycle consumption)",
        "Na-ion battery":         "Cell capacity fade per cycle; no moving parts",
        "Pumped hydro":           "Turbine and pump maintenance; civil structure is passive",
        "NH₃ synthesis→cracking": "Cracking reactor at T2; Fe/K catalyst (borderline $\\mathcal{E}^*$)",
    }

    rte_rows = []
    for name, d in rtes.items():
        chg = f4(d["chg"])
        dis = f4(d["dis"])
        rte = f4(d["rte"])
        note = rte_notes[name]
        rte_rows.append(f"| {name} | {chg} | {dis} | {rte} | {note} |")

    # Full-chain path rows: label, symbolic product, numeric result, dominant loss, storable, E* status
    chain_rows = [
        f"| Solar → CPC → hot water (co-located)"
        f" | ${f4(ETA_OPT)} \\times {f4(ETA_HX_TERMINAL)} = {f4(p1)}$"
        f" | Optical collection | No (diurnal only) | Yes |",

        f"| Solar → CPC → pressurised storage → hot water"
        f" | ${f4(ETA_OPT)} \\times {f4(rtes['Pressurised water']['rte'])} \\times {f4(ETA_HX_TERMINAL)} = {f4(p2)}$"
        f" | Storage standby loss | Diurnal | Yes |",

        f"| Solar → CPC → ORC → Na-ion → electric motor"
        f" | ${f4(ETA_OPT)} \\times {f4(ETA_ORC_MID)} \\times {f4(rtes['Na-ion battery']['rte'])} \\times {f4(ETA_MOTOR)} = {f4(p3)}$"
        f" | Carnot at T1 | Yes | Candidate |",

        f"| Solar → CPC → ORC → electrolysis → NaAlH₄ → H₂ → combustion"
        f" | ${f4(ETA_OPT)} \\times {f4(ETA_ORC_MID)} \\times {f4(ETA_ELEC)} \\times {f4(rtes['NaAlH₄ → H₂']['rte'])} \\times {f4(ETA_COMBUSTION)} = {f4(p4)}$"
        f" | Carnot + RTE | Diurnal–seasonal | Candidate (Ti gate) |",

        f"| Solar → CPC → district heating → terminal HX"
        f" | ${f4(ETA_OPT)} \\times {f4(ETA_TRANS_DIST)}^2 \\times {f4(ETA_HX_TERMINAL)} = {f4(p5)}$"
        f" | Distribution standby | Diurnal (pressurised) | Yes (pipe material borderline) |",
    ]

    # §4.8 — polar floor and location table
    a_polar_floor = E_DEMAND_KWH / (ETA_OPT * R(400))

    # Build location rows: name, DNI, A_required, Σg multiplier
    loc_rows = []
    for name, dni in LOCATIONS.items():
        a    = r48[name]["A_m2"]
        mult = r48[name]["sigma_g_mult"]
        loc_rows.append(
            f"| {name} | {int(dni)} | {f4(a)} | {f4(mult)} |"
        )

    # §4.11 — unpack results and recompute intermediate values for display
    a          = r411["a_m2"]
    m_al       = r411["m_al_total_kg"]
    sg_cpc     = r411["sigma_g_cpc_JK"]
    sg_full    = r411["sigma_g_full_JK"]
    ss_ann     = r411["sigma_s_annual_JK"]
    tau_yr     = r411["tau_star_yr"]
    tau_days   = r411["tau_star_days"]
    margin_min = r411["margin_min"]
    margin_max = r411["margin_max"]

    m_al_reflector = a * T_SHEET_M * RHO_AL
    w_irrev        = m_al * W_FORMING_J_PER_KG
    e_daily        = E_DEMAND_KWH / R(365)
    e_buffer       = e_daily * BUFFER_HOURS / R(24)
    delta_t        = T_STORAGE_C - T_AMB_C
    energy_density = ENERGY_DENSITY_KWH_PER_L_PER_10K * (delta_t / R(10))
    v_tank         = e_buffer / energy_density
    m_al_tank      = TANK_SURFACE_M2 * TANK_WALL_M * RHO_AL
    sg_storage     = m_al_tank * W_FORMING_J_PER_KG / T0_FAB_K
    m_al_hx        = R(1, 2)
    sg_terminal    = m_al_hx * W_FORMING_J_PER_KG / T0_FAB_K
    cpc_share      = sg_cpc / sg_full * 100

    lines = [
        "---",
        "unlisted: true",
        "---",
        "",
        "<!-- Generated by solar_thermal_loop_calc.py — do not edit by hand -->",
        "",
        "## Cascade efficiency",
        "",
        f"$$\\eta_\\text{{Carnot}}^{{T1}} = 1 - \\frac{{{int(T_COLD_K)}}}{{{int(T_HOT_K)}}} = {f4(eta_c)}$$",
        "",
        f"$$\\eta_\\text{{cascade}} = \\eta_\\text{{opt}} \\cdot \\eta_\\text{{ORC}} \\cdot \\eta_\\text{{elec}}"
        f" = {f4(ETA_OPT)} \\times {f4(ETA_ORC_MID)} \\times {f4(ETA_ELEC)}"
        f" = {f4(eta_ca)}$$",
        "",
        "## Round-trip efficiencies",
        "",
        "| Storage form | $\\eta_\\text{chg}$ | $\\eta_\\text{dis}$ | RTE | Extraction $\\Sigma_g$ terms |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ] + rte_rows + [
        "",
        "## Full chain efficiency",
        "",
        "| Path | $\\eta$ product | Dominant loss step | Storable? | $\\mathcal{E}^*$ confirmed? |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ] + chain_rows + [
        "",
        "## Geographic DNI scaling",
        "",
        f"Reference DNI: {int(DNI_REF)} kWh/m²/yr  |  "
        f"$\\eta_\\text{{opt}}$ = {f4(ETA_OPT)}  |  "
        f"$E_\\text{{demand}}$ = {int(E_DEMAND_KWH)} kWh/yr",
        "",
        "| Location | DNI (kWh/m²/yr) | $A_\\text{required}$ (m²) | $\\Sigma_g$ multiplier |",
        "| :--- | ---: | ---: | ---: |",
    ] + loc_rows + [
        "",
        f"Polar floor ($\\text{{DNI}} = 400$ kWh/m²/yr): "
        f"$A = {f4(a_polar_floor)}$ m²",
        "",
        "## Location comparison apertures",
        "",
    ] + [
        f"| Location | DNI (kWh/m²/yr) | $A_\\text{{required}}$ (m²) | $\\Sigma_g$ multiplier vs ref |",
        "| :--- | ---: | ---: | ---: |",
        f"| Tucson AZ | {int(LOCATIONS['Tucson AZ'])} | {f4(r48['Tucson AZ']['A_m2'])} | {f4(r48['Tucson AZ']['sigma_g_mult'])} |",
        f"| Portland OR | {int(LOCATIONS['Portland OR'])} | {f4(r48['Portland OR']['A_m2'])} | {f4(r48['Portland OR']['sigma_g_mult'])} |",
        "",
        f"Portland/Tucson aperture ratio: "
        f"${f4(r48['Portland OR']['A_m2'] / r48['Tucson AZ']['A_m2'])}\\times$",
        "",
        "## Tucson worked trace",
        "",
        f"**Step 1 — Aperture area**",
        "",
        f"$$A = \\frac{{{int(E_DEMAND_KWH)}}}{{{f4(ETA_OPT)} \\times {int(LOCATIONS['Tucson AZ'])}}} = {f4(a)}\\ \\text{{m}}^2$$",
        "",
        f"**Step 2 — Al mass**",
        "",
        f"$$m_\\text{{Al,reflector}} = {f4(a)} \\times {float(T_SHEET_M)} \\times {int(RHO_AL)} = {f4(m_al_reflector)}\\ \\text{{kg}}$$",
        "",
        f"$$m_\\text{{Al,total}} = {int(AL_FRAME_MULT)} \\times {f4(m_al_reflector)} = {f4(m_al)}\\ \\text{{kg}}$$",
        "",
        f"**Step 3 — $\\Sigma_{{g,\\text{{mfg}}}}^{{\\text{{CPC}}}}$**",
        "",
        f"$$W_\\text{{irrev,fab}} = {f4(m_al)}\\ \\text{{kg}} \\times {int(W_FORMING_J_PER_KG / R(1_000_000))}\\ \\text{{MJ/kg}} = {f4(w_irrev / R(1_000_000))}\\ \\text{{MJ}}$$",
        "",
        f"$$\\Sigma_{{g,\\text{{mfg}}}}^{{\\text{{CPC}}}} = \\frac{{{f4(w_irrev / R(1_000_000))} \\times 10^6}}{{{int(T0_FAB_K)}}} = {f4(sg_cpc / R(1000))}\\ \\text{{kJ/K}}$$",
        "",
        f"**Step 4 — Storage vessel**",
        "",
        f"Daily demand: ${f4(e_daily)}$ kWh/day. "
        f"Buffer ({int(BUFFER_HOURS)} hr): ${f4(e_buffer)}$ kWh. "
        f"$\\Delta T = {int(delta_t)}$ K. "
        f"Energy density $= {f4(energy_density)}$ kWh/litre.",
        "",
        f"$$V_\\text{{tank}} = \\frac{{{f4(e_buffer)}}}{{{f4(energy_density)}}} = {f4(v_tank)}\\ \\text{{litres}}$$",
        "",
        f"$$m_\\text{{Al,tank}} = {float(TANK_SURFACE_M2)}\\ \\text{{m}}^2 \\times {float(TANK_WALL_M)}\\ \\text{{m}} \\times {int(RHO_AL)} = {f4(m_al_tank)}\\ \\text{{kg}}$$",
        "",
        f"$$\\Sigma_{{g,\\text{{mfg}}}}^{{\\text{{storage}}}} = {f4(sg_storage / R(1000))}\\ \\text{{kJ/K}}$$",
        "",
        f"**Step 5 — Terminal heat exchanger**",
        "",
        f"$$\\Sigma_{{g,\\text{{mfg}}}}^{{\\text{{terminal}}}} = "
        f"\\frac{{{float(m_al_hx)}\\ \\text{{kg}} \\times {int(W_FORMING_J_PER_KG / R(1_000_000))}\\ \\text{{MJ/kg}} \\times 10^6}}{{{int(T0_FAB_K)}}} = {f4(sg_terminal / R(1000))}\\ \\text{{kJ/K}}$$",
        "",
        f"**Step 6 — Full chain $\\Sigma_g^{{\\text{{full}}}}$**",
        "",
        f"$$\\Sigma_g^{{\\text{{full}}}} = {f4(sg_cpc / R(1000))} + {f4(sg_storage / R(1000))} + {f4(sg_terminal / R(1000))} = {f4(sg_full / R(1000))}\\ \\text{{kJ/K}}$$",
        "",
        f"CPC term: {f4(cpc_share)}% of total.",
        "",
        f"**Step 7 — $\\Sigma_s^{{\\text{{annual}}}}$ and $\\tau^*$**",
        "",
        f"$$\\Sigma_s^{{\\text{{annual}}}} = \\frac{{{int(E_DEMAND_KWH)} \\times 3.6 \\times 10^6}}"
        f"{{{float(ETA_BOILER)} \\times {int(T_FLAME_K)}}} = {f4(ss_ann / R(1_000_000))}\\ \\text{{MJ/K/yr}}$$",
        "",
        f"$$\\tau^* = \\frac{{{f4(sg_full / R(1000))}\\ \\text{{kJ/K}}}}"
        f"{{{f4(ss_ann / R(1_000_000))}\\ \\text{{MJ/K/yr}}}} = {f4(tau_yr)}\\ \\text{{yr}} = {f4(tau_days)}\\ \\text{{days}}$$",
        "",
        f"Dominance margin: ${f4(margin_min)}\\times$ ({int(TAU_LIFE_MIN_YR)} yr) — "
        f"${f4(margin_max)}\\times$ ({int(TAU_LIFE_MAX_YR)} yr).",
        "",
    ]

    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"\nWrote {out_path}")


# ---------------------------------------------------------------------------
# Open conditions — scope boundary
# ---------------------------------------------------------------------------

def report_open_conditions():
    _sep("Open conditions (not computed here)")
    for ref, reason in [
        ("§4.9  τ_eff integral",
         "λ_d is a site-specific external input, not a formula property"),
        ("§4.4  NaAlH₄/T2 crossover τ*",
         "Ti catalyst quantity per kg H₂ capacity unspecified (T2 open)"),
        ("§1.0  C1 Q_conv = h·A·ΔT",
         "Single-equation physics — not a pipeline"),
        ("§1.3  T0 correction 298/250",
         "Named scalar constant"),
    ]:
        print(f"  {ref}")
        print(f"      {reason}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import os
    print("solar_thermal_loop_calc.py")
    print("Arithmetic: sympy exact rational")

    r44  = section_4_4()
    r47  = section_4_7()
    r48  = section_4_8()
    r411 = section_4_11()
    report_open_conditions()

    _sep("RESULT SUMMARY")
    print(f"  η_Carnot                    {r44['eta_carnot'].evalf(4)}")
    print(f"  η_cascade (solar→H₂)        {r44['eta_cascade'].evalf(4)}")
    print(f"  η_direct  (solar→heat)      {r44['eta_direct'].evalf(4)}")
    print()
    print(f"  RTE pressurised water       {r47['rtes']['Pressurised water']['rte'].evalf(4)}")
    print(f"  RTE NaAlH₄                  {r47['rtes']['NaAlH₄ → H₂']['rte'].evalf(4)}")
    print(f"  RTE Na-ion                  {r47['rtes']['Na-ion battery']['rte'].evalf(4)}")
    print(f"  RTE pumped hydro            {r47['rtes']['Pumped hydro']['rte'].evalf(4)}")
    print(f"  RTE NH₃                     {r47['rtes']['NH₃ synthesis→cracking']['rte'].evalf(4)}")
    print()
    print(f"  P1 chain η (direct heat)    {r47['p1'].evalf(4)}")
    print(f"  P2 chain η (pressurised)    {r47['p2'].evalf(4)}")
    print(f"  P3 chain η (ORC→Na-ion)     {r47['p3'].evalf(4)}")
    print(f"  P4 chain η (ORC→H₂)         {r47['p4'].evalf(4)}")
    print(f"  P5 chain η (district)       {r47['p5'].evalf(4)}")
    print()
    print(f"  Tucson A_required (m²)      {r411['a_m2'].evalf(4)}")
    print(f"  Al mass total (kg)          {r411['m_al_total_kg'].evalf(4)}")
    print(f"  Σg_mfg^CPC (kJ/K)           {(r411['sigma_g_cpc_JK']/1000).evalf(4)}")
    print(f"  Σg^full (kJ/K)              {(r411['sigma_g_full_JK']/1000).evalf(4)}")
    print(f"  Σs^annual (MJ/K/yr)         {(r411['sigma_s_annual_JK']/1e6).evalf(4)}")
    print(f"  τ* (days)                   {r411['tau_star_days'].evalf(4)}")
    print(f"  Dominance margin (×)        {r411['margin_min'].evalf(4)} – {r411['margin_max'].evalf(4)}")
    print()
    print("Structural invariants: passed.")

    out = os.path.join(os.path.dirname(__file__), "solar_thermal_loop_computed.md")
    write_computed_md(r44, r47, r48, r411, out)
