"""
Fe/Al τ* crossover — numeric data scaffold (OQ-GSH.8).

Populates check 7's crossover formula with real supply-chain data for the
Fe (incumbent) vs. Al geometric substitute comparison.

Source mapping to check 7 parameters:
    Σ_cap_s = extraction exergy of Fe + deferred Axiom II recovery cost
    Σ_cap_g = extraction exergy of Al geometric substitute
    sigma_dot_s = ongoing entropy rate of Fe supply chain (corrosion-dominated); r_s in code
    sigma_dot_g = ongoing maintenance entropy rate of Al substitute (≈ 0, self-passivating); r_g in code

Data sources:
    Szargut (1988) standard chemical exergies — b_ch values below
    NIST WebBook — ΔG_oxidation values
    ISO 9223 / atmospheric corrosion literature — r_corr representative values

API readiness:
    mp-api (Materials Project) can replace Szargut b_ch values with computed
    formation energies and elastic tensors for the Σ_g maintenance floor.
    CoolProp is not applicable here — solid-state supply chains, not fluid cycles.
    Replace the SZARGUT_* constants below with mp-api query results when available.

Run: python3 fe_crossover_numeric.py
"""

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
T0 = 298.15          # K  — standard dead-state reference temperature
R  = 8.314           # J/(mol·K)

# ---------------------------------------------------------------------------
# Szargut (1988) standard chemical exergies — J/mol
# b_ch is the exergy of a pure substance relative to the reference environment.
# These are the B_s supply-chain cost inputs before conversion to entropy (J/K).
# Replace with mp-api computed values when available.
# ---------------------------------------------------------------------------
SZARGUT_B_CH = {
    "Fe": 376_400,   # J/mol  — Szargut 1988, Table A.1
    "Al": 888_400,   # J/mol  — Szargut 1988, Table A.1
    "C":  410_260,   # J/mol  — graphite reference state
    "Si": 854_600,   # J/mol
    "H":   236_100,  # J/mol  — H₂ gas
    "O":    3_970,   # J/mol  — O₂ gas (reference species, low exergy)
}

# ---------------------------------------------------------------------------
# Molar masses — g/mol
# ---------------------------------------------------------------------------
M = {
    "Fe": 55.845,
    "Al": 26.982,
    "C":  12.011,
    "O":  15.999,
}

# ---------------------------------------------------------------------------
# Reaction thermodynamics at 298K — J/mol (NIST WebBook)
# ---------------------------------------------------------------------------
DG_OXIDATION_FE = -742_200    # J/mol Fe₂O₃  — standard Gibbs free energy of formation
                               # Reaction: 2Fe(s) + 1.5O₂(g) → Fe₂O₃(s)  (ΔfG° per mol Fe₂O₃)
                               # Per mole Fe: -742200 / 2 = -371100 J/mol Fe
DG_OXIDATION_FE_PER_MOL = DG_OXIDATION_FE / 2   # J/mol Fe

DG_REDUCTION_FE2O3 = +742_200 # J/mol — reverse reaction (Axiom II recovery cost)
DG_REDUCTION_FE_PER_MOL = DG_REDUCTION_FE2O3 / 2  # J/mol Fe

# ---------------------------------------------------------------------------
# Corrosion rate → entropy rate conversion
#
# The math spec (§3.1, OQ-GSH.8) requires r_corr·τ to have units J/K.
# Conversion chain:
#   corr_rate [m/s] × ρ_Fe [kg/m³] → mass flux [kg/(m²·s)]
#   mass flux / M_Fe [kg/mol]       → molar flux [mol/(m²·s)]
#   molar flux × |ΔG_ox| [J/mol]   → power dissipated [W/m²]
#   power / T0 [K]                  → entropy rate [W/(K·m²)]
#   × surface_area [m²]            → r_s [W/K]
#
# This instantiates the unresolved condition in GSH_mathematical_inventory.md §3.1.
#
# For treated iron, CORR_UM_YR should be replaced by the effective entropy rate
# of the protection system:
#   - ICCP (impressed current cathodic protection): r_s = W_electrical / T0,
#     where W_electrical is the continuous power draw of the protection circuit.
#     Axiom III compliance must be checked — the power source must be ambient flux.
#   - Sacrificial Mg anodes: r_s ≈ Σ_s(Mg) × f_replacement, where f_replacement
#     is the anode replacement frequency. Axiom II compliance of Mg corrosion
#     products (MgO, Mg(OH)₂) must be verified independently.
#   - Galvanic isolation (geopolymer gaskets): one-time Σ_g manufacturing cost;
#     no ongoing r_s term. Gasket degradation rate in space/radiation context
#     is uncharacterised — see §1.2 r_corr note.
# In all cases the protection system's Axiom II/III compliance is a separate
# evaluation, not inherited from the base iron calculation.
# ---------------------------------------------------------------------------
RHO_FE = 7_874.0   # kg/m³

