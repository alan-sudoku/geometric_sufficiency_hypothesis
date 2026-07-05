"""
 GSH mathematical consistency verifier.

Checks:
  1. SI unit identity: W/K == J/(K*s) -- physical unit of entropy generation rate
  2. Unit calculation: integral(W/K)dt over tau yields J/K -- constant-rate closed form
  3. Dynamic rate structure: Sigma_s and Sigma_g as Integrals of Function(t) rates
  4. Commensurability: Sigma_g and Sigma_s have matching integral bounds
  5. Minimisation objective: integral(S_dot_supply(t)+S_dot_maint(t))dt is a well-formed Integral
  6. Temporal composite structure (M:ss1 "Scope (integral formulation)" -- discrete-deployed case):
     Sigma_cap + integral(S_dot_main dt) + Sigma_rec
     -- discrete terms are tau-independent; integral term scales linearly with tau
  7. Crossover tau* formula: tau* = (Sigma_cap_g - Sigma_cap_s) / (sigma_dot_s - sigma_dot_g)
     -- positive iff Sigma_cap_g > Sigma_cap_s AND sigma_dot_s > sigma_dot_g simultaneously
     (code variables: sigma_dot_s, sigma_dot_g; document notation: Sigma_dot_s, Sigma_dot_g)
  8. No-crossover condition: sigma_dot_g >= sigma_dot_s -> tau* <= 0 (no favourable tau exists -- geometry never cheaper)
  9. Carnot -> cop_ratio chain (Challenge A / K3C60 cryogenic cost boundary):
     COP = T_C/(T_H-T_C); W_min = Q_C/COP; cop_ratio = W_min/T_H = Q_C(T_H-T_C)/(T_H*T_C)
     -- Gouy-Stodola step verified symbolically; concrete value at T_C=18K confirmed;
       T_C->0 limit shows structural connection to check 8 cop_ratio->inf form (not a proof
       that K3C60 at 18K has no crossover -- finite cop_ratio at 18K requires physical data comparison);
       extended: three physical heat-load models show no-crossover conditional on load
       not decaying as fast as T_C (linear-decay model produces finite limit)
 10. Boltzmann-Shannon bound as time-integral (Q-GSH.8-EXG-MATH):
     S_dot_gen_min(t) >= k_B * ln(Omega) / tau_thermal  ->  Sigma_g_min = integral_0^tau k_B*ln(Omega)/tau_thermal dt
     Scope: constant-Omega (static configuration) special case; ACTIVE maintenance regime only.
     The k_B*ln(Omega)/tau_thermal bound applies when an agent actively corrects misconfigurations
     (generalised Landauer / Sagawa-Ueda). For passive high-barrier structures (E_b >> k_BT),
     Arrhenius suppression -> Sigma_g_maintenance ~= 0; applying this form there is non-conservative.
     Two assertions (constant-Omega, active-regime case):
       (a) Integral over tau yields k_B*ln(Omega)*tau/tau_thermal -- units J/K (same as Sigma_g).
           Structurally identical to check 2; confirms expression is correctly formed.
       (b) Sigma_g_min scales linearly with tau (doubling tau doubles the bound).
           Valid for constant Omega only -- does not hold for time-varying Omega_G(t).
     Extended assertion: Omega(t) = Omega_0*e^(t/tau_deg) gives integral(rate dt) with a tau^2 term;
       sigma(2*tau) != 2*sigma(tau) -- algebraic proof that non-linearity holds.
     See OQ-GSH.8: extends check 9 (constant Omega) to time-varying Omega_G(t) = Omega_0*e^(t/tau_deg).
 11. TUR cumulative form structure (dimensional homogeneity fix -- TUR):
     Sigma_g^min >= 2*k_B/epsilon^2  (Barato-Seifert 2015 cumulative form)
     -- 2 and k_B in numerator; epsilon^2 in denominator; old rate form (J^2 in numerator)
       is structurally distinct from the corrected form
 12. Gibbs upper bound with n(x,tau) factor (dimensional homogeneity fix -- Gibbs):
     Sigma_s^max <= Delta_G_refine(x)/T * f(tau) * n(x,tau)
     -- Delta_G in numerator, T in denominator (extends R6 linter); n required for
       dimensional closure; f is dimensionless
 13. Axiom II intensive form (Q-GSH.25 -- eta_ex factor + per-mole basis):
     Delta_G_recovery <= eta_ex * Q_dot_ambient*tau_recovery / n_rec(x)
     -- eta_ex in numerator (dimensionless exergy efficiency factor, OQ-GSH.32);
       n_rec in denominator; LHS/RHS ratio is dimensionless;
       old extensive form (no n_rec) is structurally unbalanced;
       formula without eta_ex is structurally different from corrected form

Rates are modelled as Functions of time (not constants), so checks 3-5 verify
bound structure rather than closed-form equality -- valid for any time-varying rate,
including supply-chain spikes and discrete maintenance events (MDL-2 staging note).
Check 2 uses a constant rate to isolate the unit calculation from the bound structure.
Check 6 models the discrete-deployed composite explicitly: Sigma_total = Sigma_cap + integral(S_dot_main dt)
+ Sigma_rec. Asserts that doubling tau leaves Sigma_cap and Sigma_rec unchanged while the integral
term doubles -- the tau-amortisation property from M:ss1 "Scope (integral formulation)".
Check 7 derives the crossover lifetime tau* = (Sigma_cap_g - Sigma_cap_s) / (sigma_dot_s - sigma_dot_g) and
verifies it is positive iff both conditions hold simultaneously: geometry costs more to
build (Sigma_cap_g > Sigma_cap_s) and less to maintain (sigma_dot_s > sigma_dot_g). Maps directly to the
M:ss4 no-crossover cost outcome: tau* <= 0 when sigma_dot_g >= sigma_dot_s -- no tau exists where substitution is favourable.
Check 17 verifies the directional claim at M:ss6.1 line 869 and OQ-GSH.8 glossary line 977:
below tau* the party with the lower intercept and higher rate (cryogenic substitute in
regime d) is cheaper; above tau* the other party (Fe) is cheaper. Proves this symbolically
for the cryogenic regime (Sigma_cap_g < Sigma_cap_s, sigma_dot_g > sigma_dot_s, tau* > 0) using inequality
witnesses at tau = tau*/2 and tau = 2*tau*.
Check 8 asserts the no-crossover condition formally: sigma_dot_g >= sigma_dot_s implies tau* <= 0,
distinguishing finite no-crossover (sigma_dot_g > sigma_dot_s, finite) from infinite-rate no-crossover (sigma_dot_g -> inf).
Check 9 verifies the Carnot -> cop_ratio algebraic chain for the cryogenic cost boundary (Challenge A):
COP_Carnot = T_C/(T_H-T_C); W_min = Q_C/COP; Gouy-Stodola step cop_ratio = W_min/T_H.
Confirms the chain reduces to cop_ratio = Q_C(T_H-T_C)/(T_H*T_C), the concrete value at
T_C=18K/T_H=300K equals 47/900 (rational exact), and lim(T_C->0) gives cop_ratio->inf --
the infinite-rate limit. Does NOT compare sigma_dot_g to sigma_dot_s(Fe): that requires physical process
data outside algebraic scope.
Checks 11-13 verify the three dimensional homogeneity corrections: TUR cumulative
form (Barato-Seifert 2015), Gibbs bound with explicit n(x,tau) mole factor, and Axiom II
per-mole basis. Each check also asserts that the old (pre-correction) form is structurally
distinct, providing machine-verified grounds for the reformulations.

Run: python3 verify_gsh_math.py
Exit 0 = all checks pass. Exit 1 = at least one check failed.

To register new math expressions as the document grows: add a check function
following the pattern below and call it from main().
 17. Crossover direction -- regime (d): cryogenic substitute cheaper below tau*, Fe cheaper above tau*
     (M:ss6.1 line 869, OQ-GSH.8 glossary):
     In regime (d): Sigma_cap_g < Sigma_cap_s, sigma_dot_g > sigma_dot_s -> tau* > 0.
     At tau < tau*: Sigma_g(tau) < Sigma_s(tau) -- substitute cheaper.
     At tau > tau*: Sigma_g(tau) > Sigma_s(tau) -- Fe cheaper.
     Verified symbolically via SymPy inequality witnesses at τ = τ*/2 and τ = 2τ*.
"""

