# Mathematical and Lean proof dependencies

Arrows run from a prerequisite to a dependent result. The mathematical graph records reviewed relationships between statements, definitions and external interfaces. The Lean graph records dependencies extracted from the inherited elaborated proof export, collapsing generated helper constants to named source theorems. Their edges need not coincide.

| Graph | Included data and visualization |
|---|---|
| Mathematical DAG (50 nodes) | [Registry](statement_inventory.json), [SVG](../graphs/manuscript_dag.svg), [DOT](../graphs/manuscript_dag.dot), [interactive HTML](../graphs/manuscript_dag.html) |
| Lean source-theorem DAG (623 nodes, 4,169 edges) | [JSON](../audit/lean_theorem_graph.json), [DOT](../graphs/lean_proof_dependencies.dot) |
| Transitive reduction of the Lean DAG | [SVG](../graphs/lean_proof_dependencies_reduced.svg), [DOT](../graphs/lean_proof_dependencies_reduced.dot) |

Open the SVGs at full size to zoom. Open `graphs/manuscript_dag.html` locally in a browser for the interactive mathematical view; no server is needed.

The graph colors and coverage labels summarize the inherited scalar/combinatorial audit. They do not certify the external interface nodes, all paper prose, or the current PDF snapshot. The inherited registry's PDF hash differs from the supplied manuscript; see [VERIFICATION.md](VERIFICATION.md). The [theorem table](THEOREMS.md) explains how to find each `GD.Paper.*` proof and its `GD.PaperTargets.*` statement. Internal supporting-library names retain historical numbering.

The visualizations are included artifacts. Their matching regeneration scripts and package lockfile are absent, so this supplement does not advertise graph regeneration as a reproducibility check. `python tools/check_snapshot.py` (from `lean/`) checks the mathematical registry for missing prerequisites/cycles and the inherited proof evidence; it does not rerender graphs or establish semantic correctness of an edge. Fresh Lean compilation is described in the [Lean README](../README.md).
