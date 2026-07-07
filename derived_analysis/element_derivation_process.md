---
title: Element Derivation Process — Space Engineering Context
description: Elimination trace for the minimum-cardinality element set at 3–5 AU — which elements were eliminated, at which criterion, and why
---

# Element Derivation Process — Space Engineering Context

*This file is the derivation record for* $\mathcal{E}^*(\mathcal{F}_{\mathrm{space}})$. *It records the elimination trace — which elements were eliminated, at which criterion, and why. The computable version is `tools/derive_element_set.py`: it runs the same criteria hierarchy with deployment constants fixed as module-level constants, applies the OQ-GSH.25 recyclability formula in place of the static 99.9% proxy, and produces Σ comparison numbers where computable. The two are complementary: this file supplies the reasoning the script cannot encode (qualitative role assessments, open condition rationale); the script supplies falsifiable numbers this file cannot.*

*Limitation — derivation order inverted:* The set was constructed from domain knowledge first; the criteria trace validates it second. This is a consistency check, not an independent derivation. A blind rerun — applying the criteria hierarchy to the full 118-element library without reference to the existing claimed set — requires the Criterion 1 quantitative floor to be explicitly defined with a numeric threshold first. *[→ `geometric_sufficiency_hypothesis.md`, H:§4, Criterion 1]*

*Criteria order: defined in `geometric_sufficiency_hypothesis.md` H:§4 (prose descriptions and axiom links) and `GSH_mathematical_inventory.md` M:§4.1 (formal expressions; all M:§ references in this file point to `GSH_mathematical_inventory.md`). Hard boundary conditions (Criterion 1, Criterion 2, Criterion 3, Criterion 4) first; Σ comparison criteria (Criterion 5–9) second. Axiom II is a co-parallel Stage 1 hard boundary condition (M:§8.2, CD-DG — Constraint-Driven Dependency Graph). The five Stage 1 conditions operate in parallel — any single failure is terminal. The filter ordering below is presentational; it does not imply sequential dependency between Stage 1 conditions.*

---

**Context fixed at Layer 0 (M:§1 deployment-fixed state):**
- $T_0$: ~250 K (deep space / orbital mean, solar-heated side)
- $\dot{Q}_{\text{solar}}$: ~50 W/m² at 3–5 AU (asteroid belt reference)
- ATM: absent (vacuum)
- Abundance reference: $\text{C}$/$\text{S}$/$\text{M}$-type asteroid composition
- $\tau$: mission lifetime — required input; Criterion 3 threshold, Axiom II kinetic gate, and all Σ comparisons are $\tau$-dependent (M:§8.2 CD-DG system inputs). Not fixed in this trace — qualitative assessments below apply across the plausible range. Fixed at $\tau = 100\,\text{yr}$ in `tools/derive_element_set.py` for the computable run.

---

## $\mathcal{F}_{\text{space}}$ — Engineering requirement set

*$\mathcal{F}_{\text{space}}$ is a co-equal input with the Layer 0 deployment context. Both must be fixed before the elimination trace begins — the criteria hierarchy consumes them from Filter 1 onward. This section states $\mathcal{F}$ as a bounded list of required functional outcomes: only those outcomes that determine whether a criterion fires are included. Each entry carries a binary (required / not required) and, where required, a target value or range.*