def r_corr_to_entropy_rate(corr_rate_m_per_s: float, surface_area_m2: float,
                           T0: float = T0) -> float:
    """
    Convert atmospheric corrosion rate (m/s) to entropy generation rate (W/K).

    Parameters
    ----------
    corr_rate_m_per_s : float
        Linear corrosion rate in m/s (e.g. 50 μm/yr = 1.585e-12 m/s).
    surface_area_m2 : float
        Exposed surface area of the Fe structure in m².

    Returns
    -------
    float
        Entropy generation rate r_s in W/K.
    """
    molar_flux = (corr_rate_m_per_s * RHO_FE * 1000) / M["Fe"]  # mol/(m²·s)
    power_per_area = molar_flux * abs(DG_OXIDATION_FE_PER_MOL)   # W/m²
    return (power_per_area * surface_area_m2) / T0                # W/K


# ---------------------------------------------------------------------------
# Supply-chain entropy (Σ_s) — one-time capital terms (J/K per kg of material)
#
# Σ_cap_s per kg Fe:
#   extraction exergy: b_ch(Fe) / M_Fe × 1000 / T0  [J/K per kg]
#   Axiom II recovery cost: ΔG_reduction / M_Fe × 1000 / T0  [J/K per kg]
#
# Σ_cap_g per kg Al substitute:
#   extraction exergy: b_ch(Al) / M_Al × 1000 / T0  [J/K per kg]
#   recycling: Al₂O₃ → Al requires ~30 MJ/kg (Hall-Héroult); carbothermic at T4
#   conditions is the ℰ*-compliant path — cost higher than Hall-Héroult.
#   Using Szargut b_ch(Al) as a conservative lower bound on extraction entropy.
# ---------------------------------------------------------------------------

def sigma_cap_per_kg(element: str, T0: float = T0) -> float:
    """
    Capital supply-chain entropy per kg of element (J/K/kg).
    Extraction exergy from Szargut b_ch, normalised to T0.
    Does not include Axiom II recovery cost — add separately for Fe.
    """
    b_ch = SZARGUT_B_CH[element]        # J/mol
    m    = M[element]                   # g/mol
    return (b_ch / (m / 1000)) / T0     # J/K per kg


def sigma_rec_fe_per_kg(T0: float = T0) -> float:
    """
    Axiom II recovery cost for Fe per kg (J/K/kg).
    Energy to reduce Fe₂O₃ → Fe using ambient flux at decommissioning.
    """
    return (abs(DG_REDUCTION_FE_PER_MOL) / (M["Fe"] / 1000)) / T0  # J/K per kg


# ---------------------------------------------------------------------------
# τ* crossover — numeric instance of check 7 formula
#
# τ* = (Σ_cap_g − Σ_cap_s) / (r_s − r_g)
#
# Inputs for a representative structure (1 tonne Fe / equivalent Al substitute,
# 10 m² exposed surface, rural atmosphere corrosion C2 category):
#
#   C2 atmospheric corrosion rate: ~25–50 μm/yr for carbon steel (ISO 9223)
#   Representative surface area: 10 m² (small structural frame)
#   Default substitution: equal-volume (same geometry, mass scaled by ρ_Al/ρ_Fe ≈ 0.34).
#   r_g(Al) ≈ 0 — Al passivates; ongoing entropy cost negligible in closed-loop.
# ---------------------------------------------------------------------------
MASS_KG    = 1_000.0   # kg — representative Fe structure mass
AREA_M2    =    10.0   # m² — exposed surface area
CORR_UM_YR =    25.0   # μm/yr — ISO 9223 C2 low endpoint (used as default for single-call callers)
# ISO 9223 C2 is defined as a range (25–50 μm/yr); main() propagates both endpoints.

SECONDS_PER_YEAR = 365.25 * 24 * 3600


