# Lean 4 formalization: reviewer guide

This directory accompanies *Optimal Recursive Composition and Dyadic Phase Laws for Gradient Descent with Predetermined Stepsizes*. It formalizes the paper's **scalar recurrences and combinatorial model**. The external smooth-convex gradient-descent certificates and their tightness interpretation are outside the formalization.

Start with [the supplement's formalization guide](../LEAN_FORMALIZATION.md), [the 40-result correspondence table](docs/THEOREMS.md), and [the trust boundary](docs/VERIFICATION.md). The entry point is [GD.lean](GD.lean). The toolchain is **Lean 4.19.0**, with mathlib pinned to `c44e0c8ee63ca166450922a373c7409c5d26b00b` in `lakefile.toml` and transitive revisions fixed by `lake-manifest.json`.

## What the included evidence establishes

The inherited audit records 40 numbered scalar/combinatorial targets, 623 named source theorems, and 1,602 exported declarations. A read-only consistency check on 2026-09-24 confirmed that all 74 proof inputs and the elaborated export match the inherited build provenance. The exported theorem axiom closures contain only `propext`, `Classical.choice`, and `Quot.sound`; no exported project `unsafe` or `partial` definition occurs in the named theorem proof/type closures.

**Historical preparation (2026-09-24):** that preparation did not perform a fresh Lean build because the required Lean 4.19.0 toolchain and mathlib cache were unavailable locally. Existing `audit/run_checks.json` describes an earlier run, including an incremental build; its timings are not clean-install estimates.

**Manuscript version caveat:** the current supplied PDF has SHA-256 `e38f43f82aca4cf4e26d3f58d202a853aedee2bfd4be0d6c9f1fb1a5d6374003`, whereas the inherited correspondence registry names `db3137a4cc77fcebf4f7956f4afdccd5ed51dd006e32dec69657f84843898fc9`. The table is a guide to the registered statements, not evidence of byte-identical manuscript provenance. Review the final PDF-to-Lean correspondence before making a final-version completeness claim.

## Current repository verification

The public supplementary-materials repository now runs **Lean formal verification** on GitHub Actions for pushes, pull requests, and manual runs. The workflow checks the preserved source hashes, performs a clean `lake build GD` with the pinned toolchain and dependency revisions, exports the newly compiled declarations, and runs [the elaborated-declaration audit](tools/check_elaborated.py). No project build cache is restored.

The audit rejects `sorryAx` and every theorem axiom except `propext`, `Classical.choice`, and `Quot.sound`. It checks all named source theorems, all 40 exact registered targets, and the project proof/type dependency closures for custom axioms and unsafe or partial definitions. The workflow publishes the current export, audit report, toolchain version, and verified commit as downloadable evidence. Historical `audit/` files remain unchanged. The public repository's badge and run page show the actual execution status.

## Reproduce the checks

From this `lean/` directory, Python 3.11+ can check the supplied evidence without downloads:

```bash
python tools/check_snapshot.py
```

Expected: `snapshot_consistent: true`, `registered_scalar_results: 40`, `manuscript_hash_matches: null`, and `fresh_lean_build_performed: false`. The separate code/proof supplement does not include the main submission PDF. Optionally place it in the supplement root and add `--manuscript ../GD_stepsize_schedule.pdf`; the locally reviewed version returns `manuscript_hash_matches: false`. Adding `--require-manuscript-match` returns exit code 2 for a missing or different PDF. Exit code 0 alone does not certify a matching PDF or perform kernel checking.

To compile the proofs afresh, install elan with the pinned toolchain and run:

```bash
lake exe cache get
lake build GD
```

Initial toolchain, package, and cache downloads require network access. Compilation uses CPU and RAM; no GPU, dataset, API key, or commercial software is required. A measured fresh-build time and peak-memory figure are not supplied.

For an elaborated-environment export, in a separate working copy run:

```bash
lake env lean GD/Audit.lean
```

This last command **overwrites** `audit/lean_declarations.json`. It does not update the other provenance/coverage reports. Preserve the original audit when comparing a new export. Successful compilation and snapshot consistency are different checks; see [VERIFICATION.md](docs/VERIFICATION.md).

## Entry points and files

| Path | Reviewer use |
|---|---|
| `GD/Paper/Composition.lean` | Theorems 3.1-3.2, Propositions A.5-A.6, Appendices B-C; scalar evaluator theorem `algorithm_1` |
| `GD/Paper/CompositionLaw.lean` | Explicit hypotheses of the abstract nonnegative composition law in Theorem B.4 |
| `GD/Paper/Symmetric.lean` | Theorem 4.1, Corollary 4.2, Appendix D; regularity, corners and exact grid bounds |
| `GD/Paper/Asymmetric.lean` | Theorem 5.1 and Appendix E; actual asymmetric recurrence, uniform phase and support separation |
| `docs/THEOREMS.md`, `docs/THEOREMS.csv` | Complete registered theorem-to-paper mapping and scope notes |
| `docs/statement_inventory.json`, `audit/` | Inherited correspondence registry, proof export, hashes and audit reports |
| `tools/check_snapshot.py` | Read-only, standard-library consistency check added for this supplement |
| `graphs/`, `docs/DEPENDENCIES.md` | Included mathematical and Lean dependency visualizations |

The previous documentation mentioned a historical full audit runner and documentation generator. Their matching versions are absent from this supplement, so those commands are no longer advertised. The current root-level CI workflow is separately implemented and uses the supplied proof library and declaration exporter. [Chinese guide](docs/README_zh.md) is also available.
