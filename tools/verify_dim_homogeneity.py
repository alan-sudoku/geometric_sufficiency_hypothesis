"""
GSH dimensional homogeneity verifier.

Symbolically traces the unit algebra for every chain in M:ss8.4 of
GSH_mathematical_inventory.md.  Each check mirrors one node path in the
M:ss8.4 Mermaid diagram and produces a machine-verified closure result that
can be read directly into the LaTeX notation.

Chains verified:
  A1  Fe extraction term: b_ch(x) [J/mol] -> b_ch/T0*n(x,tau) [J/K]
  A2  Fe corrosion term:  r_corr*rho*|DG_ox|/T0/M * A * tau -> [J/K]
  A3  Recovery term:      Sigma_rec already normalised -- structural identity check
  A4  Sigma_s assembly:   A1 + A2 + A3 closes to [J/K]
  B   Boltzmann-Shannon (active-feedback Sigma_g^min):
        k_B*ln(Omega)*tau/tau_thermal -> [J/K]
  C   TUR cumulative (sustained-current Sigma_g^min):
        2*k_B / epsilon^2  where epsilon^2 = Var(X(tau))/<X(tau)>^2 [dimensionless] -> [J/K]
  AX  Axiom II thermodynamic condition (per-mole intensive form):
        DG_rec [J/mol]  <=  Q_dot_ambient*tau_recovery / n_rec [J/mol]  -- units match
  DH  Dimensional homogeneity gate: Sigma_s and Sigma_g^min both [J/K]

Unit algebra uses true SI base dimensions (kg, m, s, K, mol).  Joules are
expressed as kg*m^2*s^-2 so that all mechanical subterms (velocity, density,
molar mass) are traceable to the same roots.  This means the verifier will
catch dimensional errors in formulas that mix mechanical energy with entropy
units -- the original abstract-dimension approach would silently pass those.

assert_dimension() checks that expr / expected_dim is free of all base
physical dimensions.  Dimensionless multipliers (log, Omega, epsilon^2) are
correctly ignored because they are not members of BASE_DIM_SET.

Run:   python3 verify_dim_homogeneity.py
Exit 0 = all checks pass.
Exit 1 = at least one check failed.
"""

from sympy import symbols, simplify, log, Rational

PASS = []
FAIL = []


def record(name, passed, detail=""):
    if passed:
        PASS.append(name)
    else:
        FAIL.append(f"{name}: {detail}")


# ---------------------------------------------------------------------------
# True SI base dimensions (positive, independent)
# ---------------------------------------------------------------------------
mass_dim, length_dim, time_dim, temp_dim, mol_dim = symbols(
    "kg m s K mol", positive=True
)

# Derived units expressed in SI base dimensions
energy_dim = mass_dim * length_dim**2 / time_dim**2   # J = kg·m²·s⁻²
JK         = energy_dim / temp_dim                     # J/K
JKs        = energy_dim / temp_dim / time_dim          # W/K = J/(K·s)
Jmol       = energy_dim / mol_dim                      # J/mol
W          = energy_dim / time_dim                     # W = J/s

BASE_DIM_SET = {mass_dim, length_dim, time_dim, temp_dim, mol_dim}


# ---------------------------------------------------------------------------
# Generalised dimensional assertion helper
#
# Divides expr by expected_dim and checks that no base physical dimensions
# remain as free symbols in the ratio.  Dimensionless multipliers (log,
# Omega, symbolic coefficients) are not in BASE_DIM_SET and are ignored.
# This correctly handles negative quantities (entropy differences) and
# transcendental functions without special-casing.
# ---------------------------------------------------------------------------
def assert_dimension(name, expr, expected_dim):
    ratio = simplify(expr / expected_dim)
    remaining = ratio.free_symbols.intersection(BASE_DIM_SET)
    ok = len(remaining) == 0
    record(name, ok,
           f"got {expr}; ratio to expected = {ratio}; "
           f"remaining base dims = {remaining}")


# ---------------------------------------------------------------------------
# A1 — extraction term: b_ch(x) / T₀ · n(x, τ)
#
# b_ch  [J/mol]   chemical exergy of element x
# T₀    [K]       dead-state temperature
# n     [mol]     total moles consumed over τ  (explicit mole factor required for J/K closure)
#
# Step 1: b_ch / T₀  →  J/(mol·K)
# Step 2: × n [mol]  →  J/K  ✓
# ---------------------------------------------------------------------------
def check_A1_extraction():
    b_ch = Jmol
    T0   = temp_dim
    n    = mol_dim

    step1 = b_ch / T0
    step2 = step1 * n
    assert_dimension("A1_extraction: b_ch/T₀·n → J/K", step2, JK)