| # | Functional outcome | Required? | Target value or range | Criterion consequence |
|---|---|---|---|---|
| 1 | Structural (tensile, compressive load-bearing) | Yes | ≥200 MPa tensile for primary structure | Al, SiC-reinforced C geometry satisfy; no new element required |
| 2 | Thermal management (conduction, radiation rejection) | Yes | Operating range −100 to +200°C; thermal cycling survivable | Al, Si, C geometry satisfy within $\mathcal{E}^*$ |
| 3 | Electrical generation (solar PV) | Yes | Spectral response 300–1100 nm; ≥1 kW·e per tonne system-level specific power | Si PV satisfies; no new element required |
| 4 | Electrical conduction | Yes | Resistivity achievable within $\mathcal{E}^*$ over 10–100 m runs | Ag optimum (Criterion 7); Al secondary; no new element required |
| 5 | Magnetic — flux channelling (transformer cores, magnetic bearings — requires permeability) | Yes | $\mu_r \geq 1{,}000$ (soft iron range; required for power electronics transformer cores, magnetic bearings in reaction wheels) | No geometric arrangement of $\mathcal{E}^*$ members replicates ferromagnetic $d$-electron band structure. No $\Sigma$ calculation needed. Fe retained for this $\mathcal{F}$. |
| 6 | Magnetic — field generation only (motors, solenoids — sustained current loop sufficient) | Yes | $B$ = 0.05–0.5 T; torque density ~1–10 N·m/kg system-level | Air-core coil geometry (Al or Ag wire within $\mathcal{E}^*$) satisfies lower end; mass penalty vs. Fe-core unresolved — moot while row 5 requires Fe retention. |
| 7 | Computation / logic | Yes | Radiation tolerance ≥100 krad(Si) TID; −55 to +125°C operating | Si CMOS radiation-hardened satisfies; no new element required |
| 8 | Chemical energy storage (storable, recyclable) | Yes | ≥1 kWh/kg system-level specific energy; storable and recyclable within $\mathcal{E}^*$ using solar flux alone | H passes as Axiom III carrier (H₂/O₂ redox); no new element required |
| 9 | Catalysis (chemical processing loops) | Yes | Zero-consumption catalyst for H₂O electrolysis and fuel-cell operation; ~0.1–0.5 mg/cm² loading | Pt satisfies; no new element required |
| 10 | Sealing / joining | Yes | −100 to +200°C; ≤1 atm differential pressure | C/SiC ceramics and Al joints within $\mathcal{E}^*$; no new element required |

**$\mathcal{F}_{\text{space}}$ is specified for this derivation run.** Row 5 = Yes is the safest defensible default for a general-purpose $\mathcal{F}$: attitude control and power electronics require flux channelling; claiming No would require defending that no sub-system in general-purpose space engineering ever needs $\mu_r \geq 1{,}000$. An auditor who disagrees must supply a competing $\mathcal{F}$ that excludes all flux-channelling sub-systems.

**Scope note:** this list covers only outcomes that determine whether a criterion fires. It is not a full engineering specification.

---

## Filter 1 — Criterion 1: Abundance in $\text{C}$/$\text{S}$/$\text{M}$-type asteroids

Hard boundary condition. Eliminates any element not present at recoverable concentration in $\text{C}$-, $\text{S}$-, or $\text{M}$-type asteroids.

**Abundant in at least one asteroid type (pass — continue to next criterion):**

| Element | Asteroid type(s) | Notes |
| :--- | :--- | :--- |
| H | $\text{C}$-type (hydrated silicates, ice) | |
| C | $\text{C}$-type | Carbonaceous; high concentration |
| N | $\text{C}$-type | Trapped in organics |
| O | All types — silicate matrix | Dominant by mass |
| Na | All types — trace feldspar | |
| Mg | $\text{S}$/$\text{M}$-type — olivine, pyroxene | High concentration |
| Al | $\text{S}$/$\text{M}$-type — feldspar | |
| Si | All types — silicate dominant | |
| P | $\text{C}$-type — phosphates | Trace |
| S | $\text{C}$/$\text{M}$-type | |
| K | $\text{S}$-type — feldspar | Trace |
| Ca | All types — pyroxene | |
| Ti | $\text{S}$/$\text{M}$-type — ilmenite | Trace |
| Cr | $\text{M}$-type | |
| Mn | $\text{S}$/$\text{M}$-type | Trace |
| Fe | $\text{S}$/$\text{M}$-type — dominant metal phase | |
| Co | $\text{M}$-type — siderophile | |
| Ni | $\text{M}$/$\text{S}$-type — siderophile | |
| Cu | $\text{M}$-type | Trace |
| Zn | $\text{C}$-type | Trace |
| Ge | $\text{M}$-type | Trace |
| Ag | $\text{M}$-type | Trace — but sufficient for thin-film / catalytic use |
| Sn | $\text{C}$-type | Trace |
| Pt | $\text{M}$-type — siderophile PGM | Trace — but zero-consumption catalyst use |
| Au | $\text{M}$-type | Trace |
| Pb | $\text{C}$-type | Trace |
| Ir | $\text{M}$-type — siderophile PGM | Trace |

