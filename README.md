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
| [V3.24 — Split rigidity and obstruction elimination](docs/V3.24_Split_Rigidity_And_Obstruction_Elimination.md) | Expands the Rankin–Selberg pole estimates, twist averaging, Cauchy–Schwarz contradiction, anti-twist construction, and normalization argument that eliminate the finite obstruction branch in VWin descent. |
| [V3.25 — Split rigidity: compressed proof](docs/V3.25_Split_Rigidity_Compressed_Proof.md) | Compresses the split-rigidity argument into five moves, isolates its three mathematical engines, and updates the independent-verification boundary; identifies the arithmetic main inequality (M) as the next exposition bottleneck. |
| [V3.26 — Arithmetic main inequality (M): interface map](docs/V3.26_Arithmetic_Main_Inequality_Interface_Map.md) | Distinguishes the two namespaced SizeData₂ declarations, expands the ChainCore interface, isolates the central LinkDIV trace-to-main-term inequality, and maps the family-to-RH proof route. |
| [V3.27 — H9: two slope bounds](docs/V3.27_H9_Two_Slope_Bounds_Compressed.md) | Decomposes the human exposition's slope-range hypothesis into first-lattice and corrected-lattice bounds, records the Lean proof conversions, and isolates Places_at as the remaining local construction bottleneck. |
| [V3.28 — Places_at construction](docs/V3.28_Places_at_Construction_Compressed.md) | Reconstructs the explicit local witnesses, the five-step places_at_of proof, and the uniform family construction placesF_min'; identifies the exact upstream inputs needed to close H9. |
| [V3.29 — H9 upstream dependency compression](docs/V3.29_H9_Upstream_Dependency_Compression.md) | Removes derived H9 premises: LvlF supplies LevelTFamily and NuCommensF, LvlF plus proviso supplies MuRank, and size/rank data supply LinkMu; isolates LinkG as the next upstream branch. |
| [V3.30 — LinkG family construction](docs/V3.30_LinkG_Family_Construction_Compressed.md) | Expands LinkG_at into five clauses and compresses linkG_fam_noKer/linkG_without_kernels into the trace, orbit, lattice-sandwich, and no-kernel proof stages. |
| [V3.31 — LinkG no-kernel proof](docs/V3.31_LinkG_NoKernel_Proof_Compressed.md) | Identifies the two theorem-family inputs, derives Adm6/7/8/9 and the orbit-lattice bounds, and compresses the zero-kernel admissibility step and final LinkG conversion. |
| [V3.32 — H5 covolume bottleneck](docs/V3.32_H5_Covolume_Bottleneck_Map.md) | Identifies CovolumeBoundThirdPlaceSeries as the H5 carrier, traces it through CovolumeBoundOfX, and maps the fifteen geometric/Arakelov inputs and the eight-step alternative route. |
| [V3.33 — H5 covolume proof compression](docs/V3.33_H5_Covolume_Proof_Compressed.md) | Compresses topCovolG_alt_alt into four blocks: Gram/size/measure, good reduction and cover degree, height lower bounds, and the eight-input lift/covolume assembly. |
| [V3.34 — H5 analytic covolume core](docs/V3.34_H5_Analytic_Covolume_Core.md) | Isolates lcv_le, the exponential-versus-polynomial absorption, and the uniform-threshold argument that converts eight pointwise lift estimates into CovolumeBoundOfX. |
| [V3.35 — H12 window supply and final RH bridge](docs/V3.35_H12_Window_Supply_and_Final_RH_Bridge.md) | Traces Scales.windows through HostWW, ObjCP, KitCPW, DesignChoices, ExWin and ChainWin to the final zero-free region; records the window-exponent compatibility check. |
| [V3.36 — H12 VWin and recursion dependencies](docs/V3.36_H12_VWin_and_Recursion_Dependencies.md) | Reduces HostExW to VWinAt and ObjCP to RecAtG/EvP/SiegelMassRatioCM; exposes the upstream dependencies of the H12 supply branch. |
| [V3.37 — Final theorem and theta-lift core](docs/V3.37_Final_Theorem_and_Theta_Lift_Core.md) | Corrects the intermediate/final theorem distinction and traces the no-argument RH theorem through Row0b, GeoOne, and the universal theta-lift theorem TLiftK. |
| [V3.38 — TLiftK tool compression](docs/V3.38_TLiftK_Tools_Compressed.md) | Reduces the universal theta-lift theorem to Tools_k and HgtEx_k, lists the fourteen tool fields, and groups their construction into Siegel–Weil/Eisenstein, compactness, theta, and Lie blocks. |
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

The V2.7 Python certificate was executed successfully with Python. The upstream README's static scan found no `sorry`, `admit`, or custom axiom declarations, but a text scan is not a substitute for theorem-level checking.

**Independent verification of the upstream Lean release is complete.** Michael O. Rubinstein's verification record reports that all 175,187 modules compiled; the five main theorems depend only on `propext`, `Classical.choice`, and `Quot.sound`; all 175,187 modules were replayed through Lean's kernel with no rejection; and the independent Rust kernel `nanoda` checked 1,484,729 declarations with no typechecker errors. See [the verification record](https://mrubinst.github.io/grh-lean-verification/). This is independent machine verification of the formal proof, not a substitute for a complete human-readable derivation of every deep mathematical input.

The in-repository targeted CI run `45320185287` is documented in V3.23; the latest status report inspected for that run recorded it as in progress. That local workflow is a separate reproducibility track, and this README does not claim a later local success or failure. The upstream independent checks above should not be conflated with that local run.

The main remaining human-exposition bottleneck is the arithmetic inequality (M). The 22 November 2026 [working exposition hosted by Michael Rubinstein](https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/zeta-paper_v2.pdf) reduces (M) to thirteen hypotheses (H0)–(H12), but explicitly does not prove them outright. V3.25 therefore shifts the reconstruction focus from isolated module expansion to the exact Lean provenance and mathematical content of those hypotheses.

The finite arithmetic certificate checks only its stated finite examples. These are diagnostic checks, **not** a proof of the general automorphic or arithmetic Theta/Rallis hypotheses.
## Current research direction

V3.25 compressed split rigidity into three mathematical engines. V3.26 mapped the arithmetic main inequality (M) to ChainCore and isolated the central LinkDIV trace-to-main-term inequality. V3.27–V3.31 reconstructed the H9 slope bounds, Places_at, and the LinkG no-kernel family constructor. V3.32–V3.34 mapped H5 to CovolumeBoundThirdPlaceSeries and compressed the generic covolume assembly. V3.35–V3.36 traced H12 through the windowed family construction to VWinAt and the recursion/object branch. V3.37 traced the closed RH theorem through Row0b, GeoOne, and TLiftK. V3.38 reduces TLiftK to the fourteen-field Tools_k interface plus HgtEx_k.

The highest-value next work is to compress the nonvanishing block inside TLiftK (Rallis, decomposition, bump, datum, tail, and Schur control), then the Siegel–Weil/Eisenstein and compactness/Lie blocks. H5's deep geometric inputs and the H9 local divisibility chain remain separate branches of the human-proof reconstruction.

The upstream source remains pinned to Lean 4.33.1 and Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`, with the original Lean source fixed at `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`. V3.23 is a historical repository synchronization and local-CI status record; V3.38 updates the exposition and source map without changing the upstream proof source.
## License

No license has been specified. Unless and until a license is added, standard copyright restrictions apply.
