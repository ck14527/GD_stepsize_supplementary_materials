#!/usr/bin/env python3
"""Audit a Lean-produced declaration export against the source and paper targets.

Run GD/Audit.lean after lake build GD to obtain the current export. This Python
check rejects unsupported theorem axioms and verifies exact registered targets;
it is complementary to the Lean build, not a replacement for kernel checking.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from check_snapshot import source_theorems

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def check(path: Path) -> dict:
    rows = json.loads(path.read_text(encoding="utf-8"))
    by_name = {row["name"]: row for row in rows}
    errors = []
    if len(by_name) != len(rows):
        errors.append("Duplicate declaration names")
    named = source_theorems(ROOT)
    if not named:
        errors.append("No source theorems found")
    for name in named:
        if by_name.get(name, {}).get("kind") != "theorem":
            errors.append("Source theorem missing from compiled export: " + name)
    unsupported = sorted({axiom for row in rows if row["kind"] == "theorem"
                          for axiom in row["axioms"]} - ALLOWED_AXIOMS)
    if unsupported:
        errors.append({"unsupported_theorem_axioms": unsupported})
    closure, todo = set(), list(named)
    while todo:
        name = todo.pop()
        if name in closure:
            continue
        closure.add(name)
        row = by_name.get(name)
        if row:
            todo.extend(row["proof_references"] + row["type_references"])
    unsafe = sorted(name for name in closure if name in by_name
                    and by_name[name]["safety"] in {"unsafe", "partial"})
    project_axioms = sorted(name for name in closure if name in by_name
                            and by_name[name]["kind"] == "axiom")
    if unsafe:
        errors.append({"unsafe_or_partial_in_theorem_closure": unsafe})
    if project_axioms:
        errors.append({"project_axioms_in_theorem_closure": project_axioms})
    registry = json.loads((ROOT / "docs/statement_inventory.json").read_text(encoding="utf-8"))
    statements = [node for node in registry["nodes"]
                  if node["kind"] in {"Theorem", "Lemma", "Proposition", "Corollary"}]
    if len(statements) != 40:
        errors.append("Expected all 40 registered paper statements")
    verified_targets = 0
    for statement in statements:
        target = statement["target_definition"]
        proofs = statement["proof_declarations"]
        valid = bool(proofs) and by_name.get(target, {}).get("kind") == "definition"
        for name in proofs:
            row = by_name.get(name, {})
            valid = valid and name in named and row.get("kind") == "theorem" and row.get("exact_type_constant") == target
        if valid:
            verified_targets += 1
        else:
            errors.append("Compiled proof has a missing or different registered target: " + statement["id"])
    return {
        "check": "axioms and exact paper targets in a Lean-produced elaborated export",
        "declaration_export_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "named_source_theorems": len(named),
        "exported_declarations": len(rows),
        "registered_scalar_results": len(statements),
        "verified_registered_targets": verified_targets,
        "allowed_theorem_axioms": sorted(ALLOWED_AXIOMS),
        "unsupported_theorem_axioms": unsupported,
        "unsafe_or_partial_in_theorem_closure": unsafe,
        "project_axioms_in_theorem_closure": project_axioms,
        "errors": errors,
        "passed": not errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--declarations", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = check(args.declarations)
    except (OSError, ValueError, KeyError, TypeError) as error:
        report = {"passed": False, "error": str(error)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
