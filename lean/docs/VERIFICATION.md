# Verification scope, evidence and trust boundary

The project formalizes exact real-valued kernels, recursive optima, finite composition trees and their phase laws. The inherited registry contains **40 numbered scalar/combinatorial statements**. It does not establish every claim in the paper as a Lean theorem.

## Recorded evidence and current validation

The original [build provenance](../audit/build_provenance.json) records a successful build/export; [run_checks.json](../audit/run_checks.json) records exit code 0 for that earlier run. A read-only check during supplement preparation on 2026-09-24 established the following:

| Check | Result |
|---|---|
| SHA-256 of all Lean source and toolchain/dependency inputs | All 74 inputs match the inherited provenance, including all four files under `GD/Paper/` |
| Elaborated declaration export | SHA-256 matches the inherited provenance; 1,602 exported declarations |
| Named source theorems | 623 source declarations found and present as theorems in the export |
| Registered numbered targets | All 40 have a named theorem with the exact registered `GD.PaperTargets.*` type |
| Exported theorem axiom closures | Only `propext`, `Classical.choice`, and `Quot.sound` |
| Exported project proof/type closures | No `unsafe` or `partial` definitions and no project axiom declarations used |
| Fresh Lean kernel build in this preparation | **Not performed**: pinned Lean 4.19.0 and the dependency cache were unavailable locally |
| Current manuscript hash versus inherited mapping | **Different**; see below |

These are consistency checks of supplied records, not independent proof checking. Hash agreement binds files to records but does not authenticate the original build execution. A fresh build is the reproducible kernel-checking step. Named source theorems, numbered manuscript statements and compiler-generated declarations have different counts.

The registry refers to manuscript SHA-256 `db3137a4cc77fcebf4f7956f4afdccd5ed51dd006e32dec69657f84843898fc9`. The supplied `GD_stepsize_schedule.pdf` has SHA-256 `e38f43f82aca4cf4e26d3f58d202a853aedee2bfd4be0d6c9f1fb1a5d6374003`. A different hash alone does not imply a mathematical change, but prevents claiming identical manuscript provenance. The final PDF needs a statement-by-statement semantic review before its hash is registered. Old audit JSON is preserved as historical evidence; it has not been relabeled as a fresh run or rewritten to hide this difference. `audit/source_sha256.json` also includes hashes of older documentation and missing historical tooling; it is not a manifest of the revised submission package.

## Current clean build and compiled-declaration audit

The public supplementary-materials repository now has a root-level **Lean formal verification** workflow. Each run starts from the specified Git commit, uses Lean 4.19.0 and the exact recorded mathlib revision, retrieves the dependency cache, and executes `lake build GD` without restoring project build products. The historical preparation described above is a separate event.

After the build succeeds, the workflow runs `lake env lean GD/Audit.lean` and audits that newly generated declaration export with `tools/check_elaborated.py`. It verifies all named source theorems and the exact targets of all 40 registered statements, rejects `sorryAx` and other unsupported theorem axioms, and checks the project theorem closures for custom axioms and unsafe or partial definitions. Only `propext`, `Classical.choice`, and `Quot.sound` are allowed. The current export, audit report, toolchain version and commit are published as workflow artifacts; the inherited declaration export is restored without modification.

A successful run establishes Lean compilation and these compiled-environment properties for its exact proof inputs. It does not extend the mathematical scope below or establish a new semantic correspondence with the final PDF. The public workflow run page reports whether the current execution has succeeded.

## Formalized mathematics and exclusions

| Topic | Precise scope |
|---|---|
| Kernels and balanced composition | Exact real kernels `K` and `A`, rearrangement/equality cases, balanced recursive optimum, all optimizing splits, finite trees and exact tree-count recurrence |
| Symmetric phase | Exact recurrence and scaling, periodic profile, regularity, objective-coefficient identity, uniform remainder and cluster interval |
| Asymmetric phase | Actual Bellman recursion and canonical phase, dyadic-block uniform convergence, sharp support inequalities, nonconstancy and strict support separation |
| Abstract Theorem B.4 | A theorem for every `NonnegativeCompositionLaw`, under its displayed nonnegative-domain hypotheses; see the distinction below |
| Proposition A.5 and schedule interpretation | Treewise/scalar conjugacies and Bellman optimum are proved. Smooth-convex function classes, GD trajectories, imported closure certificates and worst-case tightness constructions are outside the Lean model |
| Corollaries 4.2, D.7 and Theorem 5.1 | Scalar objective coefficients are formalized. Interpreting them as tight GD guarantees relies on the externally cited certificate results |
| Proposition C.5 | The numbered finite-tree recurrence and its cases are covered; the subsequent unnumbered asymptotic paragraph and sample table are not its target |
| Corollary D.9 | One-sided derivative separation and nondifferentiability, including an exact finite rational certificate checked through Lean proof terms |
| Proposition D.10 | General exact grid bounds and limits, with `30 * 2^k` work for one level and `60 * 2^k` through level k in the stated real-RAM model; real powers are primitive operations |
| Numerical figures and level-17 decimals | Floating-point plots and the optional printed decimal enclosure are not Lean-certified interval evaluations. The theorem about a grid scheme is separate from a particular numerical run |
| Broader claims | No minimax optimality over all positive predetermined stepsize schedules and no end-to-end formal verification of the Python plotting implementation |

