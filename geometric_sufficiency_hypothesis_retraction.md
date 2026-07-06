---
title: The Geometric Sufficiency Hypothesis — Retraction Log
description: Every retracted claim from geometric_sufficiency_hypothesis.md — what was probed and found structurally defective after adversarial audit
---

# The Geometric Sufficiency Hypothesis — Retraction Log

Every retracted claim from [geometric_sufficiency_hypothesis.md](geometric_sufficiency_hypothesis.md). The log is the negative channel of the document — what was probed and found structurally defective after adversarial audit. It carries boundary information: what the hypothesis cannot claim constrains what it can claim.

**Entry format:** ID · Source · Date · Audit trigger · Why retracted · Exact retracted content · What replaces it · Exploration value

**Entry types:**
- **§Rxx — retraction:** content removed or replaced because it was wrong. Use when a claim, scope, or pointer is false or indefensible.
- **§Axx — amendment:** underlying direction correct; exposition was imprecise. Use when a precision addition closes an attack or resolves an ambiguity without retracting the direction.

**Section reference convention:** Bare `§N` refers to `geometric_sufficiency_hypothesis.md`. `M:§N` refers to `GSH_mathematical_inventory.md`. Both files are in the same directory as this log.

---

## Index

| ID | Description | Source | Date | Audit trigger |
| :--- | :--- | :--- | :--- | :--- |
| §A01 — notation system | $S$/$S^*$/$\Omega$ replaced with $\mathcal{E}$/$\mathcal{E}^*$/$\Sigma$ throughout | §0–§7, all OQs | 2026-06-03 | Gemini blank-read audit; notation deconflict staging entry |
| §A02 — OQ-GSH.8 | OQ-GSH.8 epistemic status amended: open quantitative question → unresolved veto precondition | §7 | 2026-06-04 | Criterion 2 reclassification triggered OQ-GSH.8 status review |
| §A03 — Conjecture → Hypothesis rename (Pass 3 + Pass 2 amendment) | Title, prose, epistemic key: "Conjecture" → "Hypothesis"; "(C) Conjecture" → "(H) Hypothesis" throughout; Q-GSC → Q-GSH and OQ-GSC → OQ-GSH in all live files (pass 2 clean-break) | §0–§7, all OQs, all live files | 2026-06-04 | Confirmed rename decision; OQ namespace clean-break pass 2 |
| §A04 — OQ-GSH.7 restructure | OQ-GSH.7 binary bootstrap question → four-tier (T1–T4) verification ladder; Gradient Locality named as open sub-condition | §7 | 2026-06-04 | Bootstrap architecture decision confirmed |
| §A05 — dimensional homogeneity of $\Sigma_s$ and $\Sigma_g$ | Three dimensional gaps in the dominance test closed: $A$ [m²] in corrosion chain, $n(x,\tau)$ [mol] in Gibbs bound, TUR rate form → cumulative form; DH_GATE confirmed | `GSH_mathematical_inventory.md` M:§1.6, M:§2.2, M:§0, M:§8.5 | 2026-06-05 | External math audit; `verify_dim_homogeneity.py` constructed |
| §R06 — Criterion 2 (Self-Passivation) retired as veto | Self-passivation removed from the criteria hierarchy entirely; corrosion cost routed exclusively to $r_{\text{corr}}(x) \cdot \tau$ inside $\Sigma_s$ | §4 table, §4 intro, §5 Fe note, §6 Challenge A, OQ-GSH.8 | 2026-06-07 | Internal argument audit; finding C1 — CRITICAL contradiction |
| §A08 — Blank-AI readability pass 1: six exposition fixes | Six blank-AI readability fixes: dominance test bound logic, Dirac delta glossary, obligation label residue, unexpanded abbreviations, draft/history language, $b_{ch}$ notation | `GSH_mathematical_inventory.md` M:§1.4, M:§1.6, M:§4.2, M:§8 | 2026-06-10 | External blank-AI audit (pass 1) |
| §A09 — Blank-AI readability pass 2: twelve inventory fixes + four hypothesis fixes | Twelve inventory fixes: cryogenic crossover direction, undefined OQ code, dominance test routing in three diagrams, editorial language, two S1 glossary gaps, canonical notation alignment, four-regime crossover table, Axiom II joint condition table, V-conditions modularity. Four hypothesis fixes: L-BT Ca exclusion merge + draft block deletion, two OQ pointer swaps, bare Q- prefix | `GSH_mathematical_inventory.md` M:§1.6, M:§4.2, M:§6.1, M:§7, M:§8; `geometric_sufficiency_hypothesis.md` H:§3, H:§5 | 2026-06-10 | External blank-AI audit (pass 2) |
| §A10 — Blank-AI readability pass 3: three symbol and constraint fixes | Three inventory fixes: $r_s$/$r_g$ slope symbols renamed to $\dot{\Sigma}_s$/$\dot{\Sigma}_g$ in M:§1.6; $r_{\text{corr}}$ definition aligned to entropy-rate units at both glossary sites and §1.1; $\Delta G_{\text{recovery}}$ constraint cell corrected from $\leq 0$ to sign-unconstrained | `GSH_mathematical_inventory.md` M:§1.1, M:§1.6, M:§4.2, M:§7 | 2026-06-11 | External blank-AI audit (pass 3) |
| §A11 — Three precision additions from partial-information audit | (1) TUR vs Boltzmann-Shannon computability distinction surfaced at M:§1.6; (2) $\Sigma_s^{\max}$ code-consumer inversion warning added; (3) $r_{\mathrm{corr}}$ ISO 9223 abiotic scope stated | `GSH_mathematical_inventory.md` M:§1.6, M:§1.1 symbol row | 2026-07-04 | External partial-information AI audit (math inventory only) |