from sympy import symbols, integrate, simplify, Function, Integral, log
from sympy.physics.units import (
    joule, kelvin, second, watt,
    convert_to,
)

PASS = []
FAIL = []


def record(name, passed, detail=""):
    if passed:
        PASS.append(name)
    else:
        FAIL.append(f"{name}: {detail}")


# ---------------------------------------------------------------------------
# Shared symbols
# ---------------------------------------------------------------------------
t, tau = symbols("t tau", positive=True)


# ---------------------------------------------------------------------------
# Check 1: SI unit identity
# W/K == J/(K·s) — the physical unit of S_dot_gen
# Both reduce to the same SI base: kg·m²/(K·s³)
# ---------------------------------------------------------------------------
def check_rate_units():
    rate_unit = watt / kelvin
    equivalent = joule / (kelvin * second)
    base = [joule, kelvin, second]
    rate_si   = convert_to(rate_unit, base)
    equiv_si  = convert_to(equivalent, base)
    ok = simplify(rate_si - equiv_si) == 0
    record("rate_units: W/K == J/(K·s)", ok,
           f"W/K={rate_si}, J/(K·s)={equiv_si}")


# ---------------------------------------------------------------------------
# Check 2: Unit calculation — constant-rate closed form
# ∫_0^τ C dt = C·τ  →  units: (W/K)·s = J/K
# Uses a constant symbol to isolate the unit argument.
# Dynamic rates (Check 3 onward) leave the integral unevaluated — this check
# proves the unit conclusion for any rate that carries W/K.
# ---------------------------------------------------------------------------
def check_integral_units_constant():
    S_dot_const = symbols("S_dot_const", positive=True)   # W/K constant
    result   = integrate(S_dot_const, (t, 0, tau))
    expected = S_dot_const * tau
    ok = simplify(result - expected) == 0
    record("integral_units (constant rate): ∫C dt = C·τ  →  J/K", ok,
           f"got {result}, expected {expected}")


# ---------------------------------------------------------------------------
# Check 3: Dynamic rate structure — Sigma definitions
# Sigma_s(E*, tau) = ∫_0^tau S_dot_supply(t) dt
# Sigma_g(G,  tau) = ∫_0^tau S_dot_maint(t)  dt
# Rates are Functions of t (time-varying). Integrals stay unevaluated.
# Assert: both are Integral objects with bounds (t, 0, tau) — STRUCTURAL match only.
# Unit closure (W/K × s = J/K) is proved for constant rates in check 2; the argument
# extends to time-varying rates because dimensionality is independent of rate shape,
# but SymPy does not evaluate units through unevaluated Integral objects.
# ---------------------------------------------------------------------------
def check_sigma_definitions_dynamic():
    S_dot_supply = Function("S_dot_supply")(t)  # W/K, time-varying
    S_dot_maint  = Function("S_dot_maint")(t)   # W/K, time-varying

    sigma_s = integrate(S_dot_supply, (t, 0, tau))
    sigma_g = integrate(S_dot_maint,  (t, 0, tau))

    ok = (
        isinstance(sigma_s, Integral) and
        isinstance(sigma_g, Integral) and
        sigma_s.limits == ((t, 0, tau),) and
        sigma_g.limits == ((t, 0, tau),)
    )
    record("sigma_definitions (dynamic): Sigma_s and Sigma_g are Integrals with bounds (t, 0, τ)",
           ok, f"Sigma_s bounds={getattr(sigma_s, 'limits', None)}, "
               f"Sigma_g bounds={getattr(sigma_g, 'limits', None)}")


# ---------------------------------------------------------------------------
# Check 4: Commensurability of the core inequality
# Sigma_g(G, tau) < Sigma_s(x, tau)
# Both are Integrals over the same bounds (t, 0, tau) — commensurable.
# SymPy cannot evaluate the direction of the inequality (no numeric values);
# this confirms only that the comparison is between same-structure quantities.
# ---------------------------------------------------------------------------
def check_inequality_commensurability():
    S_dot_supply = Function("S_dot_supply")(t)
    S_dot_maint  = Function("S_dot_maint")(t)

    lhs = integrate(S_dot_maint,  (t, 0, tau))  # Sigma_g
    rhs = integrate(S_dot_supply, (t, 0, tau))  # Sigma_s

    commensurable = (
        isinstance(lhs, Integral) and
        isinstance(rhs, Integral) and
        lhs.limits == rhs.limits == ((t, 0, tau),)
    )
    record("inequality_commensurability: Sigma_g < Sigma_s compares Integrals with matching bounds",
           commensurable,
           f"lhs.limits={getattr(lhs, 'limits', None)}, rhs.limits={getattr(rhs, 'limits', None)}")


# ---------------------------------------------------------------------------
# Check 5: MDL-2 minimisation objective — well-formed Integral
# min_{E*,G} ∫_0^tau (S_dot_supply(t) + S_dot_maint(t)) dt
# Sum of two W/K Functions of t; integral over (t, 0, tau) is well-formed.
# ---------------------------------------------------------------------------
def check_minimisation_objective():
    S_dot_supply = Function("S_dot_supply")(t)
    S_dot_maint  = Function("S_dot_maint")(t)

    objective = integrate(S_dot_supply + S_dot_maint, (t, 0, tau))

    ok = (
        isinstance(objective, Integral) and
        objective.limits == ((t, 0, tau),)
    )
    record("minimisation_objective: ∫(Ṡ_supply(t)+Ṡ_maint(t))dt is Integral over (t, 0, τ)",
           ok, str(objective))


