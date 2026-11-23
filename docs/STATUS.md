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


## V3.5 update — 2026-11-23

- Expanded `ordinaryEisensteinEigenfunctional_exists` to its exact `CuspidalUnitaryTwistsClaim` output: level raising, primitive character, Hecke eigenfunctional, `MeasMu`, and nondegenerate smoothing parameters.
- Traced `TowerEx` to the construction of a standard modular-function tower using the modular-function fraction field, (j)-invariant, analytic germs, Shimura reciprocity, bounded denominators, and saturation.
- Expanded `Meas3`: bounded distributions produce an integral-coefficient (l)-adic power series, with primitive-root Gauss-sum congruences and a nonvanishing mass bound.
- Traced `JEx` to a valuation-preserving embedding and `CoefUb` to coefficient-ring upper bounds plus finite-set integrality.
- Verified `Mono` transfers `Sys`, `IwSys2), and `HTLawCsOfCoef) under coefficient-ring inclusion.
- Added `docs/V3.5_Glue2_Foundational_Inputs_Eisenstein_Towers_and_Measure.md`.

## V3.6 update — 2026-11-23

- `PsiEx` factors Galois characters through the mod-(l) cyclotomic quotient using `KillsMu` and surjectivity of `cyc1`.
- `FrobU` derives existence of a Frobenius element and unit norm of the ordinary diagonal entry from the integral upper-triangular form.
- `DetIne` uses newform characteristic polynomials and Chebotarev degree-one density to obtain the inertia determinant relation.
- `HatW` uses finite Fourier transform invertibility, non-Archimedean norm bounds, and periodicity.
- `SmNz` is reduced to an explicit factorization of the four smoothing terms.
- `GmEx` is an explicit lower-triangular (SL_2(mathbb Z)) matrix construction.
- `ExplSmul` preserves congruence conditions under multiplication by (l^m).
- `PinOf` combines `Meas3`, `CoefUb`, `Mono), and `Expl` to construct the `Pin7) package.
- Added `docs/V3.6_Glue2_Representation_Local_Inputs_and_Pin7.md`.
- Updated the README index.

## Next steps after V3.6

1. Audit `AvgEq), `AvgMF), `RhsEq), `SmSys), and `ChiFix) by reading both their proposition definitions and proof bodies.
2. Read `glue2` line by line and map each input to the exact field/lemma it discharges.
3. Verify the final construction of `ExistsZetaEulerSystemIwasawaData Pin7) and identify every nonzero scalar, coefficient-ring enlargement, and smoothing parameter.
4. Recheck whether any `glue2` inputs are only theorem wrappers to CompanionTheory or other imported modules; record the exact source and proof boundary.
5. When Lean/Lake is available, run the target build and axiom/dependency checks; source browsing alone is not build verification.


## V3.5 supplementary deep dive — 2026-11-23

- Revisited the ordinaryEisensteinEigenfunctional_exists input already summarized in the V3.5 Glue2 audit.
- Corrected the proof-boundary classification: the Statement file is a thin wrapper, but chapterM_holds is proved in the same upstream repository in OrdinaryEisensteinEigenfunctionalExists.lean; it is not an external CompanionTheory black box.
- Expanded depleted_newform_prim: level raising, coefficient depletion, change-level character, and preservation of Hecke relations away from the enlarged level.
- Expanded unitRoot_split: a quadratic-root argument using the non-Archimedean norm to select a unit-root eigenvalue.
- Traced eigF_of_prim to a Petersson functional represented by finitely many q-expansion coefficients via a Sturm bound; Hecke T/U adjointness supplies the eigenrelations.
- Traced the nonzero functional value to Rankin unfolding, two twisted L-values, and a nonzero Gamma-factor limit.
- Expanded Atkin–Lehner extension from EigF to EigAll, including the finite-dimensional functional extension and Hecke intertwining.
- Traced val_depleted_ne_zero through Eisenstein products, Atkin–Lehner transforms, U-operator eigenrelations, and the nonzero Petersson value.
- Expanded MeasMu into level compatibility, non-Archimedean boundedness, finite coefficient field, and interpolation.
- Expanded twisted_lvalue_ne_zero_edge: Rankin mean-square bounds, entire continuation, global Euler positivity, and reciprocal-prime divergence from APLogDensity.
- The inspected analytic route proves nonvanishing only in the specified right-edge region and does not invoke EveryCharacter or the final RH theorem; no circular dependency was found along this path.
- Added docs/V3.5_Ordinary_Eisenstein_Eigenfunctional_Construction.md as a supplement to the broader V3.5 Glue2 input audit.

This supplement does not change the next-step priority after V3.6: audit AvgEq, AvgMF, RhsEq, SmSys, and ChiFix, then inspect glue2 line by line.


## V3.7 update — 2026-11-23

- Expanded the exact propositions `AvgEq`, `AvgMF`, `RhsEq`, `SmSys`, and `ChiFix`.
- Traced `ser_eq_Zm` to finite Fourier transforms, divisor-sum expansions, and the parity projector; `avgEq` follows from finite character orthogonality and linearity of `Zm`.
- Traced `avgMF` through finite Dirichlet-character Fourier expansion, local Eisenstein-product modularity, `U_l` level lowering, and the `EigAll.kill` projection onto the unique surviving character component.
- Expanded `rhsEq` as an exact four-term expansion of the Kummer projection, using `AvgEq`, `AvgMF`, and the finite unit-group sum; the parity-mismatched branch vanishes.
- Expanded `smSys`: `Sys` is stable under scalar multiplication, `IwSys2` under the smoothing difference and unit reindexing, and `SpLink` under the corresponding ultrametric congruence estimate.
- Expanded `chiFix` as the standard zero extension of the unit-part character to a multiplicative, modulo-N periodic function.
- Read `glue2` line by line: K4 constructs the raw Euler/Iwasawa system; K5 supplies the Hodge–Tate law; `RhsEq` converts it to the eight-term smoothed law; `ExplSmul` and `Mono` handle scaling and coefficient-ring enlargement; `PinOf` constructs `Pin7`; `SmSys` supplies the final smoothed system structures.
- Unpacked `ExistsZetaEulerSystemIwasawaData Pin7`: the output includes `Sys`, `IwSys2`, `SpLink`, and the full Pin7 package of local Frobenius/inertia, power-series, Hodge–Tate, primitive-root congruence, and nonvanishing data.
- Added `docs/V3.7_AvgEq_AvgMF_RhsEq_Smoothing_and_Glue2.md` and updated the README index.

## Next steps after V3.7

1. Re-audit the connection from `ExistsZetaEulerSystemIwasawaData Pin7` through the local nonvanishing package `C7.pLocu` to `ZetaUr`, checking for duplicated, missing, or strengthened conditions.
2. Review the upstream CompanionTheory Newform API and its pinned dependency version, especially the foundational modular-form, Hecke, Eisenstein, and Petersson interfaces.
3. When Lean/Lake is available, run the target build and axiom/dependency checks; source browsing alone is not build verification.
4. Reconnect the verified K4/K5/Glue2 chain to the `VWin → EveryCharacter → RH` endpoint and audit the remaining top-level bridges.