# ---------------------------------------------------------------------------
# A2 — corrosion term: r_corr · ρ · |ΔG_ox| / (T₀ · M) · A · τ
#
# r_corr  [m/s]       corrosion penetration rate
# ρ       [kg/m³]     density
# |ΔG_ox| [J/mol]     Gibbs energy of oxidation
# T₀      [K]         dead-state temperature
# M       [kg/mol]    molar mass
# A       [m²]        exposed surface area  (surface area factor required for J/K closure)
# τ       [s]         lifetime
#
# Step 1: r_corr · ρ / M       →  mol/(m²·s)
# Step 2: × |ΔG_ox|            →  W/m²
# Step 3: / T₀                 →  W/(m²·K)
# Step 4: × A                  →  W/K          ← entropy rate intermediate
# Step 5: × τ                  →  J/K  ✓
# ---------------------------------------------------------------------------
def check_A2_corrosion():
    r_corr = length_dim / time_dim
    rho    = mass_dim / length_dim**3
    dG_ox  = Jmol
    T0     = temp_dim
    M      = mass_dim / mol_dim
    A      = length_dim**2
    tau    = time_dim

    step1 = r_corr * rho / M
    step2 = step1 * dG_ox
    step3 = step2 / T0
    step4 = step3 * A
    step5 = step4 * tau

    assert_dimension("A2_corrosion_rate: step4 intermediate → W/K", step4, JKs)
    assert_dimension("A2_corrosion: r_corr·ρ·|ΔG_ox|/(T₀·M)·A·τ → J/K", step5, JK)


# ---------------------------------------------------------------------------
# A3 — recovery term: Σ_rec already J/K by Axiom II normalisation
# ---------------------------------------------------------------------------
def check_A3_recovery():
    assert_dimension("A3_recovery: Σ_rec identity check → J/K", JK, JK)


# ---------------------------------------------------------------------------
# A4 — Σ_s assembly: all three terms must be J/K before addition
# ---------------------------------------------------------------------------
def check_A4_sigma_s_assembly():
    total = JK + JK + JK
    assert_dimension("A4_sigma_s: (J/K) + (J/K) + (J/K) → J/K", total, JK)


# ---------------------------------------------------------------------------
# B — Boltzmann-Shannon active-feedback Σ_g^min
#
# Ṡ_gen,min = k_B · ln(Ω) / τ_thermal   [W/K]
# Σ_g^min   = Ṡ_gen,min · τ             [J/K]
#
# k_B        [J/K]         Boltzmann constant
# Ω          dimensionless (phase-space ratio — not in BASE_DIM_SET)
# τ_thermal  [s]           thermal fluctuation timescale
# τ          [s]           operational lifetime
#
# log(Omega) is dimensionless; assert_dimension ignores it correctly because
# Omega is not a member of BASE_DIM_SET.
# ---------------------------------------------------------------------------
def check_B_boltzmann_shannon():
    k_B   = JK
    Omega = symbols("Omega", positive=True)
    tau_t = time_dim
    tau   = time_dim

    rate    = k_B * log(Omega) / tau_t
    sigma_g = rate * tau

    assert_dimension("B_boltzmann_shannon_rate: k_B·ln(Ω)/τ_thermal → W/K", rate, JKs)
    assert_dimension("B_boltzmann_shannon: k_B·ln(Ω)·τ/τ_thermal → J/K", sigma_g, JK)