**Eliminated at Criterion 1 (not present at recoverable concentration in any common asteroid type):**

This filter eliminates the majority of the periodic table — rare earths, halogens (except trace), most transition metals, actinides, noble gases (not extractable without atmosphere), most post-transition metals.

*Note: The precise boundary depends on "recoverable concentration" — a threshold not yet defined. This is a known gap: Criterion 1 uses a qualitative filter that needs a quantitative floor (minimum extractable mass per mission mass budget). That threshold is problem-specific. For this scratchboard, the filter is: element must appear in standard asteroid mineralogy literature as a constituent phase, not merely a trace contaminant. The floor is not arbitrary — it should be tied to the $\Sigma_s$ cost of extracting from dilute matrices: an element present at 1 ppb requires exponentially more extraction exergy than one present at 1000 ppm, and the cutoff occurs where $\Sigma_s$ of extraction from the dilute source exceeds $\Sigma_s$ of any alternative supply path or geometric substitution. This is the content of Criterion 1 (quantitative floor undefined). *[→ `geometric_sufficiency_hypothesis.md`, H:§4, Criterion 1]**

**Candidate surviving set after Filter 1 (approximate — ~25–30 elements):**
H, C, N, O, Na, Mg, Al, Si, P, S, K, Ca, Ti, Cr, Mn, Fe, Co, Ni, Cu, Zn, Ge, Ag, Sn, Pt, Pb, Ir (and a few others depending on threshold)

---

## Filter 2 — Criterion 4: Refining energy (Axiom III operationalisation)

Hard boundary condition. Element must be isolable using only the available solar flux at the deployment context — ~50 W/m² at asteroid belt. High concentration optics (CPC, parabolic dish) can reach BT3 (~1700°C) from this flux given sufficient collector area, but electrochemical routes requiring grid-scale power are not available. Temperature tiers used throughout this filter: BT2 (~800–1200°C), BT3 (~1200–1700°C), BT4 (>1700°C) — solar concentrator temperature tiers defined in OQ-GSH.7. *[→ `geometric_sufficiency_hypothesis.md`; H:§7; OQ-GSH.7]*

**Eliminated at Criterion 4:**

| Element | Reason |
| :--- | :--- |
| Pb | Refineable (low melting point, 327°C) but Pb compounds toxic and no functional role not covered by other candidates — carry forward to Criterion 2 for explicit elimination |
| Fe | Carbothermic reduction of Fe₂O₃/Fe₃O₄ at ~800–1000°C — within BT2/BT3 solar thermal range. *Passes Criterion 4.* Marginal entropy note: if BT3 solar thermal is already running for Al, Si, or Mg extraction, the marginal $\Sigma_s$ of adding Fe carbothermic reduction to the same concentrator cycle may be near zero — Fe does not require a dedicated concentrator. This does not change the Criterion 4 result but is relevant to the $r_{\text{corr}}(\text{Fe})$ term inside $\Sigma_s(\text{Fe}, \tau)$ downstream — the marginal concentrator cost reduces the marginal $\Sigma_s(\text{Fe})$ for the co-production case. |
| Mg | Primary route: requires electrolysis of MgO or MgCl₂ — not achievable via solar thermal alone without Cl₂ infrastructure. Secondary route: silicothermic reduction (Pidgeon process) — MgO + Si under vacuum at ~1200°C → Mg vapor + SiO₂. Si is in $\mathcal{E}^*$; space provides natural vacuum; BT3 solar concentrators reach 1700°C, above the Pidgeon operating temperature. *Criterion 4 result: moot — Mg is eliminated at Filter 3 (Criterion 2 — single role; Pidgeon loop circularity blocks Axiom I cost comparison). Criterion 4 borderline status is not carried forward.* |
| Ti | Kroll process requires Cl₂ and Mg; carbothermic route requires >1600°C and produces TiC not pure Ti. *Borderline — carbothermic Ti reduction at BT3 is undemonstrated at engineering scale* |
| Cr | Aluminothermic or electrolytic reduction — both require pre-refined Al or grid power. Eliminated unless Al is available first. Bootstrap dependency: Cr cannot be refined before Al is available, but Al refining does not require Cr; the sequencing is one-way, not circular — Cr elimination stands once Al is confirmed in $\mathcal{E}^*$ |
| Mn | Electrolytic or aluminothermic — same as Cr; same sequencing note applies |
| Co | Smelting requires sulfuric acid roasting or pressure oxidation — neither within solar thermal alone |
| Ge | Requires HCl chemistry for purification — outside $\mathcal{E}^*$ |
| Sn | Low melting point (232°C); solar thermal refineable from cassiterite (SnO₂) via carbothermic reduction at ~1000°C. *Passes Criterion 4* |
| Ir | PGM — requires aqua regia or other aggressive chemistry. *Eliminated* |
| Au | Same as Ir |
| Cu | Smelting operable at BT2 (~800–1000°C) from sulfide ores; solar thermal achievable. *Passes Criterion 4* |
| Zn | Carbothermic reduction of ZnO at ~1000°C — passes Criterion 4 |

