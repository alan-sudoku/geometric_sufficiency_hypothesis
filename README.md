# Geometric Sufficiency Hypothesis

For any engineering requirement set $\mathcal{F}$, there exists a minimum-cardinality element set $\mathcal{E}^*$ such that all requirements in $\mathcal{F}$ can be satisfied through geometric arrangement of $\mathcal{E}^*$ alone — without adding elements whose function can be substituted by geometry. The operative criterion is thermodynamic: an element is removed when the precision entropy of the geometric substitute $\Sigma_g(\mathcal{G}, \tau)$ is lower than the supply-chain entropy of retaining it $\Sigma_s(x, \tau)$. The hypothesis is conditional on a sufficient AI reasoning system: human engineers cannot compute the geometric search space; the hypothesis holds only when that computation is available.

**Logical parent:** [The Entropic Compact](https://github.com/alan-sudoku/entropic_compact/blob/main/entropic_compact_overview.md) — the GSH is the engineering implementation of the EC's physical resource axis. The decision layer governing whether and how to act on GSH cost results sits there, not here.

---

## What is in this folder

| File | Role |
| :--- | :--- |
| [geometric_sufficiency_hypothesis.md](geometric_sufficiency_hypothesis.md) | Primary document — argument structure, four axioms, criteria hierarchy, open challenges. The hypothesis. |
| [GSH_mathematical_inventory.md](GSH_mathematical_inventory.md) | Co-primary — formula bodies, symbol glossaries, dimensional obligations, pipeline formalisation, verification coverage. The math. |
| [geometric_sufficiency_hypothesis_retraction.md](geometric_sufficiency_hypothesis_retraction.md) | Retraction log — every claim probed and found absent. The negative channel: what was shed and why. |
| [GSH_audit_prompt.md](GSH_audit_prompt.md) | Adversarial audit prompt — structured questions for an AI auditor to probe structural failures. |
| [abstract.md](abstract.md) | Deposit metadata — title, abstract, keywords, version, and licence for DOI submission. |

The four files instantiate the same Proposer-Auditor loop used across this project: the hypothesis proposes, the audit prompt challenges, the retraction log records what the loop found. The mathematical inventory is the third leg — it holds the formal content that the argument document references but does not encode inline, and it is where dimensional and algebraic claims are independently verifiable.

An AI auditor must load both primary documents: `geometric_sufficiency_hypothesis.md` carries the argument and axiomatic structure; `GSH_mathematical_inventory.md` carries the formal expressions and dimensional obligations. Neither is sufficient alone.

---

## How to engage

**General reader (no technical background):**
Attach [geometric_sufficiency_hypothesis.md](geometric_sufficiency_hypothesis.md) to an AI session and ask: (1) What is the core inequality, and what are its two sides in plain terms? (2) What are the four axioms, and what does each rule out? (3) What are the four open challenges in H:§6, and what would resolving each change about the element set?

**AI auditor (blank context):**
The audit prompt is the activation path. Attach [geometric_sufficiency_hypothesis.md](geometric_sufficiency_hypothesis.md) and [GSH_mathematical_inventory.md](GSH_mathematical_inventory.md) to a fresh AI session and run [GSH_audit_prompt.md](GSH_audit_prompt.md) as the first and only instruction. Read [geometric_sufficiency_hypothesis_retraction.md](geometric_sufficiency_hypothesis_retraction.md) first to avoid re-running already-resolved attacks.

**Verification-focused reader:**
Run the three scripts in `tools/` — they exit 0 on pass and produce falsifiable output. Read `GSH_mathematical_inventory.md` M:§0 (computability tier index) to understand what is T1-computable now vs. what is blocked by named open conditions.

**Contributor:**
The contribution mechanism is the audit path: find a structural failure — a logical flaw, category error, unargued premise, empirical counterexample, or dimensional inconsistency — and run it against the documents using the audit prompt format. If it survives with repair, it generates a retraction entry or an OQ. Suggestions that do not identify a specific structural failure are out of scope.

The most productive external input at this stage: adversarial audit of **Challenge A (magnetism gap)** — whether ferromagnetism has any geometric substitute at ambient temperature within $\mathcal{E}^*$, since this is the hypothesis's hardest open question and a candidate context-scoped falsification. The second productive target: **OQ-GSH.1** — whether $\Sigma_g(\mathcal{G}, \tau)$ is computable in the general case, since this blocks the full crossover calculation for arbitrary element-geometry pairs.

---

## Verification scripts

All scripts are in `tools/`. Run from the repository root with `python3 tools/<script>`.

| Script | What it checks | Exit 0 condition |
| :--- | :--- | :--- |
| `verify_gsh_math.py` | 20 algebraic checks (SymPy): crossover formula, regime coverage, Carnot chain, TUR cumulative form, Gibbs bound, Axiom II per-mole basis | All 20 pass |
| `verify_dim_homogeneity.py` | Dimensional homogeneity of all M:§8.4 chains (A, B, C, Axiom II, DH gate) using SI base dimensions | All 14 checks pass |
| `fe_crossover_numeric.py` | Numeric Fe/Al crossover τ* from Szargut + ISO 9223 data | Prints τ* interval; no assertion failures |

---

## Verification coverage

Everything T1-computable in the mathematical inventory is verified by the scripts above. The open conditions are genuinely open — the required inputs do not exist yet, not because a check has not been written.

| What is verified | What is open | Separation mechanism |
| :--- | :--- | :--- |
| Dimensional homogeneity of all entropy chains | $\Omega_\mathcal{G}$ phase-space definition (OQ-GSH.17) | Computability tier index (M:§0) |
| Algebraic structure of all operative formulas | $f(\tau)$ scaling form in Gibbs bound (OQ-GSH.18) | T1/T2/T3 tier labels on every formula |
| Boundary behaviour: $n=0$ collapse, $\tau \to 0$ direction, TUR magnitude | $X(\tau)$ transition count for specific $\mathcal{G}$ (OQ-GSH.26) | Open verification obligations table (M:§9) |
| Fe/Al crossover $\tau^*$ numeric instance | General $\Sigma_g$ computation for arbitrary $\mathcal{G}$ (OQ-GSH.1) | `fe_crossover_numeric.py` is one instance, not a general solver |

---

## Dimensional fixes

The core inequality $\Sigma_g(\mathcal{G}, \tau) < \Sigma_s(x, \tau)$ requires both sides in $\text{J}\cdot\text{K}^{-1}$. Three gaps were closed during development that made the dominance test formally undefined before the fix:

| Gap | Formula affected | Fix |
| :--- | :--- | :--- |
| Surface area $A$ $[\text{m}^2]$ absent from corrosion chain | $\Sigma_s$ direct chain (M:§3.1) | $A$ added; chain closes $\text{W}\cdot\text{K}^{-1} \times \text{s} \rightarrow \text{J}\cdot\text{K}^{-1}$ |
| $n(x,\tau)$ $[\text{mol}]$ absent from Gibbs upper bound | $\Sigma_s^{\max}$ (M:§1.6) | $n$ added; closes $\text{J}\cdot\text{mol}^{-1}\cdot\text{K}^{-1} \times \text{mol} \rightarrow \text{J}\cdot\text{K}^{-1}$ |
| TUR rate form ($\text{J}\cdot\text{K}^{-1}\cdot\text{s}^{-2}$) used instead of cumulative | $\Sigma_g^{\min}$ (M:§1.6) | Replaced with Barato-Seifert 2015 cumulative form: $2k_B / \epsilon^2$; units $\text{J}\cdot\text{K}^{-1}$ |

To verify independently: run `python3 tools/verify_dim_homogeneity.py` (check A2 for corrosion chain, check B for TUR cumulative vs. rate form, check DH_GATE for simultaneous closure of all three chains) and `python3 tools/verify_gsh_math.py` (checks 11–13). The Mermaid diagram in M:§8.4 shows the three normalisation chains (A, B, C) whose node names correspond directly to the script check labels.

---

## Derived analysis

`derived_analysis/` applies the hypothesis to specific engineering contexts.

| File | Content |
| :--- | :--- |
| [element_derivation_process.md](derived_analysis/element_derivation_process.md) | Elimination trace for $\mathcal{E}^*(\mathcal{F}_{\mathrm{space}})$ — space engineering context. Records which elements were eliminated at which criterion and why. Computable counterpart: `derive_element_set.py`. |
| [solar_thermal_loop_analysis.md](derived_analysis/solar_thermal_loop_analysis.md) | Application of Axiom II and the $\Sigma$ inequality to a solar thermal loop — tests a specific subsystem against the framework. Computed numbers are transcluded from `solar_thermal_loop_computed.md`; never edit them by hand. |
| `solar_thermal_loop_calc.py` | Authoritative arithmetic for `solar_thermal_loop_analysis.md` — all Layer 0 constants, §4.4/§4.7/§4.8/§4.10/§4.11 calculations using sympy exact rationals. Run `python3 solar_thermal_loop_calc.py` to regenerate `solar_thermal_loop_computed.md`. |
| `solar_thermal_loop_computed.md` | Generated file — do not edit by hand. Produced by `solar_thermal_loop_calc.py`. Carries `unlisted: true` for Quartz transclusion. |
| `derive_element_set.py` | Applies the criteria hierarchy computationally over a 26-element library with deployment constants fixed at $\tau = 100\,\text{yr}$, $T_0 = 250\,\text{K}$. Produces $\Sigma$ comparison numbers where T1-computable. |

**Status:** Concept established and consistent with the hypothesis framework. LaTeX formatting and prose editing are ongoing. Read as application examples, not as claims under the same evidentiary standard as the primary documents.

---

## Audit methodology

The argument structure audit tools used to develop and maintain these documents are in a separate repository: [argument-structure-audit](https://github.com/alan-sudoku/argument_structure_audit).

---

## Versioning

Two-part versioning: **major** on new top-level section or axiom added — the only event that changes what the hypothesis is; **minor** per working session that produces a structural change to an argument (author judgment — retraction log entries do not individually trigger it). The retraction log is the authoritative record of what changed, not a version counter.

---

## Status

Working document. No institutional affiliation. The argument structure is present in full at its current version. The open questions (H:§7) are pre-audit challenge conditions — each names the hidden assumption a common rebuttal must resolve before the rebuttal is structurally valid. Two are load-bearing: **Challenge A** (magnetism gap — whether ferromagnetism has a geometric substitute at ambient temperature) and **OQ-GSH.1** (general $\Sigma_g$ computability — whether the full crossover calculation is tractable for arbitrary element-geometry pairs).