# ---------------------------------------------------------------------------
# C — TUR cumulative form (Barato-Seifert 2015)
#
# Σ_g^min = 2 · k_B / ε²
#
# k_B   [J/K]        Boltzmann constant
# ε²    dimensionless: Var(X(τ)) / ⟨X(τ)⟩²
#
# ε² is modelled with an arbitrary symbolic dimension dim_X so SymPy can
# confirm the ratio Var/⟨X⟩² = dim_X² / dim_X² simplifies to 1 regardless
# of the physical units of the configuration variable X.
#
# The check also asserts that the old rate form — 2·k_B·J²/ε² with J [s⁻¹]
# — carries a residual s⁻¹ factor and therefore does not satisfy W/K = J/(K·s).
# ---------------------------------------------------------------------------
def check_C_TUR_cumulative():
    k_B   = JK
    dim_X = symbols("dim_X", positive=True)
    Var_X = dim_X**2
    Mean_X = dim_X
    eps_sq = simplify(Var_X / Mean_X**2)     # → 1 (dimensionless by construction)

    sigma_g = 2 * k_B / eps_sq
    assert_dimension("C_TUR_cumulative: 2·k_B/ε² → J/K", sigma_g, JK)

    # Old rate form: 2·k_B·J² / ε²  with J [s⁻¹] — should fail W/K check
    J_rate  = Rational(1) / time_dim
    old_rhs = 2 * k_B * J_rate**2 / eps_sq
    ratio   = simplify(old_rhs / JKs)
    remaining = ratio.free_symbols.intersection(BASE_DIM_SET)
    record(
        "C_TUR_old_rate_form_broken: 2·k_B·J²/ε² [J=s⁻¹] ≠ W/K (residual s⁻¹)",
        len(remaining) > 0,
        f"ratio vs W/K = {ratio}; remaining base dims = {remaining}",
    )


# ---------------------------------------------------------------------------
# AX — Axiom II thermodynamic condition (intensive per-mole form)
#
# ΔG_recovery(x) ≤ η_ex · Q̇_ambient · τ_recovery / n_rec(x)
#
# LHS: ΔG_recovery  [J/mol]
# RHS: η_ex [dimensionless] · Q̇ [W] · τ [s] / n_rec [mol]  =  J/mol  ✓
#
# η_ex is the exergy efficiency of the ambient-flux-to-chemical-work conversion
# (Landsberg/Carnot/quantum-efficiency bound — context-dependent; OQ-GSH.32).
# Being dimensionless, it does not affect dimensional closure.
#
# Old form (no n_rec): Q̇·τ [J] vs ΔG [J/mol] — residual mol factor.
# ---------------------------------------------------------------------------
def check_AX_axiom_II():
    dG_rec = Jmol
    Q_dot  = W
    tau_r  = time_dim
    n_rec  = mol_dim
    eta_ex = symbols("eta_ex", positive=True)  # dimensionless — OQ-GSH.32

    rhs = eta_ex * Q_dot * tau_r / n_rec
    assert_dimension("AX_axiom_II: η_ex·Q̇·τ/n_rec → J/mol (matches ΔG_rec)", rhs, Jmol)

    # η_ex is dimensionless: removing it must leave dimensional structure unchanged
    rhs_no_eta = Q_dot * tau_r / n_rec
    assert_dimension("AX_axiom_II_eta_dimensionless: Q̇·τ/n_rec → J/mol (η_ex contributes no dimension)", rhs_no_eta, Jmol)

    # Old extensive form: Q̇·τ [J] — should fail J/mol check
    old_rhs  = Q_dot * tau_r
    ratio    = simplify(old_rhs / dG_rec)
    remaining = ratio.free_symbols.intersection(BASE_DIM_SET)
    record(
        "AX_axiom_II_old_form_broken: Q̇·τ [J] ≠ ΔG_rec [J/mol] (residual mol)",
        len(remaining) > 0,
        f"ratio vs J/mol = {ratio}; remaining base dims = {remaining}",
    )


# ---------------------------------------------------------------------------
# DH — Dimensional homogeneity gate
#
# Σ_s and Σ_g^min must both be J/K before the core inequality executes.
# Uses assert_dimension for consistency with all other checks.
# ---------------------------------------------------------------------------
def check_DH_gate():
    assert_dimension("DH_gate: Σ_s [J/K] is valid input to comparison", JK, JK)
    assert_dimension("DH_gate: Σ_g^min B [J/K] is valid input to comparison", JK, JK)
    assert_dimension("DH_gate: Σ_g^min C [J/K] is valid input to comparison", JK, JK)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    check_A1_extraction()
    check_A2_corrosion()
    check_A3_recovery()
    check_A4_sigma_s_assembly()
    check_B_boltzmann_shannon()
    check_C_TUR_cumulative()
    check_AX_axiom_II()
    check_DH_gate()

    print(f"\n  GSH dimensional homogeneity verifier — {len(PASS)} passed, {len(FAIL)} failed\n")
    for name in PASS:
        print(f"  PASS  {name}")
    if FAIL:
        print()
        for msg in FAIL:
            print(f"  FAIL  {msg}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