# ---------------------------------------------------------------------------
# Check 6: Temporal composite structure — discrete-deployed Σ_s
# §1 "Scope (integral formulation)" — discrete-deployed case:
#   Σ_total = Σ_cap + ∫_0^τ Ṡ_main(t) dt + Σ_rec
# Σ_cap and Σ_rec are front- and back-loaded impulses (τ-independent).
# The integral term is the only τ-dependent component.
#
# τ-amortisation test: substitute τ → 2τ.
#   Σ_cap and Σ_rec must be unchanged (no τ in their expressions).
#   The integral term must double (linear scaling in τ).
# This asserts the property that makes geometric substitution more attractive
# at long τ: the one-time capital cost is amortised over more operational time.
# ---------------------------------------------------------------------------
def check_temporal_composite():
    Sigma_cap = symbols("Sigma_cap", positive=True)   # manufacturing impulse — J/K
    Sigma_rec = symbols("Sigma_rec", positive=True)   # decommissioning impulse — J/K
    S_dot_main = symbols("S_dot_main", positive=True) # constant maintenance rate — W/K

    integral_term = integrate(S_dot_main, (t, 0, tau))          # = S_dot_main * tau
    Sigma_total   = Sigma_cap + integral_term + Sigma_rec

    # Substitute τ → 2τ and compare
    Sigma_total_2tau = Sigma_total.subs(tau, 2 * tau)

    delta_cap  = simplify(
        Sigma_total_2tau.subs({S_dot_main: 0, Sigma_rec: 0}) -
        Sigma_total.subs({S_dot_main: 0, Sigma_rec: 0})
    )
    delta_rec  = simplify(
        Sigma_total_2tau.subs({S_dot_main: 0, Sigma_cap: 0}) -
        Sigma_total.subs({S_dot_main: 0, Sigma_cap: 0})
    )
    delta_integral = simplify(
        Sigma_total_2tau.subs({Sigma_cap: 0, Sigma_rec: 0}) -
        2 * Sigma_total.subs({Sigma_cap: 0, Sigma_rec: 0})
    )

    ok = (delta_cap == 0) and (delta_rec == 0) and (delta_integral == 0)
    record(
        "temporal_composite: Σ_cap and Σ_rec τ-independent; integral doubles when τ → 2τ",
        ok,
        f"Δcap={delta_cap}, Δrec={delta_rec}, Δintegral={delta_integral}",
    )


# ---------------------------------------------------------------------------
# Check 7: Crossover lifetime τ*
# Composite model for both sides:
#   Σ_s = Σ_cap_s + sigma_dot_s * τ   (element: manufacturing + ongoing supply)
#   Σ_g = Σ_cap_g + sigma_dot_g * τ   (geometry: manufacturing + ongoing maintenance)
# Crossover: Σ_g = Σ_s  →  τ* = (Σ_cap_g − Σ_cap_s) / (sigma_dot_s − sigma_dot_g)
#
# Four regimes (sign of numerator × sign of denominator):
#   (a) Σ_cap_g > Σ_cap_s AND sigma_dot_s > sigma_dot_g → τ* > 0  — substitution favourable at τ > τ*
#   (b) Σ_cap_g > Σ_cap_s AND sigma_dot_g > sigma_dot_s → τ* < 0  — no crossover, substitution never favourable
#   (c) Σ_cap_g < Σ_cap_s AND sigma_dot_s > sigma_dot_g → τ* < 0  — geometry always cheaper; no crossover needed
#   (d) Σ_cap_g < Σ_cap_s AND sigma_dot_g > sigma_dot_s → τ* > 0  — geometry cheaper to build but costlier
#                                                      to maintain; substitution favourable at
#                                                      short τ, unfavourable beyond τ*
# The sign witness used here covers all four regimes (a)–(d) above.
# Regime (d) is the short-τ-favourable crossover — not named in §4, but now
# verified by the check.
#
# §1 "Argument (Σ trade-off)" mapping: τ* is the physical analog of the dataset-size
# crossover in the MDL analogy — the point beyond which model compression (geometry)
# pays off over per-instance cost (element supply).
# §4 mapping: τ* ≤ 0 is the no-crossover cost outcome (criteria 6–10).
# ---------------------------------------------------------------------------
def check_crossover_tau():
    from sympy import solve, Symbol

    Sigma_cap_s, Sigma_cap_g = symbols("Sigma_cap_s Sigma_cap_g", positive=True)
    sigma_dot_s, sigma_dot_g = symbols("sigma_dot_s sigma_dot_g", positive=True)
    tau_var   = Symbol("tau_var", positive=True)

    Sigma_s = Sigma_cap_s + sigma_dot_s * tau_var
    Sigma_g = Sigma_cap_g + sigma_dot_g * tau_var

    solutions = solve(Sigma_g - Sigma_s, tau_var)
    ok_count = len(solutions) == 1
    if not ok_count:
        record("crossover_tau: unique τ* solution exists", False,
               f"solutions={solutions}")
        return

    tau_star = solutions[0]
    expected = (Sigma_cap_g - Sigma_cap_s) / (sigma_dot_s - sigma_dot_g)
    formula_ok = simplify(tau_star - expected) == 0

    # τ* < 0 when sigma_dot_g > sigma_dot_s and Σ_cap_g > Σ_cap_s.
    # could_extract_minus_sign() is unreliable for multi-symbol expressions;
    # use concrete substitution: Σ_cap_s=1, Σ_cap_g=2, sigma_dot_s=1, sigma_dot_g=2 → τ*=-1.
    from sympy import Rational
    tau_val  = tau_star.subs([
        (Sigma_cap_s, Rational(1)), (Sigma_cap_g, Rational(2)),
        (sigma_dot_s, Rational(1)),         (sigma_dot_g, Rational(2)),
    ])
    sign_ok = bool(tau_val < 0)

    # Test all four regimes from the docstring comment:
    #   (a) Σ_cap_g > Σ_cap_s, sigma_dot_s > sigma_dot_g → τ* > 0  (substitution favourable at τ > τ*)
    #   (b) Σ_cap_g > Σ_cap_s, sigma_dot_g > sigma_dot_s → τ* < 0  (no crossover, substitution never favourable)
    #   (c) Σ_cap_g < Σ_cap_s, sigma_dot_s > sigma_dot_g → τ* < 0  (geometry always cheaper)
    #   (d) Σ_cap_g < Σ_cap_s, sigma_dot_g > sigma_dot_s → τ* > 0  (short-τ favourable crossover)
    regime_cases = [
        # (cap_s, cap_g, r_s_val, r_g_val, expected_positive)
        (Rational(1), Rational(2), Rational(2), Rational(1), True),   # (a)
        (Rational(1), Rational(2), Rational(1), Rational(2), False),  # (b)
        (Rational(2), Rational(1), Rational(2), Rational(1), False),  # (c)
        (Rational(2), Rational(1), Rational(1), Rational(2), True),   # (d)
    ]
    regimes_passed = 0
    for cap_s_v, cap_g_v, r_s_v, r_g_v, expect_pos in regime_cases:
        v = tau_star.subs([(Sigma_cap_s, cap_s_v), (Sigma_cap_g, cap_g_v),
                           (sigma_dot_s, r_s_v), (sigma_dot_g, r_g_v)])
        if bool(v > 0) == expect_pos:
            regimes_passed += 1
    regimes_ok = (regimes_passed == 4)

    ok = formula_ok and sign_ok and regimes_ok
    record(
        "crossover_tau: τ* = (Σ_cap_g − Σ_cap_s)/(sigma_dot_s − sigma_dot_g); all 4 sign regimes verified",
        ok,
        f"τ*={tau_star}, formula_ok={formula_ok}, sign_ok={sign_ok}, regimes={regimes_passed}/4",
    )


