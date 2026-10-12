# Lean 4 formalization in the supplementary material

This supplement provides Lean 4 proofs for the paper's **scalar recurrences, composition trees and phase laws**. It also provides Python computations and figures, described separately in [NUMERICAL_REPRODUCIBILITY.md](NUMERICAL_REPRODUCIBILITY.md). A plotted curve, a numerical interval certificate and a Lean theorem provide different kinds of evidence.

## Reviewer entry points

The formalization is in [`lean/`](lean/README.md). The library entry point is [`lean/GD.lean`](lean/GD.lean). Each registered numbered result has a statement under `GD.PaperTargets` and a theorem under `GD.Paper` with that exact statement as its entire type. The [complete correspondence table](lean/docs/THEOREMS.md) lists all 40 registered numbered scalar/combinatorial results and their limitations. Names in older support modules may use historical paper numbering; use `GD.Paper.*` to locate the manuscript-facing statements.

| Manuscript topic | Selected declarations | File |
|---|---|---|
| Balanced optimality and rearrangement | `GD.Paper.theorem_3_1`, `GD.Paper.theorem_3_2` | [Composition.lean](lean/GD/Paper/Composition.lean) |
| Scalar/tree conjugacy and abstract composition | `GD.Paper.proposition_A_5`, `GD.Paper.theorem_B_4` | [Composition.lean](lean/GD/Paper/Composition.lean), [CompositionLaw.lean](lean/GD/Paper/CompositionLaw.lean) |
| Optimal recursive trees and counts | `GD.Paper.theorem_C_3`, `GD.Paper.corollary_C_4`, `GD.Paper.proposition_C_5` | [Composition.lean](lean/GD/Paper/Composition.lean) |
| Exact symmetric phase and objective coefficient | `GD.Paper.theorem_4_1`, `GD.Paper.corollary_4_2` | [Symmetric.lean](lean/GD/Paper/Symmetric.lean) |
| Regularity, dyadic corner and grid bounds | `GD.Paper.proposition_D_8`, `GD.Paper.corollary_D_9`, `GD.Paper.proposition_D_10` | [Symmetric.lean](lean/GD/Paper/Symmetric.lean) |
| Asymmetric phase and strict support separation | `GD.Paper.theorem_5_1`, `GD.Paper.theorem_E_4`, `GD.Paper.theorem_E_13` | [Asymmetric.lean](lean/GD/Paper/Asymmetric.lean) |

## What is proved, assumed and computed

The formalized objects are exact real-number kernels, the actual symmetric and asymmetric recursive values, finite composition trees, and their limiting profiles. The proofs establish balanced optimality, all equality cases and optimizing tree structures, exact symmetric scaling, asymmetric uniform phase convergence, regularity and support separation within this model.

Theorem B.4 is an abstract conditional theorem. `GD.NonnegativeCompositionLaw` explicitly lists its operator hypotheses, including homogeneity, monotonicity and four-point rearrangement. `GD.Paper.theorem_B_4` proves the conclusion for every operator satisfying those hypotheses. These are visible mathematical parameters, not custom Lean axioms that assume the conclusion.

The smooth-convex GD composition certificates cited in Appendix A are external to this development. The project does not formalize smooth-convex function classes, GD trajectories, certificate-validity/tightness constructions, or the complete translation from scalar recurrences to worst-case GD guarantees. Proposition A.5 covers the scalar/treewise conjugacies. The GD interpretation of Corollaries 4.2 and D.7 and the asymmetric objective coefficient still uses the cited external results. This distinction remains necessary even when every registered scalar theorem is proved.

The exact finite rational certificate supporting the dyadic corner in Corollary D.9 is included in the Lean proofs. Proposition D.10 proves the general exact grid bounds and their limits. Its complexity is in a real-RAM model with real powers as primitive operations. The optional level-17 decimal enclosure is reproduced by the separate numerical interval checker described in [NUMERICAL_REPRODUCIBILITY.md](NUMERICAL_REPRODUCIBILITY.md); it is **not** a Lean-certified interval evaluation. The Python phase plots, finite Bellman computations and their floating-point outputs are also outside the Lean proof guarantee. No broader minimax claim over all predetermined positive stepsize schedules is made by this formalization.

## Verification status of this package

The toolchain is pinned to **Lean 4.19.0** and mathlib commit `c44e0c8ee63ca166450922a373c7409c5d26b00b`; transitive revisions are fixed in `lean/lake-manifest.json`.

The supplied `lean/audit/` files record an earlier successful build/export. A read-only check on 2026-09-24 confirmed that all 74 proof inputs and the elaborated export agree with the inherited SHA-256 provenance, that all 623 named source theorems are present, and that all 40 registered results have the exact intended target type. The exported theorem axiom closures use only `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx`, additional mathematical axioms, or `native_decide` oracle occurs in those closures. Exported unsafe/partial project definitions are absent from theorem proof/type closures. See [the detailed trust boundary](lean/docs/VERIFICATION.md), including generated runtime constants that are outside the proofs.

**No fresh Lean build was completed during this supplement preparation.** The pinned toolchain and mathlib cache were unavailable locally. The inherited audit is evidence associated with the supplied sources; its two-second build timing was incremental, not a measured clean build. A fresh build is the independent reproduction step. Python record consistency is not kernel proof checking.

**The manuscript provenance needs final reconciliation.** The inherited correspondence registry records PDF SHA-256 `db3137a4cc77fcebf4f7956f4afdccd5ed51dd006e32dec69657f84843898fc9`; the supplied `GD_stepsize_schedule.pdf` has SHA-256 `e38f43f82aca4cf4e26d3f58d202a853aedee2bfd4be0d6c9f1fb1a5d6374003`. This need not indicate a mathematical difference, but the registry cannot be described as tied to the exact current PDF bytes. Review the final manuscript statements against the target definitions before renewing the provenance. The historical audit records have been preserved without replacing their original hash.

## Reproduction commands

From the supplement root, inspect the inherited evidence using Python 3.11+ and only its standard library:

```bash
python lean/tools/check_snapshot.py
```

For the separate code/proof supplement, `snapshot_consistent` is true and `manuscript_hash_matches` is null because the main submission PDF is not included. Exit code 0 certifies only consistency of the recorded Lean evidence. Optionally place the main submission PDF at the supplement root and run `python lean/tools/check_snapshot.py --manuscript GD_stepsize_schedule.pdf`; the locally reviewed PDF yields `manuscript_hash_matches: false`. Add `--require-manuscript-match` to make an absent or different PDF an exit-2 failure. The script does not rewrite the audit, download dependencies, compile Lean, or compare PDF prose semantically.

With elan and the pinned Lean version available, compile the mathematics:

```bash
cd lean
lake exe cache get
lake build GD
```

Initial toolchain/dependency/cache downloads need internet access. No GPU, external dataset or private credential is needed. A fresh-build time and peak-memory measurement are not provided. To inspect a new elaborated export, run `lake env lean GD/Audit.lean` in a separate working copy; that command overwrites its `audit/lean_declarations.json` and does not renew the other reports automatically. Preserve the supplied evidence when comparing runs.

The former documentation referred to a full audit runner, documentation generator and CI workflow that are absent from this package. The commands above use files actually supplied here. [Dependency graphs](lean/docs/DEPENDENCIES.md) are included for navigation; their regeneration is not a required verification step.
