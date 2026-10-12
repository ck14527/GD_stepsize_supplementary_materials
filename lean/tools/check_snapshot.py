#!/usr/bin/env python3
"""Read-only consistency check of the supplied Lean audit snapshot.

This checks recorded evidence, not Lean proofs or prose/Lean equivalence. It
does not need Lean, network access, or third-party Python packages, and never
rewrites the inherited audit. Run a fresh Lean build separately.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_theorems(root):
    """Recognize this project's source style; this is not a Lean parser."""
    result = {}
    for path in sorted((root / "GD").rglob("*.lean")):
        stack = []
        for line in path.read_text(encoding="utf-8").splitlines():
            text = line.strip()
            match = re.match(r"^namespace\s+(\S+)", text)
            if match:
                stack.append(("namespace", match[1]))
                continue
            if re.match(r"^(noncomputable\s+)?section\b", text):
                stack.append(("section", ""))
                continue
            if re.match(r"^end(?:\s+\S+)?\s*$", text):
                if stack:
                    stack.pop()
                continue
            match = re.match(r"^(?:@\[[^]]*\]\s*)?theorem\s+([^\s(:]+)", text)
            if match:
                name = ".".join([v for k, v in stack if k == "namespace"] + [match[1]])
                if name in result:
                    raise ValueError("Duplicate source theorem: " + name)
                result[name] = path.relative_to(root).as_posix()
    return result