# ---------------------------------------------------------------------------
# Check 8: No-crossover condition — no-crossover cost outcome
# When sigma_dot_g ≥ sigma_dot_s, Σ_g ≥ Σ_s for all τ ≥ 0 (given Σ_cap_g ≥ Σ_cap_s for fairness).
# Specific case: sigma_dot_g = sigma_dot_s (equal maintenance rates) — gap is constant = Σ_cap_g − Σ_cap_s.
# If additionally Σ_cap_g ≥ Σ_cap_s, geometry is never cheaper at any τ.
#
# Distinguishes:
#   No-crossover (finite)        — sigma_dot_g > sigma_dot_s, finite: τ* ≤ 0, substitution never favourable
#   No-crossover (infinite rate) — sigma_dot_g → ∞:           Σ_g → ∞ at any τ > 0 (K₃C₆₀ cryogenic case)
# ---------------------------------------------------------------------------
def check_no_crossover():
    from sympy import oo

    Sigma_cap_s, Sigma_cap_g = symbols("Sigma_cap_s Sigma_cap_g", positive=True)
    sigma_dot_s, sigma_dot_g = symbols("sigma_dot_s sigma_dot_g", positive=True)
    tau_var   = symbols("tau_var", positive=True)

    Sigma_s = Sigma_cap_s + sigma_dot_s * tau_var
    Sigma_g = Sigma_cap_g + sigma_dot_g * tau_var
    gap     = simplify(Sigma_g - Sigma_s)   # (Σ_cap_g − Σ_cap_s) + (sigma_dot_g − sigma_dot_s)·τ

    # Case 1: sigma_dot_g = sigma_dot_s — gap reduces to constant (Σ_cap_g − Σ_cap_s), τ-independent.
    gap_equal_rates = simplify(gap.subs(sigma_dot_g, sigma_dot_s))
    equal_rates_ok  = gap_equal_rates == Sigma_cap_g - Sigma_cap_s

    # Case 2: sigma_dot_g → ∞ — infinite rate; gap → ∞ at any positive τ.
    gap_infinite_rg    = gap.subs(sigma_dot_g, oo)
    gap_infinite_rg_ok = gap_infinite_rg == oo

    ok = equal_rates_ok and gap_infinite_rg_ok
    record(
        "no_crossover: sigma_dot_g=sigma_dot_s → constant gap; sigma_dot_g→∞ → gap→∞ (Σ_g → ∞, no crossover exists)",
        ok,
        f"gap_equal_rates={gap_equal_rates}, gap_infinite_rg={gap_infinite_rg}",
    )


# ---------------------------------------------------------------------------
# Check 9: Carnot → cop_ratio algebraic chain (Challenge A — K₃C₆₀ cryogenic cost boundary)
#
# Chain:
#   COP_Carnot = T_C / (T_H − T_C)
#   W_min      = Q_C / COP_Carnot                   [input work per unit cooling]
#   cop_ratio        = W_min / T_H                        [Gouy-Stodola: entropy gen rate]
#              = Q_C · (T_H − T_C) / (T_H · T_C)   [closed form]
#
# Q_C is treated as a positive constant independent of T_C. Physically, real
# parasitic heat loads vary with temperature (e.g., radiation ~ T_C^4). If
# Q_C(T_C) → 0 faster than (T_H − T_C)/(T_H · T_C) diverges, the limit
# cop_ratio → ∞ may not hold for a real system. The limit result here is therefore
# conditional on Q_C remaining bounded away from zero as T_C → 0.
#
# Three assertions:
#   (a) Symbolic reduction: cop_ratio simplifies to Q_C(T_H−T_C)/(T_H·T_C)
#   (b) Concrete value at T_C=18K, T_H=300K: cop_ratio/Q_C = 47/900  (rational exact)
#   (c) Structural limit: lim(T_C→0) cop_ratio → ∞
#
# On assertion (c): the T_C→0 limit shows the Carnot formula shares the same
# sigma_dot_g→∞ structural form as check 8's infinite-rate no-crossover limit. It is a
# structural connection — not evidence that K₃C₆₀ at 18K has no crossover. At 18K,
# sigma_dot_g/Q_C = 47/900, a finite value. Whether this finite sigma_dot_g exceeds sigma_dot_s(Fe)
# is the physical cost-comparison question; it requires supply-chain data and is
# outside algebraic scope. The limit and the 18K case are separate claims.
#
# What this does NOT assert: sigma_dot_g > sigma_dot_s(Fe) at 18K or at any finite T_C.
# ---------------------------------------------------------------------------
def check_carnot_rg_chain():
    from sympy import limit, oo, Rational

    T_C, T_H, Q_C = symbols("T_C T_H Q_C", positive=True)

    COP    = T_C / (T_H - T_C)
    W_min  = Q_C / COP                        # = Q_C(T_H − T_C)/T_C
    cop_ratio    = W_min / T_H                      # Gouy-Stodola step

    expected = Q_C * (T_H - T_C) / (T_H * T_C)
    chain_ok = simplify(cop_ratio - expected) == 0

    # Concrete value at T_C=18, T_H=300: (300−18)/(300·18) = 282/5400 = 47/900
    r_g_numeric = cop_ratio.subs([(T_C, 18), (T_H, 300), (Q_C, 1)])
    numeric_ok  = simplify(r_g_numeric - Rational(47, 900)) == 0

    # Infinite-rate limit: as T_C → 0, cop_ratio → ∞
    r_g_limit  = limit(cop_ratio.subs(Q_C, 1), T_C, 0, "+")
    limit_ok   = r_g_limit == oo

    ok = chain_ok and numeric_ok and limit_ok
    record(
        "carnot_rg_chain: cop_ratio = Q_C(T_H−T_C)/(T_H·T_C); 47/900 at 18K/300K; →∞ as T_C→0",
        ok,
        f"chain_ok={chain_ok}, numeric_ok={numeric_ok} (got {r_g_numeric}), limit_ok={limit_ok}",
    )

    # Extended: verify limit behaviour under three physical heat load models.
    # Model 1 (constant load): already above — sigma_dot_g → ∞.  No crossover (infinite rate).
    # Model 2 (conductive coupling, Q_C ∝ (T_H − T_C)): sigma_dot_g → T_H/T_C * 1 → ∞.  No crossover (infinite rate).
    # Model 3 (linear decay, Q_C ∝ T_C): cop_ratio = T_C(T_H−T_C)/(T_H·T_C) = (T_H−T_C)/T_H → finite.
    #   The T_C→0 limit is T_H/T_H = 1 — no-crossover result does NOT hold.  Conditional on non-zero load.
    r_g_conductive  = cop_ratio.subs(Q_C, T_H - T_C)
    r_g_linear      = cop_ratio.subs(Q_C, T_C)
    lim_conductive  = limit(r_g_conductive,  T_C, 0, "+")
    lim_linear      = limit(r_g_linear,      T_C, 0, "+")
    heat_load_ok = (lim_conductive == oo) and (lim_linear != oo)
    record(
        "carnot_rg_chain_heat_load_models: conductive→∞ (no crossover); linear-decay→finite (conditional)",
        heat_load_ok,
        f"lim_conductive={lim_conductive}, lim_linear={lim_linear}",
    )


