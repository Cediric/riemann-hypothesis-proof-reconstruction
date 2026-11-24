# Riemann Hypothesis Lean Proof Reconstruction

A source-audited, human-readable reconstruction of the public Lean development associated with the claimed proof of the Riemann hypothesis.

**Important scope statement:** this repository does not claim to present a complete independent human-readable proof of RH. It distinguishes (1) kernel-checked formal proof, (2) an explanatory reconstruction of the mathematics, and (3) independent mathematical review. Any unexpanded input or unverified bridge is labelled as such.

## Published material

| Document | Contents |
|---|---|
| [V2.7 — Full reconstruction and audit draft](docs/RH_Lean_Natural_Language_Reconstruction_V2.7.md) | Working manuscript through Theta orbit mass, denominator, weighted-kernel, and Rallis boundary audits. This is a searchable-text Markdown export; some layout-dependent equation objects may need cross-checking against the fixed Lean sources. |
| [V2.7 exact arithmetic certificate](checks/theta_mass_and_adjoint_exact_certificate_v27.py) | Finite exact-arithmetic diagnostics for orbit mass, lcm denominators, weighted adjoints/composition, a Hilbert–Schmidt inequality, and an adjoint-invariance counterexample. |
| [V2.8 — Rallis, Schur averaging, and Theta-lift nonvanishing](docs/V2.8_Rallis_Schur_ThetaLift_Nonvanishing.md) | Source-level reconstruction of the exact `Rallis_k`, `SchurStep_k`, `AbsNe`, and `NonVan_k` chain. |
| [V2.9 — Tools_k construction audit](docs/V2.9_Tools_Package_Construction_Audit.md) | Tracks the 14 fields of `Tools_k` to their concrete Lean constructions. |
| [V3.0 — TLiftK to RH top-level chain](docs/V3.0_TLiftK_to_RH_TopLevel_Chain.md) | Traces the route from theta-lift existence through Galois representations and EveryCharacter to RH. |
| [V3.0 supplement — Siegel–Weil and Poisson/CT splitting](docs/V3.0_SiegelWeil_to_Riemann_Hypothesis_Audit.md) | Expands the standard Siegel–Weil formula, Poisson summation, constant-term splitting, and the meaning of `MainC_k 2`. |
| [V3.1 — Sha windows, Chebyshev bounds, and zero-free regions](docs/V3.1_Sha_Windows_Chebyshev_and_ZeroFree.md) | Expands the `VWin` quantity and its route to zero-free bounds. |
| [V3.2 — Counts and Galois cohomology lengths](docs/V3.2_Counts_and_Galois_Cohomology_Lengths.md) | Separates global Sha, H², and local length quantities and traces the CountI/II/III/IV/V/Vs/Z branches. |
| [V3.3 — Kato Euler systems, LemmaK, and window constants](docs/V3.3_Kato_Euler_Systems_LemmaK_and_Window_Constants.md) | Expands the Kato/Euler-system route, finite H² bounds, SP4 image density, and window constants. |
| [V3.4 — K4/K5 inputs, Hecke projection, and ZetaUr](docs/V3.4_K4_K5_Inputs_Hecke_Projection_and_ZetaUr.md) | Audits `Nf`, `SrcUr`, `AdmWn`, the construction of `AdmTop2`, K4/K5, and the acyclic route through `ZetaUr` to `VWin`. |
| [V3.5 — Foundational Glue2 inputs](docs/V3.5_Glue2_Foundational_Inputs_Eisenstein_Towers_and_Measure.md) | Expands the ordinary Eisenstein eigenfunctional, modular-function tower, bounded-distribution power series, valuation embedding, coefficient-ring enlargement, and monotonicity inputs. |
| [V3.5 supplement — Ordinary Eisenstein eigenfunctional proof](docs/V3.5_Ordinary_Eisenstein_Eigenfunctional_Construction.md) | Deepens the ordinary Eisenstein eigenfunctional audit: depletion, unit-root splitting, Petersson/Sturm construction, Rankin nonvanishing, Atkin–Lehner extension, MeasMu, and the right-edge twisted-L nonvanishing argument. |
| [V3.6 — Representation and local inputs](docs/V3.6_Glue2_Representation_Local_Inputs_and_Pin7.md) | Expands `PsiEx`, `FrobU`, `DetIne`, `HatW`, `SmNz`, `GmEx`, `ExplSmul`, and the assembly of `Pin7`. |
| [V3.7 — Average identities and final Glue2 assembly](docs/V3.7_AvgEq_AvgMF_RhsEq_Smoothing_and_Glue2.md) | Expands `AvgEq`, `AvgMF`, `RhsEq`, `SmSys`, and `ChiFix`, then traces the 235-line `glue2` proof into `ExistsZetaEulerSystemIwasawaData Pin7`. |
| [V3.8 — Pin7 local nonvanishing and ZetaUr](docs/V3.8_Pin7_Local_Nonvanishing_and_ZetaUr.md) | Audits `C7.pLocu`: the contradiction from `¬NzAt` to `SpZero`, `pCore`, p-adic power-series nonvanishing transfer, `NzAt`, and finally `ZetaUr`. |
| [V3.9 — ZetaUr to ordinary Selmer vanishing](docs/V3.9_ZetaUr_to_Ordinary_Selmer_Vanishing.md) | Reconstructs `ZetaUr → VanishOrdL`: ordinary normal form, Euler-system strict vanishing, Greenberg upgrade, dual Selmer growth contradiction, Bloch–Kato local-to-ordinary conversion, and RepIso transport. |
| [V3.10 — LitCoh provenance and LiteratureRankN](docs/V3.10_LitCoh_Provenance_and_LiteratureRankN.md) | Traces all 12 `LitCoh` fields to their theorem constructors, follows `OpenImageCondition` and `RowT` back to `TLiftK`, and audits the assembly into `LiteratureRankNHypothesis` and `HypothesesH'`. |
| [V3.11 — Local Tate duality and Bloch–Kato local](docs/V3.11_Local_Tate_Duality_and_BlochKatoLocal.md) | Expands `SgcRep/Sgc0/Sgc1/Sgc2`, local field and roots-of-unity inputs, constructs `LocalTateDualityK` and `LocalEulerCharK`, and follows `formsL → bkAL → bkBL → BlochKatoLocal`. |
| [V3.12 — Local invariant, Kummer pairing and BK dimension](docs/V3.12_Local_Invariant_Kummer_and_BK_Dimension.md) | Constructs the Brauer invariant from finite unramified levels and Frobenius evaluation, derives the Kummer perfect pairing, and expands `bkADim` through `aMap`, `bMap`, and `relR`. |
| [V3.13 — Fontaine fundamental sequence and crystalline lifting](docs/V3.13_Fontaine_Fundamental_Sequence_and_Crystalline_Lifting.md) | Traces `FontaineBcris` through `LocTied`, proves the tensor fundamental sequence, constructs connecting Bloch–Kato cocycles, and lifts crystalline coboundaries using filtered invariants. |
| [V3.14 — FontaineBcris foundations and filtered invariants](docs/V3.14_FontaineBcris_Foundations_and_Filtered_Invariants.md) | Derives `TensorInj` from unramified linear independence, constructs `FontaineBcris` via `FundOnto` and `1−φ`, and proves graded inverse/invariant lemmas and `DeRhamSpan`. |
| [V3.15 — Core, PeriodData and Galois invariants](docs/V3.15_Core_PeriodData_and_Galois_Invariants.md) | Traces `Core → PeriodData → LocPrime → LocTheory`, constructs `invB` and `invdR`, and proves the BdR and Bcris Galois-invariant identifications. |
| [V3.16 — Ax–Sen–Tate and cyclotomic norm estimates](docs/V3.16_AxSenTate_and_Cyclotomic_Norm_Estimates.md) | Proves the bounded-orbit Ax lemma, fixed-closure approximation, Tate-twist invariant vanishing, cyclotomic norm/trace bounds, and inertia character finiteness. |
| [V3.17 — Inertia partial trace and geometric contraction](docs/V3.17_Inertia_Partial_Trace_and_Geometric_Contraction.md) | Derives the finite-index norm estimate, inertia congruence chain, geometric-sum contraction, and the partial-trace bound `ρⁿ` feeding Tate-character finiteness. |
| [V3.18 — Prime-power norm and congruence chain closure](docs/V3.18_Prime_Power_Norm_and_Congruence_Chain_Closure.md) | Proves the exact norm of `u^(ℓ^n)−1`, PadicInt exact-level adjustment, finite-index kernel chain, and the coset recursion required for partial traces. |
| [V3.19 — Tate inertia finiteness and Bcris Regular](docs/V3.19_TateCharacterFinite_and_BcrisRegular_Complete.md) | Consolidates the full `TateCharacterFiniteOnInertia` proof and its use in `BcrisRegular`, including the unramified Ainf period and the theta-zero branch. |
| [V3.20 — FontaineBcris seven-field dependency audit](docs/V3.20_FontaineBcris_SevenField_Dependency_Audit.md) | Audits the seven fields, reduces the final construction to four core inputs, traces Core/Fits, and expands TensorInj, Fund, FundOnto, 1−φ surjectivity, and Regular. |
| [V3.20 supplement — EveryCharacter to RH zero-free bridge](docs/V3.20_Supplement_EveryCharacter_ZeroFree_Bridge.md) | Reconstructs the final chain from TLiftK and VWin through Green, definite-side hypotheses, Chebyshev windows, zero-freeness, and the RH wrappers. |
| [V3.22 — Exact VWin statement and theorem-input audit](docs/V3.22_Exact_VWin_And_Input_Package_Audit.md) | Gives the exact VWin/VVle/WinPair quantifiers, the four-field LiteratureRankNHypothesis construction, and the TLiftK-to-Row0b input route. |
| [V3.23 — Repository synchronization and verification status](docs/V3.23_Repository_Synchronization_and_Verification_Status.md) | Reconciles the V3.20–V3.22 audit record with the current pinned Lean build, axiom-audit, and fresh-kernel CI state; status-only, not a new proof result. |
| [V3.20 supplement — TLiftK theta-lift construction](docs/V3.20_Supplement_TLiftK_ThetaLift_Construction.md) | Expands TLiftK into its 14-field Tools_k package and traces the nonvanishing/theta-lift/projection proof skeleton feeding the Galois row. |
| [V3.20 supplement — VWin descent input](docs/V3.20_Supplement_VWin_Descent_Input.md) | Traces the exact SR.descWeak theorem used by VWin, the RunTh trace-formula dichotomy, and split-rigidity elimination of the obstruction branch. |
| [V3.20 axiom-check script](checks/Check_FontaineBcris_Axioms.lean) | Prepared `#print axioms` checks for the assembled FontaineBcris theorem and its main inputs; intended to run in the pinned upstream Lean project. |
| [V3.21 main-theorem axiom-check script](checks/Check_Main_Axioms.lean) | Prepared `#print axioms` checks for the five public RH/GRH conclusions and the `EveryCharacter` bridge. |
| [V3.21 — Lean execution report](docs/V3.21_Lean_Execution_Report.md) | Records the pinned CI environment, the first full-build result, the import-graph diagnosis, and the targeted theorem-module build strategy. |