---

## §A01 — Notation system (Pass 1 and Pass 2)

**Source:** §0 scope, §1 Ω trade-off argument, §2 Axiom I, §3 Requirement 1, §4 intro and header, §5 Earth derivation, §7 OQ-GSH.9/10 — all sections
**Date:** 2026-06-03
**Audit trigger:** Gemini blank-read audit identified three notation collisions

**Why amended:** Three collisions in the original notation system:
1. $S$ and $S^*$ — collides with $S$ for thermodynamic entropy (universal convention)
2. $\Omega_s$, $\Omega_g$ — collides with $\Omega$ as microstate count in Boltzmann's $S = k_B \ln \Omega$ (statistical mechanics universal convention)
3. $G$ for geometric arrangement — collides with $G$ for Gibbs free energy (chemistry/engineering universal convention)

Root cause: $S$ was allocated to the element set first; entropy was displaced to $\Omega$ to avoid the $S$ collision, which then collided with the microstate symbol.

**Exact replaced notation:**

| Was | Now | Scope |
| :--- | :--- | :--- |
| $S$, $S^*$ | $\mathcal{E}$, $\mathcal{E}^*$ | Element set and optimal element set — all occurrences |
| $F$, requirement set | $\mathcal{F}$ | Functional requirement set — all occurrences |
| $G$, arrangement | $\mathcal{G}$ | Geometric arrangement — all occurrences |
| $\Omega_s(x)$ | $\Sigma_s(x, \tau)$ | Supply-chain entropy cost — all occurrences; τ now explicit in signature |
| $\Omega_g(G)$ | $\Sigma_g(\mathcal{G}, \tau)$ | Geometric maintenance entropy cost — all occurrences |
| $\Omega_g = \infty$ | $\Sigma_g \to \infty$ | Hard gap condition |
| $\Omega_s + \Omega_g$ | $\Sigma_s + \Sigma_g$ | Sum expressions |
| $\Omega_t$ | $\Sigma_t$ | Transition entropy variable (OQ-GSH.10) |

**What replaces it:** Calligraphic set grammar ( $\mathcal{E}$, $\mathcal{F}$, $\mathcal{G}$ ) following standard mathematical convention. $\Sigma_s$ and $\Sigma_g$ denote accumulated entropy generation — equivalent to $S_{\text{gen},s}$ and $S_{\text{gen},g}$ in standard engineering thermodynamics (Bejan, Moran & Shapiro). $\Sigma$ is used as a named accumulation function, not a summation operator.

**Direction retained:** All claims, axioms, obligations, and veto logic are unchanged. This is a notation substitution only — no argument content was altered.

**Exploration value:** The $\tau$ parameter is now explicit in $\Sigma_s(x, \tau)$ and $\Sigma_g(\mathcal{G}, \tau)$, reinforcing the τ-scaling argument (MDL-1 in staging) — the inequality is visibly time-dependent, not a static comparison.

**Pass 3 pending:** Title and prose rename (Conjecture → Hypothesis) is a separate §Axx entry, held pending rename decision confirmation.

---

## §A02 — OQ-GSH.8 epistemic status amendment

**Source:** §7 OQ-GSH.8
**Date:** 2026-06-04
**Audit trigger:** Criterion 2 reclassified from Hard veto to Functional (closed-loop) / Hard (open-loop) — OQ-GSH.8 status review triggered

**Why amended:** OQ-GSH.8 originally asked for the operational lifetime threshold τ below which Fe's Criterion 2 failure is outweighed by geological abundance — framed as an open quantitative question, post-hoc to the veto decision. The Criterion 2 reclassification decision established it as a functional veto in closed-loop contexts; the τ threshold is no longer a curiosity — it is the required input to the functional veto calculation. A question that frames τ as an optional refinement is now structurally imprecise.

**Exact replaced content:** `On Earth, what is the operational lifetime threshold τ below which Fe's Criterion 2 corrosion failure is outweighed by its geological abundance and processing simplicity, making Fe a valid S* member for short/medium-duration industrial applications?`

**What replaces it:** Question reframed to name the Σ crossover as the veto precondition and supply closed-loop qualifier: `**[Unresolved veto precondition — status promoted by Criterion 2 reclassification]** At what τ does $\Sigma_s(\text{Fe}, \tau)$ — extraction + processing + corrosion maintenance $r_{\text{corr}} \cdot \tau$ + Axiom II recycling obligation $\Sigma_{\text{rec}}(\text{Fe})$ — cross $\Sigma_g(\mathcal{G}_{\text{sub}}, \tau)$ for the lowest-entropy available geometric substitute (candidate: $\mathcal{G}_{\text{Al}}$ or $\mathcal{G}_{\text{C}}$)? Below this crossover τ, Fe satisfies the Criterion 2 functional veto and is a valid $\mathcal{E}^*$ member for that problem in closed-loop contexts. This is a required input for Fe inclusion/exclusion decisions — not an optional quantitative refinement.`

**Direction retained:** The question survives; its epistemic role is elevated from research curiosity to veto precondition. No claim is retracted.

**Exploration value:** Operationalising this crossover is the direct path to making Criterion 2's functional veto layer computable. The Σ crossover formula (τ* = (Σ_cap_g − Σ_cap_s) / (r_s − r_g)) from verify_gsc_math.py check 7 provides the algebraic structure; the open research gap is the supply-chain data for r_corr and Σ_rec(Fe) at representative scale.