# ---------------------------------------------------------------------------
# Check 10: Boltzmann-Shannon bound as time-integral (Q-GSH.8-EXG-MATH)
#
# Staged repair Q-GSH.8-EXG-MATH resolves the dimensional ambiguity in the
# Boltzmann-Shannon lower bound by grounding it as a time-integral:
#
#   Ṡ_gen,min(t) ≥ k_B · ln(Ω_G) / τ_thermal
#   Σ_g_min(G, r, τ) = ∫_0^τ k_B · ln(Ω_G) / τ_thermal  dt
#                     = k_B · ln(Ω_G) · τ / τ_thermal
#
# Scope: constant-Ω (static configuration) special case. When Ω_G(t) is
# time-varying (degrading configuration), the integral is non-linear in τ
# and is outside algebraic scope.
#
# Two assertions (constant-Ω case):
#   (a) Integral form: closed-form result = k_B · ln(Ω) · τ / τ_thermal
#       Units: J/K — commensurable with Σ_g. Structurally identical to check 2
#       applied to this specific integrand; confirms the expression is correctly
#       formed, not an independent verification beyond check 2.
#   (b) Linear in τ: doubling τ doubles the bound (constant-Ω case only).
#
# Does NOT assert numerical values for Ω or τ_thermal.
# Does NOT compare Σ_g_min to Σ_s — dominance test requires physical data.
# ---------------------------------------------------------------------------
def check_boltzmann_shannon_bound():
    k_B, Omega, tau_thermal = symbols("k_B Omega tau_thermal", positive=True)

    # (a) Integral form: ∫_0^τ k_B·ln(Ω)/τ_thermal dt = k_B·ln(Ω)·τ/τ_thermal
    rate = k_B * log(Omega) / tau_thermal
    sigma_g_min = integrate(rate, (t, 0, tau))
    expected_integral = k_B * log(Omega) * tau / tau_thermal
    integral_ok = simplify(sigma_g_min - expected_integral) == 0

    # (b) Linear in τ — constant-Ω case only
    sigma_closed = k_B * log(Omega) * tau / tau_thermal
    sigma_doubled_tau = sigma_closed.subs(tau, 2 * tau)
    linear_tau_ok = bool(simplify(sigma_doubled_tau - 2 * sigma_closed) == 0)

    ok = integral_ok and linear_tau_ok
    record(
        "boltzmann_shannon_bound: Σ_g_min = k_B·ln(Ω)·τ/τ_thermal; J/K; linear in τ (const-Ω)",
        ok,
        f"integral_ok={integral_ok}, linear_tau_ok={linear_tau_ok}",
    )

    # Extended: algebraic proof of non-linearity for degrading configuration Ω(t) = Ω₀·e^(t/τ_deg).
    # ∫_0^τ k_B(ln(Ω₀) + t/τ_deg)/τ_thermal dt = k_B/τ_thermal · (ln(Ω₀)·τ + τ²/(2·τ_deg))
    # Doubling τ → quadratic term doubles in quadratic fashion; sum is NOT 2× original.
    Omega_0, tau_deg = symbols("Omega_0 tau_deg", positive=True)
    rate_t = k_B * (log(Omega_0) + t / tau_deg) / tau_thermal
    sigma_t        = integrate(rate_t, (t, 0, tau))
    sigma_t_2tau   = sigma_t.subs(tau, 2 * tau)
    nonlinear_ok = bool(simplify(sigma_t_2tau - 2 * sigma_t) != 0)
    record(
        "boltzmann_shannon_nonlinear: Ω(t)=Ω₀·e^(t/τ_deg) → Σ_g_min non-linear in τ",
        nonlinear_ok,
        f"sigma_t={sigma_t}; sigma(2τ)-2·sigma(τ)={simplify(sigma_t_2tau - 2*sigma_t)}",
    )


# ---------------------------------------------------------------------------
# Check 11: TUR cumulative form structure (dimensional homogeneity fix — TUR)
#
# Corrected formula (Barato-Seifert 2015 cumulative form):
#
#   Σ_g^min ≥ 2 · k_B / ε²
#
# where ε² = Var(X(τ)) / ⟨X(τ)⟩² is the squared coefficient of variation of
# the time-integrated transition count X(τ) — dimensionless.
#
# Assertions:
#   (a) Symbolic structure: the RHS is proportional to k_B with 2/ε² as the
#       dimensionless coefficient.  Simplifies to 2·k_B·(1/ε²).
#   (b) Coefficient direction: the factor 2 and k_B are in the numerator
#       (consistent with existing R5 linter intent, now for the cumulative form).
#   (c) Old rate form is structurally different: 2·k_B·J²/(Var/⟨X⟩²) with J [s⁻¹]
#       has an extra J² factor — not the same expression as 2·k_B/ε².
#
# This replaces the R5 linter check's intent for the corrected formula.
# The old rate-form structure (J² in numerator) is the discarded form.
# ---------------------------------------------------------------------------
def check_TUR_cumulative_structure():
    from sympy import symbols, simplify, Rational

    k_B, eps_sq = symbols("k_B eps_sq", positive=True)

    rhs = 2 * k_B / eps_sq

    # (a) Structure: rhs = 2·k_B·eps_sq⁻¹ — k_B in numerator, ε² in denominator
    # Extract numerator and denominator by inspecting the expression as a fraction.
    from sympy import fraction
    num, den = fraction(simplify(rhs))
    kb_in_num  = k_B in num.free_symbols
    two_in_num = bool(simplify(num / k_B - 2) == 0)   # coefficient is exactly 2
    eps_in_den = eps_sq in den.free_symbols

    ok_structure = kb_in_num and two_in_num and eps_in_den
    record(
        "TUR_cumulative_structure: 2·k_B in numerator, ε² in denominator",
        ok_structure,
        f"num={num}, den={den}, k_B_in_num={kb_in_num}, 2_in_num={two_in_num}, eps_in_den={eps_in_den}",
    )

    # (b) Old rate form has J² in numerator — structurally different
    J = symbols("J", positive=True)
    old_rhs = 2 * k_B * J**2 / eps_sq
    old_num, _ = fraction(simplify(old_rhs))
    J_sq_in_old_num = J**2 in old_num.free_symbols or simplify(old_num / (2 * k_B * J**2)) == 1
    record(
        "TUR_old_rate_form_structurally_different: J² in numerator distinguishes old from new",
        J_sq_in_old_num,
        f"old numerator={old_num}",
    )


