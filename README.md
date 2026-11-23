# Riemann Hypothesis Lean Proof Reconstruction

A source-audited, human-readable reconstruction of the public Lean development associated with the claimed proof of the Riemann hypothesis.

**Important scope statement:** this repository does not claim to present a complete independent human-readable proof of RH. It distinguishes (1) kernel-checked formal proof, (2) an explanatory reconstruction of the mathematics, and (3) independent mathematical review. Any unexpanded input or unverified bridge is labelled as such.

## Published material

| Document | Contents |
|---|---|
| [V2.7 — Full reconstruction and audit draft](docs/RH_Lean_Natural_Language_Reconstruction_V2.7.md) | The working manuscript through the Theta orbit-mass, denominator, weighted-kernel, and Rallis boundary audit. This is a searchable-text Markdown export; some layout-dependent equation objects may need cross-checking against the fixed Lean sources. |
| [V2.8 — Rallis, Schur averaging, and Theta-lift nonvanishing](docs/V2.8_Rallis_Schur_ThetaLift_Nonvanishing.md) | A source-level reconstruction of the exact `Rallis_k`, `SchurStep_k`, `AbsNe`, and `NonVan_k` chain. |
| [V2.7 exact arithmetic certificate](checks/theta_mass_and_adjoint_exact_certificate_v27.py) | Finite exact-arithmetic diagnostics for orbit mass, lcm denominators, weighted adjoints/composition, a Hilbert–Schmidt inequality, and an adjoint-invariance counterexample. |

## Source snapshot

The upstream Lean source references in the current reconstruction are pinned to:

- Repository: [CocoSgt/riemann-hypothesis-lean](https://github.com/CocoSgt/riemann-hypothesis-lean)
- Commit: [`7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`](https://github.com/CocoSgt/riemann-hypothesis-lean/commit/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4)

Do not silently replace these source links with `main`: the fixed snapshot is part of the audit trail.

## Verification

The V2.7 Python certificate was executed successfully with Python. It reports:

- (S_3) orbit sizes (3,2,1) and stabilizer orders (2,3,6);
- orbit mass identity (3/6+2/6+1/6=1/2+1/3+1/6=1);
- minimal universal denominator (operatorname{lcm}(2,3,6)=6), versus product (36);
- two-layer denominator (1080) for the test instance;
- exact symbolic pass for weighted adjoint, kernel composition, and the stated Hilbert–Schmidt inequality;
- exact pass for the finite-dimensional counterexample showing that a subspace inner-product identity does not imply global adjoint invariance.

These are finite diagnostic checks, **not** a proof of the general automorphic or arithmetic Theta/Rallis hypotheses. The V2.8 note is a source reconstruction; no new Lean compilation is claimed in this repository.

## Current research direction

The next audit target is the upstream construction of the `Tools_k` package—especially the actual derivation of `swFull`, `boxSec`, `dbl`, `basic`, and `cpt`—and how those inputs are assembled into `TLift_k`. See the [V2.9 Tools_k dependency audit](docs/V2.9_Tools_Package_Construction_Audit.md#5-当前审计等级与下一步).

## License

No license has been specified. Unless and until a license is added, standard copyright restrictions apply.