The complete [correspondence table](THEOREMS.md) supplies result-specific notes. Entry points are in [Composition.lean](../GD/Paper/Composition.lean), [Symmetric.lean](../GD/Paper/Symmetric.lean), and [Asymmetric.lean](../GD/Paper/Asymmetric.lean).

### Explicit assumptions versus external interfaces

`GD.NonnegativeCompositionLaw` in [CompositionLaw.lean](../GD/Paper/CompositionLaw.lean) packages an operator, a scale greater than one, nonnegativity, symmetry, identity at zero, diagonal scaling, homogeneity, strict monotonicity and the four-point inequalities, with their domains. `GD.Paper.theorem_B_4` proves balanced optimality for every object satisfying those hypotheses. These hypotheses are ordinary theorem parameters; the desired conclusion is not assumed. The concrete kernel results are proved elsewhere in the development.

The imported smooth-convex composition certificates are a different boundary: this project does not encode or prove their trajectory-level statements. They enter the manuscript's interpretation of the scalar model, not as hidden custom axioms in the Lean theorems. Absence of custom axioms therefore does not mean that the entire GD application is formalized.

## Trusted components

The pinned toolchain is Lean 4.19.0, with mathlib commit `c44e0c8ee63ca166450922a373c7409c5d26b00b` and transitive dependencies in `lake-manifest.json`. Kernel checking relies on this Lean implementation and its standard foundations, not an independently implemented checker.

The exported theorem axiom closures contain no `sorryAx`, custom mathematical axiom or `native_decide` oracle. The source scan found no `sorry`, `admit` or `native_decide` tokens. A source-text scan alone would not establish this property; the axiom evidence comes from `Lean.collectAxioms` in [GD/Audit.lean](../GD/Audit.lean). The export contains two generated `_elambda_1` records classified as axioms and generated unsafe runtime constants outside all named theorem proof/type closures. They are not assumptions of the proved theorems. The exporter omits inductive types, constructors and recursors from its JSON rows; it is a theorem-audit export, not a complete serialized Lean environment.

Every registered result is represented by a `GD.PaperTargets.*` proposition and a `GD.Paper.*` theorem whose whole elaborated type is exactly that target. A target definition by itself is not a proof. The human claim that a target faithfully represents a PDF statement is a separate semantic review; the audit does not derive it by parsing the PDF.

## Reproduction

From `lean/`, check the inherited snapshot without modifying it:

```bash
python tools/check_snapshot.py
```

Exit 0 means consistent inherited evidence. The separate code/proof supplement does not include the main submission PDF, so `manuscript_hash_matches` is null by default. If that PDF is placed in the supplement root, add `--manuscript ../GD_stepsize_schedule.pdf`; the locally reviewed version returns false. `--require-manuscript-match` makes a missing/different manuscript an exit-2 failure. The script uses only the Python standard library and explicitly reports that no fresh build or semantic PDF comparison was performed.

For a fresh proof build with the pinned toolchain installed:

```bash
lake exe cache get
lake build GD
```

This compiles every imported proof in the root library. Cache retrieval needs initial network access. No GPU or dataset is required; a fresh-build duration and peak RAM have not been measured for this package. The inherited two-second build timing is incremental and must not be used as a clean-build estimate.

To export current elaborated types, references and axioms, run `lake env lean GD/Audit.lean` in a separate copy. It writes `audit/lean_declarations.json`; it does not regenerate provenance, the correspondence registry, or all audit reports. Recheck the new export against the intended sources and inspect its axiom closures before recording new provenance. The historical full-runner and graph-generation scripts are not supplied. The public repository now provides a separate clean-build and compiled-declaration CI workflow; its run records and artifacts report the actual execution results.
