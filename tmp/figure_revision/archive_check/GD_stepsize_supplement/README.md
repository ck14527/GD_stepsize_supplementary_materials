# Supplementary material: recursive GD stepsizes and dyadic phase laws

This anonymous review artifact accompanies *Optimal Recursive Composition and Dyadic Phase Laws for Gradient Descent with Predetermined Stepsizes*. It contains numerical implementations, figure data, and a Lean 4 formalization of the scalar and combinatorial results. The manuscript and its mathematical appendices are submitted separately as the paper PDF.

## Start here

| Review question | Entry point |
|---|---|
| What does the Lean development prove? | [LEAN_FORMALIZATION.md](LEAN_FORMALIZATION.md) |
| Which paper statement corresponds to which Lean theorem? | [lean/docs/THEOREMS.md](lean/docs/THEOREMS.md) |
| How were numerical values and plots obtained? | [NUMERICAL_REPRODUCIBILITY.md](NUMERICAL_REPRODUCIBILITY.md) |
| Which logs are historical, and which checks were rerun? | [checks/README.md](checks/README.md) |
| What is the formalization boundary? | [lean/docs/VERIFICATION.md](lean/docs/VERIFICATION.md) |

Three kinds of evidence must be distinguished:

* **Lean proofs:** scalar kernels and recurrences, optimizing splits and trees, phase laws, regularity, and specified exact finite certificates. The supplied audit maps 40 numbered scalar/combinatorial statements to Lean declarations. This does not include the external smooth-convex GD certificate theorems or every unnumbered claim.
* **Numerical interval checks:** the level-17 decimal minimum enclosure and numerical six-factor product enclosures, computed using Python integer and interval arithmetic. These are not Lean kernel verification.
* **Floating-point checks:** reference recurrences, finite-horizon Bellman tables, and plotting samples. These detect implementation errors; they do not prove claims about the limiting profile or its extremizers.

The Lean audit records a previous successful build. Matching its source hashes does not constitute a fresh kernel build. Its manuscript fingerprint differs from the current local PDF; the mapping and scope notes explain this limitation.

## Quick numerical reproduction

Use Python 3.11 or newer and install the pinned dependencies:

```bash
python -m pip install -r requirements.txt
python scripts/reference_checks.py --phi-level 12 --obsf-level 10 --output checks/current/reviewer/reference.json
python scripts/check_bundled_data.py --output checks/current/reviewer/bundled_data.json
python scripts/verify_project.py
```

The reference test compares the binary symmetric evaluator through `N=4096`, the complete maximizing-split formula through `N=256`, and the asymmetric recurrence through `N=2048`. Its low-resolution curve is a test output. The stored-table check reads all 524,288 rows, checks indices and coefficient identities, and recomputes plotted extrema; it does not repeat the large asymmetric maximization. The project verifier checks artifact structure, the SHA-256 manifest when present, and stored Lean snapshot hashes, not mathematical correctness. The exporter separately screens PDF metadata and text.

The new small numerical checks were run with the installed Python 3.13.1 and NumPy 2.2.4; the inherited environment used Python 3.13.5 and NumPy 2.3.5. The requirements retain the pinned reference dependencies. Reports record the actual environment rather than implying that this pass reinstalled the pinned one.

## Lean 4 reproduction

The project pins Lean **4.19.0** and mathlib commit `c44e0c8ee63ca166450922a373c7409c5d26b00b`. Install [elan](https://lean-lang.org/install/), then run:

```bash
cd lean
lake exe cache get
lake build GD
```

Initial downloads require internet access and additional disk space. A fresh full build can take substantially longer than the small numerical tests. The library build is the essential kernel verification step. [LEAN_FORMALIZATION.md](LEAN_FORMALIZATION.md) explains the audit, statement mapping, and unavailable historical tooling.

## Independent C++/Python comparison

With a C++17 compiler, create `build/` and `checks/current/` and run:

```bash
g++ -O3 -std=c++17 scripts/obsf_exhaustive.cpp -o build/obsf_exhaustive
./build/obsf_exhaustive 11 checks/current/obsf_11.csv
python scripts/check_bundled_data.py --cpp-check checks/current/obsf_11.csv --output checks/current/reviewer/cpp_comparison.json
```

On Windows, use `build/obsf_exhaustive.exe` as the executable name. Argument `11` means all leaf counts through `2^11=2048`, not interpolation level 11. This portable command omits machine-specific optimization flags. The inherited large run used the flags and environment in `checks/environment.json`.

## Optional interval checks and figure regeneration

```bash
python scripts/check_phase_certificate.py --output checks/current/reviewer/interval_checks.json
python scripts/prepare_phase_plots.py
python scripts/check_plot_support.py
```

The interval calculation is a separate check (about 16 seconds in this packaging run; runtime depends on the system). Plot generation needs pdfLaTeX, `standalone`, TikZ, and PGFPlots. It regenerates the level-22 symmetric display data and postprocesses the supplied asymmetric table; it does not rerun the asymmetric Bellman search. It writes compact figure sources, data, PDFs, and a new report under `checks/current/`. Use `--panel psi` to regenerate only the asymmetric panel. Its support barrier is evaluated from Lemma E.5, equations (72)-(74), giving `c_*` approximately `0.420809352823451`. The supplied PDFs can be viewed without LaTeX. The two detailed `*_original.pdf` figures are historical assets whose generating code was not supplied.

To rerun the full asymmetric search, compile the C++ program and use argument `19`. This evaluates **137,438,691,328 ordered candidate splits** with quadratic time and linear storage. The historical 81.51-second Bellman-loop timing is specific to its recorded machine and excludes CSV output and plotting.

## Files and integrity

The compact figure PDFs contain no embedded panel titles. The manuscript
places its `(a)` and `(b)` subcaptions below the images, as in the supplied
paper layout. Regeneration preserves this arrangement. The asymmetric curve
data and its reported extrema are unchanged.

| Path | Contents |
|---|---|
| `scripts/` | Numerical checks, exhaustive C++ recurrence, plotting and packaging tools |
| `lean/GD.lean`, `lean/GD/` | Definitions, theorem targets, proofs, and audit exporter |
| `lean/lean-toolchain`, `lean/lakefile.toml`, `lean/lake-manifest.json` | Exact toolchain and dependency configuration |
| `lean/docs/`, `lean/audit/`, `lean/graphs/` | Statement map, historical audit evidence, and dependency diagrams |
| `checks/obsf_19.csv.gz` | Table columns `N,U_N,W_N,C_N`; `C_N=N^p/W_N`; the schedule has `N-1` steps |
| `figures/` | Current compact sources/data/PDFs and historical detailed PDFs |
| `SHA256SUMS` | Per-file integrity manifest generated in the exported ZIP |

This folder does not contain the manuscript's complete LaTeX source. It is a code/data/proof supplement, not a compile-ready manuscript project.

Generate a clean review archive from this working folder with:

```bash
python scripts/export_anonymous.py output/GD_stepsize_supplement_ICLR2027.zip
```

The exporter excludes manuscript copies, author-only notes, version-control history, caches, machine binaries, and identifying release metadata. It preserves Lean proof inputs and writes a checksum manifest. With GNU coreutils, use `sha256sum -c SHA256SUMS` inside the extracted archive. Automated identity checks cannot establish absence of all contextual clues.

No new software license is assigned by this packaging pass. Dependencies retain their respective licenses.