**Candidate surviving set after Filter 2 (~18–20 elements):**
H, C, N, O, Na, Mg*, Al, Si, P, S, K, Ca, Ti*, Fe, Ni, Cu, Zn, Ag, Sn, Pt

Ti is borderline — carbothermic Ti reduction at BT3 is undemonstrated at engineering scale; Ti retention is an open dependency pending BT3/BT4 confirmation. Mg is eliminated at Filter 3 — see Filter 3 Mg row. *[→ `geometric_sufficiency_hypothesis.md` H:§7 OQ-GSH.7; BT tier definitions: `derived_analysis/solar_thermal_loop_analysis.md`]*

---

## Filter 3 — Criterion 3: Recyclability (mass recovery rate ≥ 99.9% per cycle using gradient-derived energy)

Hard boundary condition. Product of use must be recoverable within $\mathcal{E}^*$ using gradient-derived energy at deployment context temperature. Includes the kinetic operability gate from OQ-GSH.7: thermodynamic feasibility is necessary but not sufficient. *[→ `geometric_sufficiency_hypothesis.md`; H:§7; OQ-GSH.7]*

**Eliminated at Criterion 3:**

| Element | Oxidation product | Recovery feasibility | Result |
| :--- | :--- | :--- | :--- |
| S | SO₂/SO₃ | Reduction requires temperatures >1000°C and reducing atmosphere — marginal within $\mathcal{E}^*$ | *Borderline — carry to Σ comparison criteria, flagged* |
| Pb | PbO/PbSO₄ | Reduction at ~880°C (carbothermic) passes thermodynamic test; however Pb has no functional role in $\mathcal{E}^*$ not covered by other candidates (no structural, conductive, or catalytic role that Ag, Pt, Al, or C cannot fill). *Eliminated at Criterion 3 via Criterion 2 pre-check: zero distinct functional roles in deployment context.* |
| P | P₂O₅ | Reduction thermodynamically demanding; no clear catalyst in $\mathcal{E}^*$ | *Borderline* |
| Zn | ZnO | Carbothermic reduction at ~1000°C — passes | Pass |
| Cu | CuO/Cu₂O | Reduction at ~800°C — passes | Pass |
| Sn | SnO₂ | Carbothermic at BT2 — passes | Pass |
| Ni | NiO | Reducible with C at ~600°C — passes | Pass |
| Fe | Fe₂O₃/Fe₃O₄ | Carbothermic reduction feasible; Axiom II deferred debt accrues from t=0. Corrosion contribution to $\Sigma_s(\text{Fe}, \tau)$ is deployment-fixed via $r_{\text{corr}}(\text{Fe})$ from ISO 9223 data for the specific environment; in this deployment context (ATM: absent), $r_{\text{corr}} \approx 0$ — corrosion contribution is negligible. No classification gate required. *[→ Application Examples below]* | Pass |
| Ca | CaO | Reduction requires >2000°C — above BT4 ceiling of solar concentrators without W infrastructure | *Eliminated unless W is available (circular)* |
| Mg | MgO | Silicothermic route (Pidgeon process): SiO₂ + 2Mg → Si + 2MgO; recycling step to recover Mg requires 2MgO + Si → 2Mg + SiO₂. The two steps cancel: the Si consumed in the recycling step is the same Si produced in the reduction step. Net output is zero — no surplus Si, no recyclable Mg outside the loop. Criterion 2 (single role); Pidgeon loop circularity blocks Axiom I cost comparison: Mg has no non-circular refining route within $\mathcal{E}^*$. *Eliminated.* | Eliminated — Pidgeon circularity |