def check(root, manuscript=None):
    errors = []
    provenance = read_json(root / "audit/build_provenance.json")
    paths = [root / name for name in ("GD.lean", "lean-toolchain", "lakefile.toml", "lake-manifest.json")]
    paths += sorted((root / "GD").rglob("*.lean"))
    current = {p.relative_to(root).as_posix(): digest(p) for p in paths}
    recorded = provenance["files"]
    differences = sorted(n for n in current.keys() | recorded.keys() if current.get(n) != recorded.get(n))
    if differences:
        errors.append({"proof_input_mismatches": differences})
    export_matches = digest(root / "audit/lean_declarations.json") == provenance["elaborated_export_sha256"]
    if not export_matches:
        errors.append("Elaborated export does not match its recorded hash.")

    rows = read_json(root / "audit/lean_declarations.json")
    by_name = {r["name"]: r for r in rows}
    if len(by_name) != len(rows):
        errors.append("Duplicate names in elaborated export.")
    named = source_theorems(root)
    for name in named:
        if name not in by_name or by_name[name]["kind"] != "theorem":
            errors.append("Missing exported source theorem: " + name)

    unexpected_axioms = sorted({a for r in rows if r["kind"] == "theorem" for a in r["axioms"]} - ALLOWED_AXIOMS)
    if unexpected_axioms:
        errors.append({"unexpected_theorem_axioms": unexpected_axioms})
    closure = set()
    todo = list(named)
    while todo:
        name = todo.pop()
        if name in closure:
            continue
        closure.add(name)
        row = by_name.get(name)
        if row is None:
            # The exporter intentionally omits inductive types, constructors,
            # recursors and other constants classified as `other`.
            continue
        todo.extend(row["proof_references"] + row["type_references"])
    unsafe = sorted(n for n in closure if n in by_name and by_name[n]["safety"] in {"unsafe", "partial"})
    if unsafe:
        errors.append({"unsafe_or_partial_in_project_proof_closure": unsafe})
    used_project_axioms = sorted(n for n in closure if n in by_name and by_name[n]["kind"] == "axiom")
    if used_project_axioms:
        errors.append({"project_axioms_in_proof_closure": used_project_axioms})

    registry = read_json(root / "docs/statement_inventory.json")
    coverage = read_json(root / "audit/coverage.json")
    statements = [n for n in registry["nodes"] if n["kind"] in {"Theorem", "Lemma", "Proposition", "Corollary"}]
    coverage_by_id = {r["paper_id"]: r for r in coverage["results"]}
    if len(statements) != 40 or len(coverage_by_id) != 40:
        errors.append("Expected 40 registered numbered scalar/combinatorial statements.")
    for statement in statements:
        entry = coverage_by_id.get(statement["id"], {})
        for key in ("proof_declarations", "target_definition"):
            if entry.get(key) != statement.get(key):
                errors.append("Registry/coverage mismatch: " + statement["id"] + " / " + key)
        target = statement["target_definition"]
        if by_name.get(target, {}).get("kind") != "definition":
            errors.append("Missing target definition: " + target)
        for proof in statement["proof_declarations"]:
            row = by_name.get(proof, {})
            if proof not in named or row.get("kind") != "theorem" or row.get("exact_type_constant") != target:
                errors.append("Proof does not have its exact registered target: " + proof)
    if coverage["source_pdf_sha256"] != registry["source_pdf_sha256"]:
        errors.append("Registry and coverage refer to different manuscript snapshots.")

    graph = {n["id"]: n["depends_on"] for n in registry["nodes"]}
    done = set()
    while len(done) < len(graph):
        ready = {n for n, deps in graph.items() if n not in done and set(deps) <= done}
        if not ready:
            errors.append("Mathematical registry has a cycle or an unknown prerequisite.")
            break
        done.update(ready)

    # Collapse exported auxiliary references in the same way as the inherited
    # graph, and compare every edge rather than trusting its displayed counts.
    edges = set()
    for theorem in named:
        todo = list(by_name.get(theorem, {}).get("proof_references", []))
        seen = set()
        while todo:
            dependency = todo.pop()
            if dependency in seen:
                continue
            seen.add(dependency)
            if dependency in named:
                edges.add((dependency, theorem))
            elif dependency in by_name:
                row = by_name[dependency]
                todo.extend(row["proof_references"] + row["type_references"])
    lean_graph = read_json(root / "audit/lean_theorem_graph.json")
    recorded_edges = {(e["from"], e["to"]) for e in lean_graph["edges"]}
    if set(lean_graph["nodes"]) != set(named) or recorded_edges != edges:
        errors.append("Inherited Lean dependency graph differs from the exported theorem references.")
    order = lean_graph["topological_order"]
    positions = {name: i for i, name in enumerate(order)}
    if len(positions) != len(order) or set(positions) != set(named) or any(
        positions.get(a, -1) >= positions.get(b, -1) for a, b in edges
    ):
        errors.append("Inherited Lean dependency graph has an invalid topological order.")

    paper_hash = digest(manuscript) if manuscript and manuscript.is_file() else None
    paper_matches = paper_hash == registry["source_pdf_sha256"] if paper_hash else None
    return {
        "check": "read-only consistency of inherited Lean evidence; not fresh kernel verification",
        "snapshot_consistent": not errors,
        "proof_input_files": len(current),
        "proof_input_mismatches": differences,
        "elaborated_export_hash_matches": export_matches,
        "named_source_theorems": len(named),
        "exported_declarations": len(rows),
        "registered_scalar_results": len(statements),
        "mathematical_graph_nodes": len(graph),
        "lean_graph_nodes": len(named),
        "lean_graph_edges": len(edges),
        "unexpected_theorem_axioms": unexpected_axioms,
        "unsafe_or_partial_in_project_proof_closure": unsafe,
        "project_axioms_in_proof_closure": used_project_axioms,
        "generated_axiom_records_outside_proof_closure": sorted(r["name"] for r in rows if r["kind"] == "axiom" and r["name"] not in closure),
        "registered_pdf_sha256": registry["source_pdf_sha256"],
        "supplied_pdf_sha256": paper_hash,
        "manuscript_hash_matches": paper_matches,
        "fresh_lean_build_performed": False,
        "semantic_correspondence_checked_by_this_script": False,
        "errors": errors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manuscript", type=Path, help="Optional PDF for byte-for-byte comparison with the recorded manuscript hash.")
    parser.add_argument("--require-manuscript-match", action="store_true", help="Fail if the manuscript is absent or differs from the registered snapshot.")
    args = parser.parse_args()
    try:
        report = check(ROOT, args.manuscript)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"snapshot_consistent": False, "error": str(error)}, indent=2))
        return 1
    print(json.dumps(report, indent=2))
    if not report["snapshot_consistent"]:
        return 1
    if args.require_manuscript_match and report["manuscript_hash_matches"] is not True:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