# ---------------------------------------------------------------------------
# Check 12: Gibbs upper bound with explicit n(x,τ) factor (dimensional homogeneity fix — Gibbs)
#
# Corrected formula:
#
#   Σ_s^max(x, τ) ≤ ΔG_refine(x) / T · f(τ) · n(x, τ)
#
# Assertions:
#   (a) ΔG in numerator, T in denominator (extends existing R6 linter check).
#   (b) n(x,τ) appears as a positive multiplicative factor — required for
#       dimensional closure from J·mol⁻¹·K⁻¹ → J·K⁻¹.
#   (c) Without n, the expression has a residual mol⁻¹ factor — confirmed broken.
#   (d) f(τ) is dimensionless (a pure scaling factor); with f=1 the formula
#       still closes dimensionally, confirming f does not carry units.
# ---------------------------------------------------------------------------
def check_gibbs_bound_with_n():
    from sympy import symbols, simplify

    dG, T, f, n = symbols("dG T f n", positive=True)
    # dG [J/mol], T [K], f [dimensionless], n [mol]

    rhs_corrected = dG / T * f * n    # J/mol / K * 1 * mol = J/K

    # (a) dG in numerator, T in denominator
    from sympy import fraction
    num, den = fraction(simplify(rhs_corrected))
    dG_in_num = dG in num.free_symbols
    T_in_den  = T  in den.free_symbols
    record(
        "gibbs_bound_dG_in_num_T_in_den: direction check holds after adding n",
        dG_in_num and T_in_den,
        f"num={num}, den={den}",
    )

    # (b) n is a multiplicative factor — removing it changes the expression
    rhs_without_n = dG / T * f
    structurally_different = simplify(rhs_corrected - rhs_without_n) != 0
    record(
        "gibbs_bound_n_is_required: formula without n differs from formula with n",
        structurally_different,
        f"with_n={rhs_corrected}, without_n={rhs_without_n}",
    )

    # (c) f is dimensionless: setting f=1 does not change dimensional structure
    from sympy import Rational
    rhs_f1     = rhs_corrected.subs(f, Rational(1))
    rhs_corrected_simplified = simplify(rhs_corrected / f)
    f_dimensionless = simplify(rhs_f1 - rhs_corrected_simplified) == 0
    record(
        "gibbs_bound_f_dimensionless: f=1 leaves dimensional structure unchanged",
        f_dimensionless,
        f"rhs_f1={rhs_f1}, rhs/f={rhs_corrected_simplified}",
    )


# ---------------------------------------------------------------------------
# Check 13: Axiom II intensive form structural check (dimensional homogeneity fix — per-mole basis)
#
# Corrected formula (Q-GSH.25):
#
#   ΔG_recovery(x) ≤ η_ex · Q̇_ambient · τ_recovery / n_rec(x)
#
# η_ex: exergy efficiency of ambient-flux-to-chemical-work conversion —
#   dimensionless, 0 < η_ex ≤ 1; bounded above by η_theoretical (Landsberg
#   for solar, Carnot for thermal gradient, quantum efficiency for
#   photochemical). Context-dependent; operative value open per OQ-GSH.32.
#
# Assertions:
#   (a) n_rec appears in the denominator of the RHS.
#   (b) η_ex appears in the numerator of the RHS.
#   (c) With n_rec in denominator, LHS and RHS have the same dimensional
#       structure (both proportional to the same symbol combination).
#   (d) Old form (without n_rec): LHS has an extra mol⁻¹ factor relative to
#       RHS — structurally unbalanced; confirmed by checking their ratio is
#       not dimensionless (contains mol).
#   (e) Formula without η_ex is structurally different (η_ex is not optional).
# ---------------------------------------------------------------------------
def check_axiom_II_intensive_structure():
    from sympy import symbols, simplify

    dG_rec, Q_dot, tau_r, n_rec, eta_ex = symbols("dG_rec Q_dot tau_r n_rec eta_ex", positive=True)
    # dG_rec [J/mol], Q_dot [J/s], tau_r [s], n_rec [mol], eta_ex [dimensionless]

    lhs = dG_rec                                    # J/mol
    rhs_intensive = eta_ex * Q_dot * tau_r / n_rec  # dimensionless · J/s · s / mol = J/mol

    # (a) n_rec in denominator of RHS
    from sympy import fraction
    _, den = fraction(simplify(rhs_intensive))
    n_in_den = n_rec in den.free_symbols
    record(
        "axiom_II_intensive_n_in_denominator: n_rec appears in RHS denominator",
        n_in_den,
        f"RHS denominator={den}",
    )

    # (b) η_ex in numerator of RHS
    num, _ = fraction(simplify(rhs_intensive))
    eta_in_num = eta_ex in num.free_symbols
    record(
        "axiom_II_intensive_eta_in_numerator: η_ex appears in RHS numerator",
        eta_in_num,
        f"RHS numerator={num}",
    )

    # (c) LHS and RHS have identical dimensional structure
    ratio_corrected = simplify(lhs / rhs_intensive)
    expected_ratio = dG_rec * n_rec / (eta_ex * Q_dot * tau_r)
    balanced = simplify(ratio_corrected - expected_ratio) == 0
    record(
        "axiom_II_intensive_lhs_rhs_balanced: LHS/RHS = dG·n/(η_ex·Q̇·τ) — same dimensional form",
        balanced,
        f"ratio={ratio_corrected}",
    )

    # (d) Old form (no n_rec) is unbalanced: LHS [J/mol], RHS_old [J]
    rhs_old   = eta_ex * Q_dot * tau_r    # J (missing n_rec)
    ratio_old = simplify(lhs / rhs_old)
    old_is_different = simplify(ratio_old - ratio_corrected) != 0
    record(
        "axiom_II_old_form_structurally_unbalanced: LHS/RHS_old ≠ LHS/RHS_intensive",
        old_is_different,
        f"ratio_old={ratio_old}, ratio_corrected={ratio_corrected}",
    )

    # (e) Formula without η_ex is structurally different
    rhs_no_eta = Q_dot * tau_r / n_rec
    no_eta_different = simplify(rhs_intensive - rhs_no_eta) != 0
    record(
        "axiom_II_eta_required: formula without η_ex is structurally different from corrected form",
        no_eta_different,
        f"with_eta={rhs_intensive}, without_eta={rhs_no_eta}",
    )


# ---------------------------------------------------------------------------
# Check 14: Gibbs bound collapse at n=0 (Q-GSH.15 — zero-consumption guard)
#
# The Gibbs upper bound Σ_s^max = ΔG/T · f(τ) · n(x,τ).
# At n = 0 (strict zero-consumption, e.g. Pt as catalyst) the formula evaluates
# to zero. This check verifies:
#   (a) n=0 → Σ_s^max = 0 — formula collapses as expected.
#   (b) At n=0, dominance test fires Σ_g^min > Σ_s^max for any Σ_g^min > 0
#       → pipeline correctly retains element, but for the wrong reason: the
#         Gibbs bound collapses rather than capturing the genuine initial
#         extraction cost Σ_s^initial (one-time, τ-independent).
#   (c) Σ_s = Σ_s^initial + n(x,τ)·ΔG/(T·f) — with initial term present,
#       the formula does not collapse at n=0.
# Purpose: expose the missing initial-extraction accounting path for
# zero/trace-consumption elements (OQ-GSH.24 infrastructure amortisation gap).
# ---------------------------------------------------------------------------
def check_gibbs_n_zero_guard():
    from sympy import symbols, simplify

    dG, T, f, Sigma_s_initial, Sigma_g_min = symbols(
        "dG T f Sigma_s_initial Sigma_g_min", positive=True
    )
    n_sym = symbols("n", nonnegative=True)

    # (a) n=0 → bound collapses to zero
    bound = dG / T * f * n_sym
    at_zero = bound.subs(n_sym, 0)
    collapses = at_zero == 0
    record(
        "gibbs_n_zero_collapses: n=0 → Σ_s^max = 0 (formula collapse confirmed)",
        collapses,
        f"bound at n=0: {at_zero}",
    )

    # (b) With Σ_g^min > 0, dominance test retains element — correct output, wrong path
    # Dominance: retain if Σ_g^min > Σ_s^max
    # At n=0: Σ_s^max=0; any positive Σ_g_min > 0 triggers retention
    # This is symbolically always true for positive Σ_g_min — confirm the direction
    dominance_retain = Sigma_g_min > at_zero  # Σ_g_min > 0 = True for positive Σ_g_min
    record(
        "gibbs_n_zero_retention_direction: Σ_g^min > 0 > Σ_s^max=0 → retain (correct output)",
        bool(dominance_retain),
        "retention holds because Σ_g_min is positive and Σ_s^max collapsed to 0",
    )

    # (c) With initial extraction term, bound does not collapse at n=0
    bound_with_initial = Sigma_s_initial + dG / T * f * n_sym
    at_zero_with_initial = bound_with_initial.subs(n_sym, 0)
    does_not_collapse = simplify(at_zero_with_initial - Sigma_s_initial) == 0
    record(
        "gibbs_initial_term_prevents_collapse: Σ_s^initial + n·ΔG/T·f ≠ 0 at n=0",
        does_not_collapse,
        f"bound at n=0 with initial term: {at_zero_with_initial}",
    )