**Candidate surviving set after Filter 3 (~13 elements):**
H, C, N, O, Na, Al, Si, K, Fe*, Ti*, Ni, Cu, Zn, Ag, Sn, Pt

*Fe: passes Criterion 3 — Axiom II recycling loop is thermodynamically feasible; corrosion debt accrues from t=0 per $r_{\text{corr}}(\text{Fe})$ (ISO 9223 deployment-fixed value; $r_{\text{corr}} \approx 0$ in vacuum for this context). Ti: still borderline on Criterion 4. Pb: eliminated (zero distinct functional role). S: borderline recyclability — carries to Σ comparison criteria, flagged. Mg: eliminated — Pidgeon loop circularity; Criterion 2 (single role); circularity blocks Axiom I cost comparison — not a kinetic open question.*

---

## Filter 4 — Criterion 2: Functional role breadth (hard boundary condition)

Hard boundary condition (M:§4.1). Elements that perform only one functional role fail Criterion 2 unconditionally — $|\{f : x \text{ satisfies } f\}| = 1$. Elements covering multiple functional roles pass and continue to Filter 6. This is logically parallel to Criterion 1, Criterion 3, Criterion 4 and Axiom II in Stage 1 of the CD-DG (M:§8.2); it is run as Filter 4 here for presentation clarity — that ordering does not create a dependency on the outcome of Filters 1–3. *Note on label: M:§4.1 names this criterion "Allotropic Versatility" — Carbon's allotropic versatility (graphene, diamond, CNT, fullerene) is the canonical example of a single element covering multiple functional roles via geometric arrangement.*

**Assessed:**

| Element | Functional roles | Covered by | Result |
| :--- | :--- | :--- | :--- |
| Ni | Corrosion-resistant coating, catalyst | Pt covers catalysis (zero-consumption); C/Al cover structure; no irreplaceable role confirmed | *Eliminated at Filter 4 — hard boundary condition applies* |
| Cu | Electrical conductivity | Ag is Criterion 7 optimum | Single role — but Criterion 7 Σ comparison is the operative test; carry to Filter 6 |
| Zn | Sacrificial anode (anti-corrosion) | Single functional role: galvanic protection of Fe. Fe is in the set for this $\mathcal{F}$, so the role is active. Criterion 2 applies: $|\{f : \text{Zn satisfies } f\}| = 1$ — no other role confirmed. *Eliminated at Filter 4.* |
| Sn | Low-temperature joining (solder); bearing surface | One primary structural role; bearing function coverable by C geometry | *Marginal — single specialist role; carry to Filter 6* |
| Ti | Structure (high-strength, low-mass) | Al-SiC composite geometry could substitute at cost of $\Sigma_g$ | *Multi-role (structure + thermal tolerance) — passes Filter 4; Σ comparison deferred to Filter 6* |
| S | Vulcanisation; chemical precursor | No confirmed functional role not covered by $\mathcal{E}^*$ members in space context | *Eliminated at Filter 4* |

---

## Filter 5 — Axiom II: All states recoverable using gradient-derived energy

Hard boundary condition (with kinetic gate). Axiom II is a Stage 1 co-parallel condition in the CD-DG (M:§8.2) — logically parallel to Criterion 1, Criterion 2, Criterion 3, Criterion 4. It is presented as Filter 5 here for readability (elements that fail Criterion 1, Criterion 3, or Criterion 4 at Filters 1–3 are not re-evaluated here), but the filter ordering does not create a dependency on prior filter outcomes. Any element whose reaction products under operating conditions cannot be recovered within $\mathcal{E}^*$ using gradient-derived energy fails this condition unconditionally. The kinetic operability gate from OQ-GSH.7 applies: thermodynamic feasibility is necessary but not sufficient. *[→ `geometric_sufficiency_hypothesis.md`; H:§7; OQ-GSH.7]*