---

## §A03 — Conjecture → Hypothesis rename (Pass 3)

**Source:** Title, §0 scope header, §1 Claim paragraph, §1 arguments, §1 scope nodes, §2 axiom scope notes, §5 terrestrial derivation, §6 challenge table footer, epistemic key — all occurrences
**Date:** 2026-06-04
**Audit trigger:** Rename decision confirmed — all candidate options agreed on this minimum change

**Why amended:** "Conjecture" in the mathematical sense implies a known falsification condition and a proof-gap as the only remaining open status. The document does not currently have a computable falsification condition — §1 Claim is an existence posit, not a proved theorem with a known gap. "Hypothesis" is the epistemically accurate term: testable in principle, physically grounded, not yet verified. The rename does not weaken the existence claim; it accurately represents the document's epistemic role.

**Exact replaced symbol:**

| Was | Now | Scope |
| :--- | :--- | :--- |
| Conjecture (capital C in prose) | Hypothesis (capital H in prose) | All prose references — "the Conjecture's claim scope", "a conjecture-following AI", etc. |
| conjecture (lowercase in prose) | hypothesis (lowercase in prose) | "outside the conjecture's domain", "the conjecture is deferred", "failures of the conjecture", etc. |
| `*(C) Conjecture*` | `*(H) Hypothesis*` | Epistemic status key entry |
| `The Geometric Sufficiency Conjecture (GSC)` | `The Geometric Sufficiency Hypothesis (GSH)` | Document title (H1) |
| `(GSC)` initialism in title | `(GSH)` initialism in title | Title line only |

**OQ code rename (pass 2 amendment):** OQ-GSC codes renamed to OQ-GSH throughout all live files (source, retraction log, math spec, audit prompt) as part of the clean-break rename decision in pass 2. Archived files retain original OQ-GSC codes as historical records. The GSC/GSH namespace split is now fully resolved — all live codes use the GSH namespace.

**Direction retained:** All claims, axioms, obligations, veto logic, and OQ entries are unchanged. This is a terminology substitution only.

**Exploration value:** The rename makes the document's epistemic position legible to readers familiar with the conjecture/hypothesis distinction in mathematics and philosophy of science. It also removes the implicit claim that a proof-gap is the only thing separating the document from a theorem — the research agenda is broader than gap-closing.

---

## §A04 — OQ-GSH.7 restructure

**Source:** §7 OQ-GSH.7
**Date:** 2026-06-04
**Audit trigger:** Bootstrap architecture decision confirmed — OQ-GSH.7 restructured from a single binary question to a four-tier verification structure

**Why amended:** OQ-GSH.7 originally asked "Is ℰ* sufficient to construct the flux-interception and recycling infrastructure required by Axioms II and III?" as a single binary open question, with the Solar-Thermal Bootstrap Loop as a candidate test. The confirmed architecture decision restructures the verification pathway into four discrete tiers (T1–T4), each independently valuable, each anchored to physical thresholds of ℰ* elements, and each confirming a distinct sub-claim. The original single-question framing collapses four independent research targets into one answer that may never arrive. Restructuring OQ-GSH.7 around the tier ladder makes the question answerable in stages and each positive result carries standalone scientific value.

**Exact replaced content:** `Is $\mathcal{E}^*$ sufficient to construct the flux-interception and recycling infrastructure required by Axioms II and III without importing elements outside the set? What is the minimum EROI threshold at which the self-sustaining loop is positive? *Candidate loop:* Solar-Thermal Bootstrap Loop — Compound Parabolic Concentrators (CPCs; Al/Ag reflectors, no tracking required) intercept solar flux → SiC absorber at focal point → Na/K heat-transfer loop to thermochemical reactor → direct thermal dissociation drives element recycling → geopolymer cold-casting (ℰ* = {Al,Si,O,Na,K}) scales concentrator infrastructure.`

**What replaces it:** Four-tier verification ladder with physical anchors, independent confirmation value per tier, and explicit Gradient Locality sub-condition. Full replacement text committed to source.

**Direction retained:** The bootstrap loop question survives — it is T4 of the new ladder. T1/T2/T3 are not retractions of OQ-GSH.7; they are decompositions of its sub-problems into independently testable claims. The Gradient Locality sub-condition is named as open but does not block T1/T2 confirmation.

**Exploration value:** The T1 tier (200–300°C, non-tracking CPC, solar thermal at 200°C demonstrated technology) is already physically competitive with fossil-fuel alternatives. Restructuring OQ-GSH.7 around the tier ladder converts an abstract sufficiency question into a concrete engineering research agenda with commercial-scale relevance at the lowest tier.

---

## §A05 — Dimensional homogeneity of $\Sigma_s$ and $\Sigma_g$

**Source:** `GSH_mathematical_inventory.md` M:§1.6 (Gibbs bound, TUR bound), M:§2.2 (Axiom II thermodynamic condition), M:§0 tier table (TUR row), M:§8.5 (Chain A node A4, Chain C, DH_GATE edge)
**Date:** 2026-06-05
**Audit trigger:** External math audit; `verify_dim_homogeneity.py` constructed as machine-verification counterpart

**Why amended:** The dominance test — the only currently computable approximation of $\Sigma_g < \Sigma_s$ — compares $\Sigma_g^{\min}$ (TUR bound) against $\Sigma_s^{\max}$ (Gibbs bound). Both bounds were in wrong units before this fix. The comparison was formally undefined: any numeric result from it was a category error regardless of the argument structure around it. Three independent dimensional breaks were identified and closed.

