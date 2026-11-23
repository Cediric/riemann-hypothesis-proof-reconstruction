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
