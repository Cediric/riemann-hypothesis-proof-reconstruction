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

## Source snapshot

The upstream Lean source references in the current reconstruction are pinned to:

- Repository: [CocoSgt/riemann-hypothesis-lean](https://github.com/CocoSgt/riemann-hypothesis-lean)
- Commit: [`7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`](https://github.com/CocoSgt/riemann-hypothesis-lean/commit/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4)

Do not silently replace these source links with `main`: the fixed snapshot is part of the audit trail.

## Verification

The V2.7 Python certificate was executed successfully with Python. The upstream README reports a static scan with no `sorry`, `admit`, or custom axiom declarations, but also states that no independent build/review had been published at mirroring time. This reconstruction has not independently run `lake build Main`, `#print axioms`, or `lean4checker`; the current execution environment has no Lean/Lake installation. See the [V3.0 reproducibility boundary](docs/V3.0_TLiftK_to_RH_TopLevel_Chain.md#6-公开仓库的可复核性边界).

The finite arithmetic certificate checks only its stated finite examples. These are diagnostic checks, **not** a proof of the general automorphic or arithmetic Theta/Rallis hypotheses. No new Lean compilation is claimed in this repository.

## Current research direction

The latest completed audit is V3.12, which reconstructs the local Brauer invariant from unramified levels and Frobenius evaluation, proves the Kummer perfect pairing, and expands the Bloch–Kato dimension formula through `relR`. The next target is the p-adic Hodge fundamental exact sequence, construction of Bloch–Kato cocycles from period pairs, and crystalline coboundary lifting. See [V3.12](docs/V3.12_Local_Invariant_Kummer_and_BK_Dimension.md#7-下一轮v313).

## License

No license has been specified. Unless and until a license is added, standard copyright restrictions apply.