def crossover_tau_years(
    corr_um_yr: float = CORR_UM_YR,
    al_mass_kg: float = None,
    fe_mass_kg: float = MASS_KG,
    surface_area_m2: float = AREA_M2,
    T0: float = T0,
) -> dict:
    """
    Compute τ* for Fe → Al geometric substitute substitution.

    Parameters
    ----------
    corr_um_yr : float
        Atmospheric corrosion rate for Fe in μm/yr.
    al_mass_kg : float or None
        Mass of Al substitute in kg.  None (default) → equal-volume substitution:
        fe_mass_kg × (ρ_Al / ρ_Fe), the exact geometric replica mass.
        Pass fe_mass_kg explicitly for equal-mass comparison.
    fe_mass_kg : float
        Mass of the Fe structure in kg (default: module-level MASS_KG).
    surface_area_m2 : float
        Exposed surface area of the Fe structure in m² (default: module-level AREA_M2).
    T0 : float
        Dead-state reference temperature in K (default 298.15).

    Returns a dict with all intermediate values and τ* in years.
    """
    RHO_AL = 2_700.0   # kg/m³
    if al_mass_kg is None:
        al_mass_kg = fe_mass_kg * (RHO_AL / RHO_FE)   # equal-volume geometric replica

    corr_m_s = (corr_um_yr * 1e-6) / SECONDS_PER_YEAR  # m/s

    sigma_cap_fe = sigma_cap_per_kg("Fe", T0) * fe_mass_kg     # J/K
    sigma_rec_fe = sigma_rec_fe_per_kg(T0) * fe_mass_kg        # J/K
    sigma_cap_s  = sigma_cap_fe + sigma_rec_fe                 # J/K  (Σ_cap_s)

    sigma_cap_g  = sigma_cap_per_kg("Al", T0) * al_mass_kg     # J/K  (Σ_cap_g)

    r_s = r_corr_to_entropy_rate(corr_m_s, surface_area_m2, T0)    # W/K
    r_g = 0.0                                               # W/K  (Al passivates)

    # τ* = (Σ_cap_g − Σ_cap_s) / (r_s − r_g)
    numerator   = sigma_cap_g - sigma_cap_s
    denominator = r_s - r_g

    if abs(denominator) < 1e-30:
        tau_star_s = float("inf")
    else:
        tau_star_s = numerator / denominator

    tau_star_yr = tau_star_s / SECONDS_PER_YEAR

    return {
        "sigma_cap_Fe_J_per_K":   sigma_cap_fe,
        "sigma_rec_Fe_J_per_K":   sigma_rec_fe,
        "sigma_cap_s_J_per_K":    sigma_cap_s,
        "sigma_cap_g_J_per_K":    sigma_cap_g,
        "r_s_W_per_K":            r_s,
        "r_g_W_per_K":            r_g,
        "tau_star_years":         tau_star_yr,
        "regime": (
            "favourable substitution at τ > τ*"
            if tau_star_yr > 0 else
            "geometry unconditionally cheaper — no crossover needed"
            if (tau_star_yr < 0 and numerator < 0) else
            "geometry unconditionally more expensive — no crossover exists"
            if (tau_star_yr < 0 and numerator > 0) else
            "no crossover"
        ),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    # ISO 9223 C2 interval: 25–50 μm/yr for carbon steel
    C2_LOW, C2_HIGH = 25.0, 50.0

    RHO_AL = 2_700.0
    al_equal_vol = MASS_KG * (RHO_AL / RHO_FE)

    print("Fe → Al geometric substitute τ* crossover (OQ-GSH.8 numeric instance)")
    print(f"  Fe structure: {MASS_KG:.0f} kg, {AREA_M2:.0f} m² exposed surface")
    print(f"  ISO 9223 C2 corrosion range: {C2_LOW:.0f}–{C2_HIGH:.0f} μm/yr")
    print()

    for label, al_kg in [
        (f"equal-volume Al ({al_equal_vol:.0f} kg)", al_equal_vol),
        (f"equal-mass Al ({MASS_KG:.0f} kg)", MASS_KG),
    ]:
        r_low  = crossover_tau_years(C2_LOW,  al_mass_kg=al_kg)
        r_high = crossover_tau_years(C2_HIGH, al_mass_kg=al_kg)
        t_low  = r_low["tau_star_years"]
        t_high = r_high["tau_star_years"]
        # Higher corrosion rate → larger r_s → smaller τ*; swap so interval reads low→high
        if t_low > t_high:
            t_low, t_high = t_high, t_low

        print(f"  {label}")
        print(f"    Σ_cap_s (Fe extraction + recycling): {r_low['sigma_cap_s_J_per_K']:.1f} J/K")
        print(f"      — extraction: {r_low['sigma_cap_Fe_J_per_K']:.1f} J/K")
        print(f"      — recycling:  {r_low['sigma_rec_Fe_J_per_K']:.1f} J/K")
        print(f"    Σ_cap_g (Al extraction):             {r_low['sigma_cap_g_J_per_K']:.1f} J/K")
        print(f"    r_s range: {r_high['r_s_W_per_K']:.4e} – {r_low['r_s_W_per_K']:.4e} W/K")
        if t_low > 0:
            print(f"    τ* interval: [{t_low:.1f}, {t_high:.1f}] years")
        else:
            print(f"    τ* interval: [{t_low:.1f}, {t_high:.1f}] years  (negative → {r_low['regime']})")
        print()
    print("Data sources: Szargut (1988) b_ch; NIST ΔG; ISO 9223 corrosion rates.")
    print("mp-api replacement targets: b_ch(Fe), b_ch(Al), elastic tensors for Σ_g floor.")


if __name__ == "__main__":
    main()