**Exact replaced content:**

| Gap | Pre-fix form | Post-fix form |
| :--- | :--- | :--- |
| Surface area $A$ absent from corrosion chain (M:§3.1) | Chain closed at W m⁻² K⁻¹ — never reached J K⁻¹ | $A$ [m²] added; chain closes W K⁻¹ × s → J K⁻¹ |
| $n(x,\tau)$ absent from Gibbs bound (M:§1.6) | $\Delta G / T \cdot f(\tau)$ → J mol⁻¹ K⁻¹ (per-mole, not total) | $\cdot\, n(x,\tau)$ [mol] added; closes J mol⁻¹ K⁻¹ × mol → J K⁻¹ |
| Axiom II extensive form (M:§2.2) | LHS $\Delta G_{\text{recovery}}$ [J mol⁻¹] vs RHS $\dot{Q} \cdot \tau_{\text{recovery}}$ [J] — incommensurable | RHS divided by $n_{\text{rec}}(x)$ [mol]; both sides J mol⁻¹ |
| TUR rate form (M:§1.6, M:§0) | $2k_B J^2 / (\operatorname{Var}/\langle X\rangle^2)$ → J K⁻¹ s⁻² | Barato-Seifert 2015 cumulative form: $2k_B / \epsilon^2$ → J K⁻¹ |

**What replaces it:** Corrected formula bodies in M:§1.6 and M:§2.2. M:§8.5 Chain C rewritten around the cumulative TUR form (nodes C1–C7); DH_GATE edge changed from dashed (conditional) to solid (confirmed). M:§0 tier table TUR row updated to cumulative form. New symbol rows $n(x,\tau)$, $n_{\text{rec}}(x)$, $X(\tau)$, $\epsilon^2$ added to M:§1.1 symbol table.

**New open condition registered:** OQ-GSH.26 — $X(\tau)$, $\langle X(\tau)\rangle$, $\operatorname{Var}(X(\tau))$ require definition for a specific $\mathcal{G}$ before the TUR bound is numerically usable. Companion to OQ-GSH.17 ( $\Omega_\mathcal{G}$ phase-space definition).

**Direction retained:** The argument structure, axiomatic content, and all claim directions are unchanged. The dominance test was always the intended instrument; this amendment establishes that it is a valid operation. No claim is retracted.

**Exploration value:** The DH_GATE is now confirmed. The remaining open conditions blocking numeric use of the dominance test are definitional (OQ-GSH.26, OQ-GSH.18), not dimensional. The boundary between what is closed and what is open is now machine-verifiable: `python3 tools/verify_dim_homogeneity.py` exits 0 on all 14 checks.

---

## §R06 — Criterion 2 (Self-Passivation) retired as veto condition

**Source:** §4 table row 2, §4 intro, §5 Fe table entry, §5 Fe scope note, §6 Challenge A candidate resolution, OQ-GSH.8
**Date:** 2026-06-07
**Audit trigger:** Internal argument audit; finding C1 — CRITICAL contradiction

**Why retracted:** Criterion 2 double-handled the corrosion cost variable. The mathematical inventory (§3.1, §4.2) already encodes corrosion correctly as $r_{\text{corr}}(x) \cdot \tau$ inside $\Sigma_s(x, \tau)$:

$$\Sigma_s(\text{Fe}, \tau) = \Sigma_s^{\text{extraction}} + r_{\text{corr}} \cdot \tau + \Sigma_{\text{rec}}(\text{Fe})$$

Self-passivation is one environment-conditioned mechanism that determines the *magnitude* of $r_{\text{corr}}$ for a specific element-environment pair — one of several (surface coating, cathodic protection, environmental control). Placing self-passivation as a binary veto before the inequality is evaluated means: (1) the corrosion cost is assessed twice — once as a gate, once inside $\Sigma_s$; (2) the gate pre-empts the inequality for valid engineering trade-offs (e.g., a coating strategy that reduces $r_{\text{corr}}$ and passes the inequality would be blocked by the veto before evaluation); (3) the open-loop/closed-loop classification created a false binary in place of what is a continuous $r_{\text{corr}}$ variable set by deployment environment.

The architectural root: the original hypothesis framing was intuitive — propose a set, veto with criteria. Once the $\Sigma$ inequality became the operative decision rule, criteria should have been relabelled as named boundary conditions (limiting cases of the inequality), not retained as an independent decision layer preceding it. Criterion 2 was the clearest instance of this structural error because its subject matter — corrosion — was already correctly inside the math.

**Exact retracted content:**

*§4 table row 2 (original):*
> `| 2 | Self-Passivation | Functional (closed-loop) / Hard (open-loop) | Closed-loop: Σ_g(G_sub, τ) < Σ_s(Fe, τ) — corrosion maintenance rate r_corr · τ compounded with Axiom II deferred recycling debt Σ_rec(Fe); applies only where r_corr is stable and products are contained. Open-loop / dispersive / catastrophic-regime: hard veto — Axiom II recovery pathway not feasible | ... |`

*§4 intro paragraph (original):*
> "Criterion 2 (Self-Passivation) is a τ-conditional functional veto: corrosion-driven maintenance entropy is finite and τ-dependent, accruing as an Axiom II deferred debt from the start of operation regardless of decommissioning timing. The veto fires when a geometric substitute satisfies Axiom I's inequality over the problem's τ. This functional classification applies only in closed-loop contexts where the corrosion regime is passivation-limited and products are contained; open-loop or dispersive environments retain Criterion 2 as a hard veto."