**Critical cases:**

| Element | Operating product | Recovery | Result |
| :--- | :--- | :--- | :--- |
| N | N₂ (inert atmosphere consumption) | Atmospheric loss in vacuum — once lost, recovery requires energy-intensive fixation not achievable within $\mathcal{E}^*$ alone | *Conditional: N is viable only if losses are contained. Open-space use eliminates N unless containment is demonstrated* |
| Ag | AgO (oxidation in high-flux environment) | Ag₂O reduction at ~300°C — easily achievable. Passes. | Pass |
| Pt | PtO₂ (very slow oxidation) | Reduction at ~500°C. Near-zero consumption in catalytic role. Passes. | Pass |
| Sn | SnO₂ | Carbothermic reduction — passes | Pass |

---

## Filter 6 — Criterion 5–9: Σ comparison and hard functional gap

Elements surviving hard boundary conditions are subject to the Σ comparison: retained only if no other $\mathcal{E}^*$ member can geometrically substitute at lower Σ.

| Element | Criterion | Assessment |
| :--- | :--- | :--- |
| Cu | Criterion 7 (Signal/Conductivity) | Ag has higher electrical and optical conductivity; Cu retained only while $\Sigma_g(\mathcal{G}_{\text{Cu→Ag}}, \tau) > \Sigma_s(\text{Cu}, \tau)$ — i.e., while Ag deposition infrastructure is immature. In a mature $\mathcal{E}^*$ context, Cu is on a directed removal trajectory. Excluded from space $\mathcal{E}^*$ where Ag deposition is demonstrable. |
| Sn | Criterion 2 | Single specialist joining role. SiC ceramics and carbon-fibre composites cover structural joining without Sn in the space context. Removed. |
| Ti | Criterion 5 | Al-SiC geometry at cost of increased $\Sigma_g$. The Σ comparison is structurally incomplete — two required inputs are missing: (i) $\tau_{\text{wearout}}$ for Al/SiC under $\mathcal{F}_{\text{space}}$ thermal cycling (−100 to +200°C); if $\tau > \tau_{\text{wearout}}$, the operative $\Sigma_g$ is $\lceil \tau / \tau_{\text{wearout}} \rceil \cdot \Sigma_{g,\text{mfg}}$, not $\Sigma_{g,\text{mfg}}$ alone — CTE mismatch under continuous thermal cycling makes this multiplier likely greater than 1, strengthening Ti retention; (ii) $T_0^{\text{fab}}$ mismatch — Al/SiC manufacturing entropy is computed at 298 K (Earth fabrication) but the operative inequality runs at $T_0 = 250\,\text{K}$ (deployment dead-state) — unadjusted per OQ-GSH.19. Comparison computationally blocked by OQ-GSH.17; OQ-GSH.18. *Retained pending OQ-GSH.21 and $\tau_{\text{wearout}}$ data — the pipeline requires positive evidence of substitution viability before removal.* |
| Fe | Flux-channelling sub-requirement ( $\mu_r \geq 1{,}000$, row 5 = Yes) | No geometric arrangement of $\mathcal{E}^*$ members replicates ferromagnetic $d$-electron band structure. No $\Sigma$ calculation needed. Fe retained for this $\mathcal{F}$. Marginal entropy note: if BT3 solar thermal already running for Al/Si, Fe carbothermic refining carries near-zero marginal $\Sigma_s$ — co-production reduces the effective $\Sigma_s(\text{Fe})$. |
| Na, K | Criterion 7 / Criterion 8 | Heat transfer optimum as liquid metal; alkali-ion storage. Na and K occupy the same functional category; Axiom I requires that neither alone satisfies all alkali-dependent requirements before both are retained — not yet demonstrated *[→ OQ-GSH.4]*. Retained pending Na-alone or K-alone substitution proof. |

---

## $\mathcal{E}^*(\mathcal{F}_{\text{space}})$ — Element set for space engineering context

After applying all nine criteria to the ~118 elements filtered through the space deployment context:

**Unambiguous survivors:** C, H, O, Si, Al, Ag, Pt

