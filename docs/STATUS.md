# Research status — 2026-11-23

## Published

- V2.7 searchable-text reconstruction is committed in `docs/RH_Lean_Natural_Language_Reconstruction_V2.7.md`.
- The exact finite arithmetic certificate is committed in `checks/theta_mass_and_adjoint_exact_certificate_v27.py` and has been run successfully.
- V2.8 source-level reconstruction of `Rallis_k`, `SchurStep_k`, `AbsNe`, and `NonVan_k` is committed in `docs/V2.8_Rallis_Schur_ThetaLift_Nonvanishing.md`.

## Verified source-level findings

- `Rallis_k` proves integrability and the implication “zero theta lift ⇒ a specified coefficient/matrix-coefficient integral is zero”; it is not, by itself, a positivity theorem.
- `SchurStep_k` uses the finite-dimensional irreducible `SameType` package, invariant Hermitian-form uniqueness, Riesz representation, and compact-quotient averaging to obtain a nonzero scalar averaging identity.
- `AbsNe` is a measure-theoretic main-term-versus-tail lemma.
- `NonVan_k` combines local bump data, a finite set of places, coefficient support/factorization, group decomposition, Schur averaging, and tail control to contradict the Rallis vanishing implication.
- `TPGTop.tLift_of_tools_k` actually feeds this nonvanishing chain into the construction of `TLift_k`.

## Not yet established by this reconstruction

- A full independent derivation of every field in `Tools_k`.
- A complete natural-language expansion of all local representation-theoretic, automorphic, and arithmetic inputs upstream of `Tools_k`.
- A proof of the global arithmetic main inequality (M) in ordinary mathematical prose.
- A complete independent human-readable proof of RH.

## Next steps

1. Trace the construction of `Tools_k` from `TPGHolds` and its imported source modules.
2. Expand the dependencies `swFull`, `boxSec`, `dbl`, `basic`, and `cpt` into explicit mathematical statements.
3. For each dependency, separate proved Lean lemmas, imported published results, and hypotheses/bridges that still need mathematical explanation.
4. Keep every new claim pinned to a source commit and add counterexamples where a tempting inference is invalid.

## V2.9 update — 2026-11-23

- Confirmed that `Tools_k` is explicitly assembled in `TPGHolds.lean`; it is not merely passed as an unproved parameter at the `TLift_k` stage.
- Confirmed `tLift_holds_k : TLift_k` is constructed from `tools_holds_k` and `hgtEx_of_k stab2Cpt_k`.
- Traced the `cpt) field through `cptAll_of_k`, `SiegelAll`, `SiegelSetUnitary`, and the internal `SiegelCore) proof.
- Traced `swFull) through anisotropic Siegel–Weil, Eisenstein continuation, and Box-section inputs.
- Added `docs/V2.9_Tools_Package_Construction_Audit.md`.

Next: expand the standard Siegel–Weil formula's CT-splitting/Poisson inputs, then trace `TLift_k → arithmetic main inequality (M) → final RH statement`.

## V3.0 update — 2026-11-23

- Recovered the top-level chain: `TLiftK → Row0b → EveryCharacter → RiemannHypothesis`.
- Confirmed `TLiftK` is the high-rank theta-lift existence statement; it is converted to strong Galois representations through the weight-one geometric realization and crystalline descent.
- Confirmed `EveryCharacter` is the right-half-plane nonvanishing statement for all Dirichlet L-functions; the RH endpoint uses the zeta functional equation to reflect zeros.
- Recorded the three-field `OpenLiteratureStatements` construction in `MainConclusion.lean`; its Row0b fields are supplied by the proved Galois-representation theorem and the Local Langlands field by `recTExists`.
- Added `docs/V3.0_TLiftK_to_RH_TopLevel_Chain.md`.
- Important reproducibility boundary: the upstream README says no independent build/review had been published at mirroring time and recommends `lake build Main` plus `#print axioms`. The current environment has no `lean` or `lake`, so no independent compile or axiom report is claimed.

## V3.1 update — 2026-11-23

- Expanded `VWin`: it is a long-window bound for the weighted formal Galois-cohomology quantity `shaLen` over cyclotomic number fields satisfying `IsChiField`, not a generic window-existence assertion.
- Traced `Row0b → LiteratureRankNHypothesis → HypothesesH' → CountI/II/III/V/Z + LemmaK/ThmBab/ThmBcFree → VWin`.
- Traced `VWin → supplyChi → HostExW`; `TopG) plus Green and nonempty `HypsAlt) yields Chebyshev bounds on long windows.
- Confirmed `TopWin.level_of_tiedWin` uses `FormB) and a small-epsilon exponent comparison to rule out zeros with real part above 1/2.
- Expanded the other branch: `ThetaIntegralsAgree), `LocalMatching), and `CovolumeBoundOfX) feed the nonempty definite-side `HypsAlt) construction.
- Added `docs/V3.1_Sha_Windows_Chebyshev_and_ZeroFree.md`.

Next: expand CountI/II/III/V/Z and the Kato/Hida/SP4/reduced-unitary-lift estimates; separately expand the spherical closure `Tr.closeSph) and the (L^3)-type covolume estimate.