**What replaces it:** Corrosion cost is handled exclusively by $r_{\text{corr}}(x)$ as a deployment-fixed input (ISO 9223 data) inside $\Sigma_s(x, \tau)$. The general inequality evaluates the full trade-off for any element-environment pair without a classification gate. Self-passivation, coating, cathodic protection, and environmental control are alternative mechanisms that reduce $r_{\text{corr}}$ for a given pair — each adds its own $\Sigma_g$ cost, which the inequality also evaluates. The §4 criteria count is reduced from ten to nine; the table row is struck through and marked retired with a pointer to the §4 intro scope note.

**Downstream corrections applied:**
- §4 section heading and ToC entry: "ten sequential vetoes" → "nine criteria"
- §4 intro: criteria list updated to remove Criterion 2 from the functional veto group
- §3 Obligation 2 example: "weights Criteria 2 and 4" → "weights Criterion 4 and the corrosion term in $\Sigma_s$"
- §3 Obligation 4 contextual optimality example: "fails Criterion 2 for long-duration structures" → "carries high $r_{\text{corr}}$ term in $\Sigma_s$ for long-duration structures in corrosive environments"
- §5 elimination trace Fe row, §5 Fe scope note, §6 Challenge A Fe re-entry argument, OQ-GSH.8: all Criterion 2 references replaced with general inequality framing
- §A02 entry in this log: now superseded — OQ-GSH.8's framing as "unresolved veto precondition" predated this retraction; OQ-GSH.8 now refers to the general inequality crossover $\tau^*$ without a veto framing
- Review flags added to `element_derivation_process.md` and `derived_analysis/solar_thermal_loop_analysis.md`

**Exploration value:** Retiring Criterion 2 as a veto has two consequences for the hypothesis's claim space. First, the open-loop/closed-loop classification disappears — replacing a false binary with a continuous environmental variable ( $r_{\text{corr}}$) makes the Fe inclusion/exclusion question fully computable once OQ-GSH.8 is resolved. Second, the architectural diagnosis generalises: the GSH is a thermodynamic budgeting framework, not a veto hierarchy. Every remaining "hard veto" criterion (1, 3, 4, 5) is a named limiting case of the inequality ( $\Sigma_s \to \infty$ or $\Sigma_g \to \infty$ for all $\mathcal{G}$). The criteria are navigation aids, not an independent decision layer.

---

## §A07 — Seven math fixes from external audit (Fixes 1–7)

**Source:** `GSH_mathematical_inventory.md` M:§2.2, M:§1.6, M:§4.1, M:§3 Requirement 1, M:§6.1, M:§1.1 symbol table
**Date:** 2026-06-05
**Audit trigger:** External math audit; `verify_dim_homogeneity.py` and `verify_gsh_math.py` constructed as verification artefacts

**Why amended:** Seven distinct gaps identified by the external auditor. In each case the underlying direction was correct; the formulation was incomplete or imprecise.

---

**Fix 1 — Kinetics gap in Axiom II**

*Gap:* Axiom II tested only the thermodynamic condition $\Delta G_{\text{recovery}} \leq \dot{Q}_{\text{ambient}} \cdot \tau_{\text{recovery}}$. A recovery loop kinetically inert at all $\mathcal{E}^*$-accessible temperatures would pass — thermodynamic feasibility does not guarantee a non-zero reaction rate.

*Exact replaced content (M:§2 Axiom II operative test):*
> $\Delta G_{\text{recovery}} \leq \dot{Q}_{\text{ambient}} \cdot \tau_{\text{recovery}}$ (single condition)

*What replaces it:* Two-condition operative test: (i) $\Delta G_{\text{recovery}} \leq \eta_{\text{ex}} \cdot \dot{Q}_{\text{ambient}} \cdot \tau_{\text{recovery}} / n_{\text{rec}}$ (thermodynamic; $\eta_{\text{ex}}$ added by Fix 7); (ii) $v_{\text{recovery}} \geq v_{\text{min}}(\mathcal{G}, \tau)$ using only catalysts and infrastructure within $\mathcal{E}^*$ (kinetic). OQs opened: OQ-GSH.15 (kinetic accessibility), OQ-GSH.16 (finite-time thermodynamics gap).

---

**Fix 2 — Boltzmann-Shannon bound regime scope**

*Gap:* The bound $k_B \ln(\Omega_\mathcal{G}) \cdot \tau / \tau_{\text{thermal}}$ was stated as a universal maintenance entropy lower bound with no regime qualification. Applying it to passive high-barrier structures ( $E_b \gg k_B T$) overestimates $\Sigma_g$ by orders of magnitude.

*Exact replaced content (M:§1.6 bounding method):*
> Single regime: $k_B \ln(\Omega_\mathcal{G}) \cdot \tau / \tau_{\text{thermal}}$ as universal lower bound

*What replaces it:* Three-regime split — active feedback (Sagawa-Ueda); active sustained-current (TUR); passive high-barrier ( $\Sigma_{g,\text{maintenance}} \approx 0$). OQs opened: OQ-GSH.17 ( $\Omega_\mathcal{G}$ phase-space definition), OQ-GSH.18 ( $f(\tau)$ form for Gibbs bound).

---

**Fix 3 — "Reversible" term ambiguity in Criterion 4**

*Gap:* Criterion 4 used "reversible" without qualification — the word carries two incompatible senses in thermodynamics: $\Delta S_{\text{gen}} = 0$ (unachievable in any real process) and mass recovery (the engineering criterion intended).

