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
