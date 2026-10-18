"""Normaliza registros legados para o contrato central de controle da equipe."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import equipe


MIGRATION_DATE = "2026-10-18"
STATUS_ALIASES = {
    "in_progress": "em-andamento",
    "in-review": "em-revisao",
    "in_review": "em-revisao",
    "em_revisao": "em-revisao",
    "completed": "concluida",
    "done": "concluida",
    "blocked": "bloqueada",
    "todo": "a-fazer",
}


def as_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "\n".join(filter(None, (as_text(item) for item in value)))
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value).strip()


def normalize(data: dict) -> dict:
    normalized = copy.deepcopy(data)
    member_ids = {member["id"] for member in normalized["members"]}

    for task in normalized["tasks"]:
        task["status"] = STATUS_ALIASES.get(task["status"], task["status"])
        owner = task.get("owner", task.get("assignee"))
        if isinstance(owner, str) and owner in member_ids:
            task["owner"] = owner
        else:
            if task.get("owner") is not None:
                task.setdefault("legacyOwner", copy.deepcopy(task["owner"]))
            task["owner"] = None
        task["acceptance"] = as_text(
            task.get("acceptance") or task.get("acceptanceCriteria") or task.get("objective")
        )
        task["evidence"] = as_text(task.get("evidence"))
        task["blocker"] = as_text(task.get("blocker"))
        task.setdefault("history", [{
            "at": MIGRATION_DATE,
            "status": task["status"],
            "note": "Registro legado normalizado para o contrato central.",
        }])

    for decision in normalized["decisions"]:
        decision["summary"] = as_text(
            decision.get("summary") or decision.get("title") or decision.get("decision")
        )
        decision["reason"] = as_text(decision.get("reason") or decision.get("decision"))
        decision["evidence"] = as_text(decision.get("evidence"))
        if not decision["evidence"]:
            if decision.get("date"):
                decision["evidence"] = f"Data registrada: {decision['date']}"
            elif decision.get("status"):
                decision["evidence"] = f"Estado registrado: {decision['status']}"
            else:
                decision["evidence"] = f"Registro legado normalizado em {MIGRATION_DATE}."

    for integration in normalized["integrations"]:
        integration["name"] = as_text(
            integration.get("name") or integration.get("system") or integration["id"]
        )
        integration["environment"] = as_text(
            integration.get("environment")
            or "Ambiente não informado no registro original"
        )
        integration["identity"] = as_text(
            integration.get("identity")
            or "Identidade não informada no registro original"
        )
        integration["evidence"] = as_text(
            integration.get("evidence") or integration.get("contract")
            or f"Registro legado normalizado em {MIGRATION_DATE}."
        )

    equipe.validate(normalized)
    return normalized


def migrate(path: Path) -> None:
    with equipe.lock(path):
        data = json.loads(path.read_text(encoding="utf-8"))
        equipe.save(path, normalize(data))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    for path in args.paths:
        migrate(path)
        print(f"Registro normalizado: {path}")


if __name__ == "__main__":
    main()