*Exact replaced content (M:§4 Criterion 4):*
> "reversible recovery loop"

*What replaces it:* "mass recovery rate $\geq 99.9\%$ per cycle using ambient flux, and recovery loop not kinetically inert at $\mathcal{E}^*$-accessible conditions." Thermodynamic reversibility removed from this criterion; covered by Axiom II directly.

---

**Fix 4 — TUR bound missing for sustained-current active regime**

*Gap:* Sagawa-Ueda was the sole lower bound stated for all active maintenance. For sustained-current steady states (dynamic electromagnetic traps, powered non-equilibrium assemblies), TUR gives a tighter bound; Sagawa-Ueda requires a discrete measurement-feedback cycle and does not apply to continuous driving.

*Exact replaced content (M:§1.6 active regime):*
> Single active bound: Sagawa-Ueda $k_B \ln(\Omega_\mathcal{G}) / \tau_{\text{thermal}}$ for all active maintenance

*What replaces it:* Active regime split into two sub-cases — feedback-correction (Sagawa-Ueda) and sustained-current (TUR: $\dot{S}_{\text{gen}} \geq 2 k_B J^2 / (\operatorname{Var}(\hat{X}) / \langle X \rangle^2)$).

---

**Fix 5 — Exergy normalisation basis not stated**

*Gap:* M:§3 Requirement 1 described the computation obligation without committing a normalisation basis for $\Sigma_s$ and $\Sigma_g$. The reference state for the exergy calculation was unstated, leaving the dimensional homogeneity gate ungrounded.

*Exact replaced content (M:§3 Requirement 1):*
> Computation obligation stated without naming the normalisation basis

*What replaces it:* Exergy $B = H - T_0 S$ committed as the normalisation basis for both $\Sigma_s$ and $\Sigma_g$. Both in Joules; dimensional homogeneity confirmed by `verify_dim_homogeneity.py`. No new OQs opened.

---

**Fix 6 — M:§6.1 cryogenic crossover formula algebraic error**

*Gap:* M:§6.1 formula $\tau^* = \Sigma_s(\text{Fe}) / (\dot{\Sigma}_g - \dot{\Sigma}_s(\text{Fe})) < 0$ is algebraically inconsistent: with $\Sigma_s(\text{Fe}) > 0$ and $\dot{\Sigma}_g > \dot{\Sigma}_s$ (established by COP = 0.064 at 18 K), the ratio is positive, contradicting the asserted $\tau^* < 0$. The single-term model collapses the two-intercept structure.

*Exact replaced content (M:§6.1 formula):*
> $\tau^* = \Sigma_s(\text{Fe}) / (\dot{\Sigma}_g - \dot{\Sigma}_s(\text{Fe})) < 0$

*What replaces it:* Two-intercept crossover model: $\tau^* = (\Sigma_{s,\text{initial}} - \Sigma_{g,\text{mfg}}) / (\dot{\Sigma}_g - \dot{\Sigma}_s)$. The $\tau^* < 0$ condition correctly stated as requiring $\Sigma_{g,\text{mfg}} > \Sigma_{s,\text{initial}}$. OQ opened: OQ-GSH.31 (cryogenic envelope intercept condition — rate condition established by COP; intercept condition empirically open).

---

**Fix 7 — Axiom II thermodynamic condition missing exergy efficiency factor**

*Gap:* M:§2.2 used $\dot{Q}_{\text{ambient}}$ (incident flux power) directly as the available energy budget. Converting radiant or thermal flux to chemical work is bounded by efficiency limits: Landsberg ( $\approx 0.93$) for solar radiation, Carnot for thermal gradients, quantum efficiency for photochemical pathways. The gate was optimistic for borderline candidates without the factor.

*Exact replaced content (M:§2.2 Axiom II formula):*
> $\Delta G_{\text{recovery}} \leq \dot{Q}_{\text{ambient}} \cdot \tau_{\text{recovery}} / n_{\text{rec}}$

*What replaces it:* $\Delta G_{\text{recovery}} \leq \eta_{\text{ex}} \cdot \dot{Q}_{\text{ambient}} \cdot \tau_{\text{recovery}} / n_{\text{rec}}$. Symbol $\eta_{\text{ex}}$ added to M:§1.1 symbol table. OQ opened: OQ-GSH.32 (three open conditions: operative conversion pathway per element, $\eta_{\text{theoretical}}$ at deployment conditions, materiality threshold).

---

**Exploration value:** The seven amendments collectively reveal the difference between a *structurally coherent* formulation and a *computationally closed* one. Each fix adds a condition that was implicitly assumed but not stated: a kinetic gate, a regime boundary, an unambiguous term, a tighter bound for a sub-regime, a normalisation reference, an algebraic two-intercept structure, and an efficiency ceiling. The core inequality and the three-regime $\Sigma_g^{\min}$ structure survive all seven unchanged. What changes is the set of conditions that must be verified before the inequality is applied — all seven OQs opened by these fixes are blocking conditions on specific pipeline paths, not on the framework's existence posit.

---

## §A08 — Blank-AI readability pass 1: six exposition fixes

**Source:** `GSH_mathematical_inventory.md` M:§1.4, M:§1.6, M:§4.2, M:§8 (all subsections)
**Date:** 2026-06-10
**Audit trigger:** External blank-AI readability audit, pass 1

**Why amended:** Six findings identified by blank-AI audit where a reader without prior context would misroute or misinterpret content.

