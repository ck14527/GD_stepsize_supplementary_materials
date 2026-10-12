# Check records and provenance

A report's date or location alone does not establish that its computation was
rerun. Use the classification and command in each report.

| Record | Interpretation |
|---|---|
| `environment.json`, `numerical_checks.json`, `reference_run.txt` | Inherited environment and numerical reference-run records |
| `obsf_19.csv.gz`, `obsf_exhaustive_run.txt`, `obsf_full_checks.json` | Supplied large table, inherited timing, and historical postprocessing |
| `interval_checks.json`, `interval_run.txt` | Inherited Python interval results; not Lean checks |
| `preflight.json`, `package_checks.json`, `source_baseline.json`, `original_result_inventory.json` | Historical manuscript/source packaging records; their page counts, inventories, and status fields do not describe the current folder |
| `current/` (pre-existing files) | Earlier packaging records; the name `current` is not evidence of a fresh run |
| `current/reviewer/` | New checks or later reviewer reruns using the root README commands |
| `current/plot_checks.json` | Postprocessing by the updated plotting script, if run |
| `revision/package_validation.json` | New structural and stored-hash validation; the report identifies only the computations executed by that command |
| `../lean/audit/` | Historical Lean build, declarations, coverage, and dependency evidence |

New reports should use distinct paths to preserve the inherited records. The
interval checker accepts `--output` for this purpose.

## Limits on inference

* C++/Python agreement at small horizons does not validate every large-table entry.
* Table shape, scalar identities, and reciprocal bounds do not certify every
  large-horizon asymmetric maximum.
* `||Psi_18-Psi_17||_infinity` is a successive-scale difference, not a certified
  bound on `||Psi_18-Psi_F||_infinity`.
* Hash checks establish byte identity with stored records; they do not execute
  Lean or validate a proof term.
* A Lean build certifies the formal statements under their hypotheses and
  foundational axioms. Manuscript correspondence requires a separate review.

Historical numerical and proof evidence is retained for provenance. It must
not be cited as newly measured results.

## Checks rerun for this revision

The reports in `current/reviewer/` record a new small Python reference run,
stored-table consistency check, C++/Python comparison through `N=2048`, and
the full level-17 interval calculation. The latter passed all finite-grid
inequalities, both minimizing-index checks, and separated the corner products.
The asymmetric compact panel was regenerated with the support constant from
Lemma E.5; `current/plot_checks.json` records this postprocessing.
`current/reviewer/plot_support.json` independently checks the support value at
60-digit precision and confirms that the exported line lies inside the axis.
Neither the full large Bellman search nor a fresh Lean kernel build was run.