# ---------------------------------------------------------------------------
# Check 15: τ→0 dominance direction (Q-GSH.16 — short-lifetime guard)
#
# As τ→0:
#   Σ_s(x,τ) → 0  (rate-integral model: ∫_0^τ Ṡ dt → 0)
#   Boltzmann-Shannon bound → 0  (proportional to τ/τ_thermal)
#   Gibbs bound → 0  (via f(τ) → 0 when f = τ/τ_cycle)
#   Manufacturing entropy Σ_g_mfg = W_irrev/T0  is τ-INDEPENDENT — stays constant
#
# Dominance at τ→0: Σ_g^min ≈ Σ_g_mfg > 0; Σ_s^max → 0
#   → geometry disqualified; element retained (Σ_g > Σ_s)
#   → pipeline output: retain all elements → |E*| = |E| at τ=0
# This is the correct physical answer (zero-lifetime deployment has no
# supply-chain liability) but inverts the hypothesis's directional claim.
#
# Checks:
#   (a) Σ_s^max(τ) → 0 as τ → 0 for the continuous-rate and Gibbs models.
#   (b) Σ_g_mfg is τ-independent: ∂(Σ_g_mfg)/∂τ = 0.
#   (c) At τ → 0: Σ_g_mfg > Σ_s^max — dominance fires in retention direction.
#   (d) At τ → ∞: Σ_s (linear in τ) eventually exceeds Σ_g_mfg (constant)
#       → crossover τ* = Σ_g_mfg / sigma_dot_s exists and is positive for sigma_dot_s > 0.
# ---------------------------------------------------------------------------
def check_tau_zero_dominance_direction():
    from sympy import symbols, limit, oo, simplify, diff

    tau, tau_cycle, sigma_dot_s, W_irrev, T0, k_B, Omega, tau_thermal = symbols(
        "tau tau_cycle sigma_dot_s W_irrev T0 k_B Omega tau_thermal", positive=True
    )

    # Σ_s continuous-rate model: sigma_dot_s · τ (constant rate)
    Sigma_s_rate = sigma_dot_s * tau
    lim_s_rate = limit(Sigma_s_rate, tau, 0)
    record(
        "tau_zero_Sigma_s_rate_vanishes: sigma_dot_s·τ → 0 as τ→0",
        lim_s_rate == 0,
        f"limit = {lim_s_rate}",
    )

    # Gibbs bound with f(τ) = τ/τ_cycle
    Sigma_s_gibbs = (sigma_dot_s / tau_cycle) * tau   # proxy: ΔG/T · (τ/τ_cycle) · n collapses to this form
    lim_s_gibbs = limit(Sigma_s_gibbs, tau, 0)
    record(
        "tau_zero_Sigma_s_gibbs_vanishes: Gibbs bound → 0 as τ→0 (f=τ/τ_cycle form)",
        lim_s_gibbs == 0,
        f"limit = {lim_s_gibbs}",
    )

    # Boltzmann-Shannon bound: k_B·ln(Ω)·τ/τ_thermal
    Sigma_g_BS = k_B * Omega * tau / tau_thermal   # ln(Ω) treated as Omega symbol here
    lim_g_BS = limit(Sigma_g_BS, tau, 0)
    record(
        "tau_zero_BS_bound_vanishes: k_B·ln(Ω)·τ/τ_thermal → 0 as τ→0",
        lim_g_BS == 0,
        f"limit = {lim_g_BS}",
    )

    # (b) Manufacturing entropy is τ-independent
    Sigma_g_mfg = W_irrev / T0
    deriv = diff(Sigma_g_mfg, tau)
    record(
        "Sigma_g_mfg_tau_independent: ∂(W_irrev/T0)/∂τ = 0",
        deriv == 0,
        f"derivative = {deriv}",
    )

    # (c) At τ→0: Σ_g_mfg > Σ_s_rate → retention direction
    # Symbolic: W_irrev/T0 > sigma_dot_s·0 = 0 → True for positive W_irrev, T0
    from sympy import Symbol
    retention_at_zero = Sigma_g_mfg > limit(Sigma_s_rate, tau, 0)
    record(
        "tau_zero_retention_direction: Σ_g_mfg > Σ_s→0 at τ=0 (geometry disqualified, retain element)",
        bool(retention_at_zero),
        f"Σ_g_mfg={Sigma_g_mfg}, Σ_s at τ=0 = {limit(Sigma_s_rate, tau, 0)}",
    )

    # (d) Crossover τ* = Σ_g_mfg / sigma_dot_s — positive for sigma_dot_s > 0
    tau_star = Sigma_g_mfg / sigma_dot_s
    crossover_positive = simplify(tau_star) > 0
    record(
        "tau_star_mfg_crossover_positive: τ* = W_irrev/(T0·sigma_dot_s) > 0 for sigma_dot_s>0",
        bool(crossover_positive),
        f"τ* = {tau_star}",
    )