| Fix | Finding class | What changed |
| :--- | :--- | :--- |
| 1 | C6 — direction error | Dominance test label "geometry strictly cheaper" at lines 404, 711, Mermaid edge 1167: $\Sigma_g^{\min} < \Sigma_s^{\max}$ does not establish ordering when operating on bounds. Label replaced with "bounds do not disqualify geometry — overlap possible; proceed to full computation" |
| 2 | C9i — S1 gap | M:§1.4 Dirac delta formula: $\Sigma_s^{\text{mfg}}$, $\Sigma_s^{\text{decom}}$, $\delta(t)$ had no local glossary. Three glossary bullets inserted |
| 3 | C1/C7b — dead label | "obligation 1b" and "obligation 2" residue in eight locations (M:§1.6 source label, M:§1.6 prose, M:§8.1 CD-DG prose, three Mermaid node strings). Replaced with OQ-GSH.17 and OQ-GSH.18 throughout |
| 4 | C2 — undefined term | COP, CALPHAD, DFT, FEA, MEMS unexpanded at first use. Expansions added inline at first occurrence |
| 5 | C3 — workflow language | Two notes used internal staging language ("Committed fixes", "introduced as a committed repair"). Replaced with logical-state descriptions |
| 6 | C11c — notation | $b_{\text{ch}}$ at three locations; §1.1 canonical form is $b_{ch}$. Aligned to canonical form |

**Direction retained:** No claim, formula, or argument direction changed. All fixes are exposition corrections.

**Exploration value:** Fix 1 (dominance test label) corrects a persistent reader trap — the bound ordering error would cause any auditor reading the dominance test description to conclude geometry is conclusively cheaper when bounds overlap, which is the wrong routing decision.

---

## §A09 — Blank-AI readability pass 2: twelve inventory fixes + four hypothesis fixes

**Source:** `GSH_mathematical_inventory.md` M:§1.6, M:§2.2, M:§4.2, M:§6.1, M:§7, M:§8; `geometric_sufficiency_hypothesis.md` H:§3, H:§5
**Date:** 2026-06-10
**Audit trigger:** External blank-AI readability audit, pass 2; hypothesis document bug report

**Why amended:** Twelve inventory fixes and four hypothesis document fixes.

**Inventory fixes:**

| Fix | Finding class | What changed |
| :--- | :--- | :--- |
| 1 | C6 — direction inversion | Cryogenic crossover direction at M:§6.1 lines 869, 870, 977: "cryogenic substitute cheaper above $\tau^*$, Fe cheaper below" inverted. Corrected to: element cheaper above $\tau^*$, substitute cheaper below |
| 2 | C1 — dead pointer | `Q-GSH.7-KIN` undefined code in G1 failure mode and M:§8.1 prose. Replaced with canonical `OQ-GSH.15` |
| 3 | C6 — routing error | Dominance test `DOM→REMOVE` edge in three Mermaid diagrams (CD-DG, H-DFG, DAG) and Tr8 prose: overlap region routed directly to REMOVE. Corrected to `DOM→FullOPEN/CROSS` |
| 4 | C3/C8 — editorial language | Three M:§7 OQ table rows (OQ-GSH.17, OQ-GSH.18, OQ-GSH.25) used staging/editorial language. Replaced with logical-state descriptions |
| 5 | C9 — S1 gap | M:§6.1 magnetism gap formula: $\mu_r^{\text{ferromagnetic}}$ and $T_{\text{ambient}}$ had no local glossary. Two glossary bullets added |
| 6 | C9 — S1 gap | M:§6.1 cryogenic formula: $r_{\text{thermal load}}$ had no glossary entry. Glossary bullet appended |
| 7 | C11 — notation | $\Sigma_{ai}$ (24 occurrences) vs §1.1 canonical $\Sigma_{\text{ai}}$. Global sed replacement |
| 8 | C11 — notation | $\tau_{\text{rec}}$ at M:§1.6 line 400: non-canonical. Replaced with $\tau_{\text{recovery}}$ |
| 9 | C11 — notation | $\dot{S}_{\text{gen,maint}}$ at M:§1.4 line 353: non-canonical. Replaced with $\dot{S}_{\text{gen,maintenance}}$ |
| 10 | C6 — gap | Four-regime crossover enumeration absent from M:§1.6; only cryogenic case stated. Full regime table inserted with Computation and Pipeline routing columns |
| 11 | C6/C8 — structure | M:§2.2 Axiom II joint condition stated as bullet list; all three outcome combinations not enumerable. Replaced with 3-row 2×2 lookup table |
| 12 | C8 — structure | M:§6.5 V-conditions: consequence cells conflated diagnosis, severity, and action. Severity and Pipeline action columns added; V5/V7 extended content moved to notes |

**Hypothesis document fixes:**

| Fix | Finding class | What changed |
| :--- | :--- | :--- |
| 1 | Critical — duplicate block | Second L-BT bootstrap block (lines 391–400) was same scenario as corrected block but contained unique Ca exclusion condition. Ca exclusion merged as condition (vi) into corrected block; draft block deleted |
| 2 | Significant — wrong pointer | H:§3 Req.3 stop-search scope note: `OQ-GSH.5` → `OQ-GSH.20` |
| 3 | Significant — wrong pointer | H:§3 Req.3 W roadmap scope note: `OQ-GSH.6` → `OQ-GSH.5` |
| 4 | Minor — notation | Missing `OQ-` prefix on OQ-GSH.4 references at H:§2 lines 130, 137. Corrected to canonical `OQ-GSH.4` form |

**Direction retained:** No claim, formula, or argument direction changed in either document.