**Conditionally retained (require further verification):**
- N — only if containment is demonstrated (Axiom II kinetic gate)
- Na, K — both retained pending demonstration that neither Na alone nor K alone satisfies all alkali-dependent requirements (OQ-GSH.4)
- Ti — Σ comparison structurally incomplete: $\tau_{\text{wearout}}$ for Al/SiC under $\mathcal{F}_{\text{space}}$ thermal cycling not established (step multiplier $\lceil \tau / \tau_{\text{wearout}} \rceil$ likely $> 1$, favouring retention); $T_0^{\text{fab}}$ mismatch unadjusted (OQ-GSH.19); computationally blocked (OQ-GSH.17; OQ-GSH.18); retained pending OQ-GSH.21
- Fe — flux-channelling sub-requirement ( $\mu_r \geq 1{,}000$, row 5 = Yes); no geometric substitute demonstrated within $\mathcal{E}^*$

**Prior claimed set:** {C, H, O, N, Si, Al, Na, K, Ag, Pt} — 10 elements. **Requires update: Fe retained for this $\mathcal{F}$, giving 11 elements.**

**Trace verdict:** The 7 unambiguous survivors match the source set core. The conditional N and Na/K match the source set's conditional language. Ti is conditionally retained — the Σ comparison is unresolved; the pipeline retains when indeterminate. Fe is retained for this $\mathcal{F}$ — no geometric substitute demonstrated for the flux-channelling sub-requirement; the source set's provisional exclusion does not hold for a $\mathcal{F}$ with row 5 = Yes. Mg eliminated by Pidgeon loop circularity (Criterion 2 — single role; circularity blocks Axiom I cost comparison).

**The trace exposes three gaps:**

1. Criterion 1 quantitative floor — "recoverable concentration" has no formal threshold. An auditor cannot replicate Filter 1 without a defined minimum tied to extraction $\Sigma_s$ cost. *[→ `geometric_sufficiency_hypothesis.md`, H:§4, Criterion 1]*

2. Ti retention vs. source set exclusion — Ti passes all hard boundary conditions. The Σ comparison against Al/SiC is structurally incomplete: $\tau_{\text{wearout}}$ for Al/SiC under continuous thermal cycling (−100 to +200°C) is not established, and the step multiplier $\lceil \tau / \tau_{\text{wearout}} \rceil$ is likely greater than 1 given CTE mismatch — making the substitute more expensive than a single-manufacture assumption implies. The $T_0^{\text{fab}}$ context mismatch (298 K fab vs. 250 K deployment) is also unadjusted (OQ-GSH.19). Ti is conditionally retained pending OQ-GSH.21 and $\tau_{\text{wearout}}$ data. *[→ `geometric_sufficiency_hypothesis.md`, H:§7, OQ-GSH.19; OQ-GSH.21]*

3. Mg elimination path — traced in Filter 3 (Pidgeon loop circularity, Criterion 2 — single role; circularity blocks Axiom I cost comparison).

**Plausible set under current gap conditions:**

The three pipeline gaps (OQ-GSH.17, OQ-GSH.18, OQ-GSH.23 — $\Sigma_g$ computation incompleteness) affect only the Σ comparison stage (Filter 6). The hard boundary filters (Filters 1–5) are computable from standard data and are unaffected. The plausible set is therefore:

| Status | Elements | Basis |
|---|---|---|
| Unambiguous | C, H, O, Si, Al, Ag, Pt | Hard boundary conditions pass; no open Σ comparison |
| Conditional — flux-channelling substitute undemonstrated | Fe | No geometric substitute for $\mu_r \geq 1{,}000$ within $\mathcal{E}^*$ demonstrated; retained for this $\mathcal{F}$ (row 5 = Yes) |
| Conditional — kinetic gate open | N | Axiom II containment undemonstrated (OQ-GSH.15) |
| Conditional — Σ comparison structurally incomplete | Ti | Two missing inputs: $\tau_{\text{wearout}}$ for Al/SiC under thermal cycling (step multiplier likely $>1$, favouring Ti retention); $T_0^{\text{fab}}$ mismatch unadjusted. Computationally blocked by OQ-GSH.17; OQ-GSH.18. Retained pending OQ-GSH.21 and $\tau_{\text{wearout}}$ data |
| Conditional — substitution undemonstrated | Na, K | Neither Na-alone nor K-alone substitution demonstrated (OQ-GSH.4) |