## Source snapshot

The upstream Lean source references in the current reconstruction are pinned to:

- Repository: [CocoSgt/riemann-hypothesis-lean](https://github.com/CocoSgt/riemann-hypothesis-lean)
- Commit: [`7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`](https://github.com/CocoSgt/riemann-hypothesis-lean/commit/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4)

Do not silently replace these source links with `main`: the fixed snapshot is part of the audit trail.

## Verification

The V2.7 Python certificate was executed successfully with Python. The upstream README reports a static scan with no `sorry`, `admit`, or custom axiom declarations, but this is not a substitute for a build or theorem-level axiom audit. V3.20/V3.21 add separate diagnostic scripts for the FontaineBcris dependency chain and the RH/GRH theorem wrappers. The first full `lake build Main` attempt passed `Statements` and reached 15,219/15,228 build units, but the job ended without a retrievable terminal Lean error; it is not counted as a successful build. The revised workflow now builds `Supplements.Kernels.MainTheorems` directly, caches compiled Lake artifacts, and runs both `#print axioms` scripts. The targeted run is [45320185287](https://github.com/Cediric/riemann-hypothesis-proof-reconstruction/actions/runs/45320185287). Two fresh-replay jobs were triggered by the cancellation of earlier audit runs before the replay workflow was narrowed; those jobs still target full `Main`. The replay workflow has since been updated to target `Supplements.Kernels.MainTheorems` for future runs. No successful theorem-module build, clean axiom audit, or `leanchecker` result is claimed yet. See the [V3.21 execution report](docs/V3.21_Lean_Execution_Report.md) and the [V3.0 reproducibility boundary](docs/V3.0_TLiftK_to_RH_TopLevel_Chain.md#6-公开仓库的可复核性边界).

The finite arithmetic certificate checks only its stated finite examples. These are diagnostic checks, **not** a proof of the general automorphic or arithmetic Theta/Rallis hypotheses. No new Lean compilation is claimed in this repository.

## Current research direction

The latest completed mathematical source-level audits remain V3.20 and V3.22: FontaineBcris, the TLiftK/SiegelCore construction, the exact Mathlib RH proposition, the EveryCharacter-to-RH zero-free bridge, and the exact VWin quantifiers with non-vacuity checks for primitive characters, prime pairs, host fields, and Galois-cohomology data. V3.23 is a repository synchronization and verification-status record, not a new mathematical proof result. The pinned execution baseline is Lean 4.33.1 with Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`; the upstream Lake package is `tree` with `srcDir = "src"`. V3.21 has separate axiom-audit scripts for FontaineBcris and the RH theorem wrappers. The full `Main` build was too broad for the first CI attempt: it reached 15,219/15,228 units but ended without a retrievable Lean error. The primary workflow now targets `Supplements.Kernels.MainTheorems`, which contains the theorem wrappers needed for the RH/GRH claims without the additional small-class-number imports. It also caches compiled artifacts. The fresh-kernel workflow has been narrowed to the same module for future runs; two earlier replay jobs had already started on the full `Main` target. All theorem-level axiom and fresh-kernel checks remain pending.

## License

No license has been specified. Unless and until a license is added, standard copyright restrictions apply.