**Exploration value:** Fix 9 (four-regime crossover table) converts a single-instance example (cryogenic case) into a complete four-regime enumeration — a blank-AI reader can now classify any element–substitute pair by regime without reading the cryogenic prose first. Fix 1 in the hypothesis document (L-BT Ca exclusion merge) preserves a unique architectural constraint (Ca exclusion from the lunar bootstrap set) that would have been silently lost in a straight delete.

---

## §A10 — Blank-AI readability pass 3: three symbol and constraint fixes

**Source:** `GSH_mathematical_inventory.md` M:§1.1, M:§1.6, M:§4.2, M:§7
**Date:** 2026-06-11
**Audit trigger:** External blank-AI readability audit, pass 3

**Why amended:** Three symbol inconsistencies identified where a blank reader would encounter the same physical quantity under two different names, or a constraint cell that contradicts the operative formula.

| Fix | Finding class | What changed |
| :--- | :--- | :--- |
| 1 | C11 — symbol inconsistency | M:§1.6 affine model used $r_s$, $r_g$ as slope symbols; §1.1 defines $\dot{\Sigma}_s$, $\dot{\Sigma}_g$ for the same role; M:§6.1 already used the canonical form. Renamed throughout M:§1.6 formulas and regime table; S1 glossary added |
| 2 | C11 — unit inconsistency | $r_{\text{corr}}$ defined as m·s⁻¹ in M:§4.2 glossary and J·K⁻¹·s⁻¹ in M:§7 glossary; §1.1 entry gave no units. Aligned all three sites to J·K⁻¹·s⁻¹ (post-conversion rate) with explicit pointer to `fe_crossover_numeric.py` conversion chain |
| 3 | C6 — direction error | §1.1 constraint cell for $\Delta G_{\text{recovery}}(x)$ stated `$\leq 0$ required for thermodynamic feasibility`. M:§2.2 formula compares $\Delta G_{\text{recovery}}$ against a positive RHS — only meaningful for driven (positive $\Delta G$) recovery. Constraint cell replaced with "sign unconstrained; bounded by available ambient exergy — M:§2.2"; notes cell rewritten to distinguish spontaneous vs driven recovery |

**Direction retained:** No formula or argument direction changed. Fix 3 removes a constraint that contradicted the operative formula; the formula itself is unchanged.

**Exploration value:** Fix 1 ( $r_s$/$r_g$ → $\dot{\Sigma}_s$/$\dot{\Sigma}_g$ rename) eliminates the last symbol collision between M:§1.6 and the rest of the document. Fix 3 ( $\Delta G_{\text{recovery}}$ constraint) corrects a cell that would cause any reader to conclude that only exergetically spontaneous recovery reactions qualify under Axiom II — the exact opposite of the framework's intent for driven recovery processes.

---

## §A11 — Three precision additions from partial-information audit

**Source:** `GSH_mathematical_inventory.md` M:§1.6, M:§1.1 ( $r_{\mathrm{corr}}$ symbol row); `geometric_sufficiency_hypothesis.md` H:§1
**Date:** 2026-07-04
**Audit trigger:** External AI auditor reading only `GSH_mathematical_inventory.md` (hypothesis file withheld); three exposition gaps identified where correct content existed elsewhere but was not locally visible at point of use.

**Why amended:** All three fixes are additive precision notes. No formula, argument direction, or claim was wrong; the imprecision in each case was that a scope boundary or distinction was stated in one location but not surfaced at the location where a forward-pass reader would need it.

| Fix | Finding class | What changed |
| :--- | :--- | :--- |
| 1 | Computability conflation | M:§1.6 — TUR bound and Boltzmann-Shannon bound both carry tier T3 in M:§0 but have different practical blocking conditions. A computability note added between the TUR block and the passive-regime section: TUR ( $2k_B/\varepsilon^2$) is evaluable once $\mathrm{Var}(X(\tau))$ is measured (T3 = regime-scoped only); Boltzmann-Shannon is additionally blocked by $\Omega_{\mathcal{G}}$ having no formulated expression (OQ-GSH.17). Shared T3 label does not mean equally blocked. |
| 2 | Automated inversion risk | M:§1.6 $\Sigma_s^{\max}$ naming note — existing prose stated the "ceiling on cheapness" interpretation but did not warn that an automated code consumer reading $\Sigma_s^{\max}$ as a conventional cost ceiling would invert the dominance inequality direction. Code-consumer warning sentence added. |
| 3 | Abiotic source scope | M:§1.1 $r_{\mathrm{corr}}$ symbol row — ISO 9223 cited as data source without stating it is an abiotic (electrochemical, sterile environment) standard. MIC (microbiologically influenced corrosion) produces distinct kinetics not captured by ISO 9223. Note added: biotic deployment contexts require a separate corrosion rate model; pipeline structure unchanged — $r_{\mathrm{corr}}$ remains deployment-fixed regardless of which model populates it. |

**Direction retained:** No formula, OQ, or argument direction changed. All three fixes add local precision notes; the underlying framework content was correct throughout.

**Exploration value:** Fix 1 directly addresses a demonstrated auditor failure mode — the shared T3 label caused an independent reader to conflate TUR and Boltzmann-Shannon computability. Fix 2 converts a prose-only naming disambiguation into a code-path warning, extending the naming note's reach to automated consumers. Fix 3 closes a latent deployment-context error: a practitioner applying ISO 9223 values in a biotic context (water infrastructure, planetary greenhouse) would underestimate $r_{\mathrm{corr}}$ and obtain an optimistic crossover $\tau^*$.

---