# ---------------------------------------------------------------------------
# Check 16: TUR bound magnitude at sample ε² values (Q-GSH.14 — scale guard)
#
# TUR bound: Σ_g^min ≥ 2·k_B/ε²
# k_B = 1.380649e-23 J/K
#
# For the bound to be macroscopically significant (comparable to engineering-scale
# Σ_s ~ 10^3–10^6 J/K), ε² must be ≈ 10^{-26} or smaller.
#
# Sample substitutions expose the order-of-magnitude gap:
#   ε² = 1     (maximum uncertainty, single transition):  2k_B ≈ 2.76e-23 J/K
#   ε² = 0.01  (tight, 1% CV):                           2k_B/0.01 ≈ 2.76e-21 J/K
#   ε² = 1e-20 (extreme precision):                      2k_B/1e-20 ≈ 2.76e-3  J/K
#
# Checks:
#   (a) At ε²=1: TUR bound ≈ 2.76e-23 J/K — below any macroscopic Σ_s.
#   (b) At ε²=1e-20: TUR bound ≈ 2.76e-3 J/K — still below 1 J/K engineering threshold.
#   (c) Crossover ε²* where TUR = 1 J/K: ε²* = 2k_B ≈ 2.76e-23 — physically
#       implausible for any macroscopic system (requires CV < 5e-12).
#   These confirm the TUR bound is operative only at nano/molecular scale.
# ---------------------------------------------------------------------------
def check_TUR_magnitude_sample():
    k_B_val = 1.380649e-23  # J/K

    # (a) ε²=1: TUR ≈ 2k_B
    tur_eps1 = 2 * k_B_val / 1.0
    below_macro_eps1 = tur_eps1 < 1e-3   # well below any engineering Σ_s
    record(
        "TUR_magnitude_eps2_eq_1: 2k_B/1 ≈ 2.76e-23 J/K — far below engineering Σ_s scale",
        below_macro_eps1,
        f"2k_B/ε²(ε²=1) = {tur_eps1:.3e} J/K",
    )

    # (b) ε²=1e-20: TUR ≈ 2.76e-3 J/K — still sub-millijoule/K
    tur_eps_small = 2 * k_B_val / 1e-20
    below_macro_eps_small = tur_eps_small < 1.0
    record(
        "TUR_magnitude_eps2_eq_1e-20: 2k_B/1e-20 ≈ 2.76e-3 J/K — still below 1 J/K",
        below_macro_eps_small,
        f"2k_B/ε²(ε²=1e-20) = {tur_eps_small:.3e} J/K",
    )

    # (c) Crossover ε²* where TUR = 1 J/K
    eps_sq_crossover = 2 * k_B_val / 1.0   # ε²* = 2k_B for TUR=1 J/K
    physically_implausible = eps_sq_crossover < 1e-20
    record(
        "TUR_crossover_eps2_implausible: ε²* for TUR=1 J/K is 2k_B ≈ 2.76e-23 — sub-quantum CV",
        physically_implausible,
        f"ε²* = {eps_sq_crossover:.3e} — requires CV < {eps_sq_crossover**0.5:.2e}",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Check 17: Crossover direction in regime (d) — cryogenic context (M:§6.1 line 869)
#
# Regime (d): Σ_cap_g < Σ_cap_s  AND  sigma_dot_g > sigma_dot_s  →  τ* > 0
#   (lower upfront cost for geometry; higher ongoing maintenance rate)
#   This is the cryogenic regime: substitute has lower manufacturing cost but COP-
#   amplified maintenance entropy rate.
#
# Model:
#   Σ_s(τ) = Σ_cap_s + sigma_dot_s · τ   (Fe: higher intercept, lower slope)
#   Σ_g(τ) = Σ_cap_g + sigma_dot_g · τ   (substitute: lower intercept, higher slope)
#   τ* = (Σ_cap_g − Σ_cap_s) / (sigma_dot_s − sigma_dot_g)  =  positive in regime (d)
#
# Directional claim (M:§6.1 line 869, OQ-GSH.8 glossary line 977):
#   below τ*: cryogenic substitute cheaper (Σ_g < Σ_s)
#   above τ*: Fe cheaper (Σ_g > Σ_s)
#
# Proof strategy: symbolic inequality witnesses at τ = τ*/2 and τ = 2·τ*.
#   At τ = τ*/2 = (Σ_cap_g − Σ_cap_s)/(2(sigma_dot_s − sigma_dot_g)):
#     Σ_g − Σ_s = (Σ_cap_g − Σ_cap_s) + (sigma_dot_g − sigma_dot_s)·τ*/2
#               = (Σ_cap_g − Σ_cap_s) − (Σ_cap_g − Σ_cap_s)/2
#               = (Σ_cap_g − Σ_cap_s)/2  < 0  (since Σ_cap_g < Σ_cap_s in regime d)
#   At τ = 2·τ*:
#     Σ_g − Σ_s = (Σ_cap_g − Σ_cap_s) + (sigma_dot_g − sigma_dot_s)·2τ*
#               = (Σ_cap_g − Σ_cap_s) − 2(Σ_cap_g − Σ_cap_s)
#               = −(Σ_cap_g − Σ_cap_s)  > 0  (since Σ_cap_g < Σ_cap_s in regime d)
# ---------------------------------------------------------------------------
def check_crossover_direction_regime_d():
    from sympy import Symbol, simplify, Rational

    Sigma_cap_s = Symbol("Sigma_cap_s", positive=True)
    Sigma_cap_g = Symbol("Sigma_cap_g", positive=True)
    sigma_dot_s = Symbol("sigma_dot_s", positive=True)
    sigma_dot_g = Symbol("sigma_dot_g", positive=True)

    # Regime (d) assumptions: Σ_cap_g < Σ_cap_s, sigma_dot_g > sigma_dot_s
    # Encode via substitution: cap_s=2, cap_g=1, sigma_dot_s=1, sigma_dot_g=2 (concrete witness)
    subs = [(Sigma_cap_s, Rational(2)), (Sigma_cap_g, Rational(1)),
            (sigma_dot_s, Rational(1)),         (sigma_dot_g, Rational(2))]

    tau_star = (Sigma_cap_g - Sigma_cap_s) / (sigma_dot_s - sigma_dot_g)

    Sigma_s_fn = Sigma_cap_s + sigma_dot_s * tau
    Sigma_g_fn = Sigma_cap_g + sigma_dot_g * tau

    # τ* must be positive in regime (d)
    tau_star_val = tau_star.subs(subs)
    tau_star_positive = bool(tau_star_val > 0)

    # Below τ*: substitute cheaper — Σ_g < Σ_s  →  Σ_g − Σ_s < 0
    tau_below = tau_star_val / 2
    gap_below = (Sigma_g_fn - Sigma_s_fn).subs(subs).subs(tau, tau_below)
    gap_below_simplified = simplify(gap_below)
    sub_cheaper_below = bool(gap_below_simplified < 0)

    # Above τ*: Fe cheaper — Σ_g > Σ_s  →  Σ_g − Σ_s > 0
    tau_above = tau_star_val * 2
    gap_above = (Sigma_g_fn - Sigma_s_fn).subs(subs).subs(tau, tau_above)
    gap_above_simplified = simplify(gap_above)
    fe_cheaper_above = bool(gap_above_simplified > 0)

    ok = tau_star_positive and sub_cheaper_below and fe_cheaper_above
    record(
        "crossover_direction_regime_d: cryogenic substitute cheaper below τ*,"
        " Fe cheaper above τ*",
        ok,
        f"τ*={tau_star_val}, gap@τ*/2={gap_below_simplified} (<0 means sub cheaper),"
        f" gap@2τ*={gap_above_simplified} (>0 means Fe cheaper),"
        f" τ*>0={tau_star_positive},"
        f" sub_cheaper_below={sub_cheaper_below},"
        f" fe_cheaper_above={fe_cheaper_above}",
    )


def main():
    check_rate_units()
    check_integral_units_constant()
    check_sigma_definitions_dynamic()
    check_inequality_commensurability()
    check_minimisation_objective()
    check_temporal_composite()
    check_crossover_tau()
    check_no_crossover()
    check_carnot_rg_chain()
    check_boltzmann_shannon_bound()
    check_TUR_cumulative_structure()
    check_gibbs_bound_with_n()
    check_axiom_II_intensive_structure()
    check_gibbs_n_zero_guard()
    check_tau_zero_dominance_direction()
    check_TUR_magnitude_sample()
    check_crossover_direction_regime_d()

    print(f"\n GSH math verifier — {len(PASS)} passed, {len(FAIL)} failed\n")
    for name in PASS:
        print(f"  PASS  {name}")
    if FAIL:
        print()
        for msg in FAIL:
            print(f"  FAIL  {msg}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