This is the complete set for $\mathcal{F}_{\text{space}}$ as specified. *[→ OQ-GSH.2 for the question of whether Fe can be excluded from any $\mathcal{F}$; OQ-GSH.21 for Ti; OQ-GSH.4 for Na/K]*

---

## Context variation — $|\mathcal{E}^*|$ by deployment context

The space engineering derivation above is one context. $|\mathcal{E}^*|$ varies with deployment conditions; the criteria hierarchy produces a different survivor set for each.

| Context | Adjustment | Estimated $\lvert\mathcal{E}^*\rvert$ |
| :--- | :--- | :--- |
| Space / 3–5 AU (this derivation) | Baseline above | 7 unambiguous + 4 conditional ( $\mathrm{Fe, N, Ti, Na/K)}$ |
| Earth / terrestrial | Criterion 1 shifts to geological abundance ( $\mathrm{Si, Al, C, Na, K}$ abundant; $\mathrm{Ag}$ and $\mathrm{Pt}$ trace); physics gaps are secondary — primary challenge is the OQ-GSH.7 solar-thermal bootstrap loop | 8–10 ( $\mathrm{Ag}$/$\mathrm{Pt}$ substitution if trace mass is prohibitive) |
| Deep space / cryogenic | $\mathrm{K}$ enables $\mathrm{C}$ superconductivity; $\mathrm{N}$ may be dropped if $\mathrm{Si}_3\mathrm{N}_4$ is redundant with $\mathrm{SiC}$. Scope limit: the hypothesis requires a minimum ambient gradient floor — interstellar transit with no accessible gradient source is outside the hypothesis's operating domain. For near-gradient transit contexts, the Gradient Locality principle applies *[→ `geometric_sufficiency_hypothesis.md` H:§2 Axiom III Gradient Locality]*. | 7–9 |
| Stellar proximity / high-flux | $\mathrm{SiC}$ refractory ceiling exceeded; $\mathrm{W}$ candidate addition required | 11 |
| Single-resource environment | Set contracts to locally available elements; geometric demand increases | *OQ-GSH.1* |
| Lunar ( $\mathrm{H}$/$\mathrm{C}$-absent) | BT1–BT4 bootstrap architecture does not apply; MRE-anchored substitute. Revised set $\mathcal{E}^*_{\mathrm{lunar}} = \{\mathrm{O, Si, Al, Fe, Na, K, Ti}\}$ — see OQ-GSH.30 | 7 |

---

## Application examples

*These examples illustrate how the criteria hierarchy produces specific, computable outputs — not how a maximiser would apply the framework.*

### Fe inclusion — context-dependent, not universal

$\mathrm{Fe}$ inclusion or exclusion is not derivable without a specified $\mathcal{F}$. The general inequality requires defined substitute geometry, $\tau$, and deployment-specific $r_{\mathrm{corr}}(\mathrm{Fe})$. In all operating contexts, $r_{\mathrm{corr}}(\mathrm{Fe})$ is a deployment-fixed input (ISO 9223 data) that modifies $\Sigma_s(\mathrm{Fe}, \tau)$ for the specific environment. Environments with low $r_{\mathrm{corr}}$ (vacuum, dry inert atmosphere) have negligible corrosion contribution to $\Sigma_s$; corrosive environments have higher $r_{\mathrm{corr}}$ and correspondingly higher $\Sigma_s(\mathrm{Fe}, \tau)$. Universal $\mathrm{Fe}$ exclusion violates Requirement 4 — the correct result is problem-specific.

For the space context specifically: Fe is in the set for this $\mathcal{F}$ (row 5 = Yes) — the flux-channelling sub-requirement ( $\mu_r \geq 1{,}000$) has no demonstrated geometric substitute within $\mathcal{E}^*$. In vacuum, $r_{\mathrm{corr}} \approx 0$, so corrosion is not an issue.

*Earth context application examples (Cu removal trajectory; fossil fuel substitution) — see `derived_analysis/solar_thermal_loop_analysis.md` Section 8.*