## V3.2 update — 2026-11-23

- Separated the three formal length quantities: global `shaLen` (length of a Sha submodule of H¹), `VLen` (length of H²), and local normalized `Vlen/Vn`.
- Recovered the exact CountI/II/III/IV/V/Vs/Z case split; corrected the earlier abbreviated list by recording CountIV and CountVs as actual inputs to `pointHV_of_counts`.
- Traced CountI through OneChar, KatoTwoW/Bloch–Kato vanishing, 3-dimensional Galois representations, Frobenius trace estimates, CorGK, and the global orbit sum.
- Traced CountII/III through SP4 image density and adjoint lifting; CountIV/V/Vs through field extensions, Euler characteristic, local/global duality, and host bounds; CountZ through geometric PropZ.
- Confirmed `SumIn + SumOut → PointHV → ThmHV → JointWin → VWin`.
- Added `docs/V3.2_Counts_and_Galois_Cohomology_Lengths.md`.

Next: inspect the exact theorem inputs behind `KatoTwoW), `sp4Main_alt), `ThmS6_s), `ThmBab), `ThmBcFree), and `LemmaK).

## V3.3 update — 2026-11-23

- Expanded CountI's Kato route: K4 Euler-system Iwasawa classes, K5 smoothed-zeta Hodge–Tate law, Glue2, ZetaUr, VanishOrdL, KatoTwoW, OneChar, CorGK.
- Recorded the exact role of `LemmaK): a discriminant-controlled bound for finite H² lengths; `LemmaKOfPublished` uses Poitou–Tate, local finiteness, local Tate duality, KBridge, and Hermite-normal-form torsion control.
- Traced `ThmBab) from LemmaK + Ferrero–Washington + tower bounds.
- Traced `ThmBcFree) from odd residue PsiBound via stick and prime bounds.
- Expanded the SP4 branch for CountII/III: symplectic-four image density, adjoint lifting, LemmaM/M'/P, number and rigidity inputs.
- Added `docs/V3.3_Kato_Euler_Systems_LemmaK_and_Window_Constants.md`.

Next: audit K4/K5 input packages (`Nf`, `SrcUr`, `AdmWn`, `AdmTop2)), the SP4 image/rigidity hypotheses, and CountV's Euler-characteristic inputs.


## V3.0 supplementary update — 2026-11-23

- Added a separate source-level supplement for the standard Siegel–Weil formula.
- Traced `Poisson_k` to adelic Fourier/Theta summation and reversible coordinate changes.
- Traced `CTSplit_k` to fundamental-domain independence, compact domains, absolute convergence, first-orbit identification, and the second-orbit dilation law.
- Clarified that `mainInequality_by_corank` proves the Siegel–Weil central-value identity `MainC_k 2`; it should not be conflated with a separate arithmetic inequality for Dirichlet (L)-functions.
- Added `docs/V3.0_SiegelWeil_to_Riemann_Hypothesis_Audit.md`.

## V3.4 update — 2026-11-23

- Expanded the definitions of `Nf`, `SrcUr`, and `AdmWn`.
- Traced `SrcL → Nf + SrcUr` through spherical input, newform twisting, finite coefficient fields, and integral upper-triangular conjugation.
- Confirmed that `AdmTop2` has a concrete construction theorem: `exists_admissible_hecke_projection_nonvanishing`. Its proof builds a Galois/Hecke-compatible projection, then uses finite freeness, a basis, (l)-power rescaling, and coefficient-ring enlargement to obtain integrality.
- Expanded K4's construction of `IsZWc`, `Sys`, `IwSys2`, and `SpLink`.
- Corrected the K5 proof description: `K5.top` is built by `law_of_inputs hco exists_pres_smoothed`; it is not the separate `GlobalTheory.K5.TopGeo.top` theorem.
- Traced K5's coefficient Hodge–Tate law and smoothed polynomial presentation into `HTLawCsOfCoef`.
- Traced `C7.pLocu` to the local-units argument and the power-series nonvanishing-transfer theorem.
- Confirmed the dependency direction `K4/K5/C7 → ZetaUr → VanishOrdL → KatoTwoS → KatoTwoW → VWin`; no cycle was found in the inspected module/call graph.
- Added `docs/V3.4_K4_K5_Inputs_Hecke_Projection_and_ZetaUr.md`.
- Updated the README index.

## Next steps after V3.4

1. Audit every auxiliary input passed to `glue2`, beginning with `ordinaryEisensteinEigenfunctional_exists`, `meas3`, `jEx`, `coefUb), and `mono`.
2. Continue through `psiEx`, `frobU`, `detIne`, `hatW`, `pinOf), and `smNz).
3. Trace `gmEx`, `explSmul`, `avgEq`, `avgMF`, `rhsEq`, `smSys), and `chiFix) to their theorem bodies.
4. For each input, distinguish proved construction, imported mathematical result, explicit hypothesis, and any unverified bridge.
5. Continue the independent axiom/dependency audit when a Lean/Lake environment is available; do not infer build success from source browsing.
