"""Controle local de equipes e consolidacao dos registros dos repositorios."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil

import fabrica

ROOT = Path(__file__).resolve().parents[1]
STATES = {"a-fazer", "em-andamento", "em-revisao", "bloqueada", "concluida"}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def applications():
    catalog = json.loads((ROOT / "catalogo/aplicacoes.json").read_text(encoding="utf-8"))
    return {r["plugin"]: Path(r["directory"]) for r in catalog["records"]
            if r["category"] == "aplicacao"}


def validate(data):
    if data.get("schemaVersion") != 1:
        raise ValueError("Versao do registro desconhecida")
    fabrica.valid_name(data["application"])
    for collection in ("members", "tasks", "decisions", "integrations"):
        if not isinstance(data.get(collection), list):
            raise ValueError(f"Colecao invalida: {collection}")
        ids = [row["id"] for row in data[collection]]
        if len(ids) != len(set(ids)):
            raise ValueError(f"IDs duplicados: {collection}")
    members = {m["id"] for m in data["members"]}
    for member in data["members"]:
        if not member.get("name", "").strip() or not member.get("role", "").strip():
            raise ValueError("Membro exige nome e papel")
    for task in data["tasks"]:
        owner = task["owner"]
        if task["status"] not in STATES or (owner is not None and owner not in members):
            raise ValueError("Estado ou responsavel invalido")
        if not task.get("title", "").strip() or not task.get("acceptance", "").strip():
            raise ValueError("Tarefa exige titulo e criterio de aceite")
        if task["status"] == "concluida" and not task.get("evidence", "").strip():
            raise ValueError("Conclusao exige evidencia")
        if task["status"] == "bloqueada" and not task.get("blocker", "").strip():
            raise ValueError("Bloqueio exige motivo")
        if not isinstance(task.get("history"), list):
            raise ValueError("Historico de tarefa ausente")
    for decision in data["decisions"]:
        if not all(str(decision.get(k, "")).strip() for k in ("summary", "reason", "evidence")):
            raise ValueError("Decisao exige resumo, motivo e evidencia")
    for integration in data["integrations"]:
        if not all(str(integration.get(k, "")).strip() for k in ("name", "environment", "identity", "evidence")):
            raise ValueError("Integracao exige nome, ambiente, identidade e evidencia")


def read(app):
    paths = applications()
    if app not in paths:
        raise ValueError(f"Aplicacao fora do catalogo: {app}")
    path = paths[app] / ".agents/equipe/controle.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    validate(data)
    if data["application"] != app:
        raise ValueError("Identidade do registro diverge do catalogo")
    return path, data


@contextmanager
def lock(path):
    lockfile = path.with_suffix(".lock")
    descriptor = os.open(lockfile, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        os.close(descriptor)
        yield
    finally:
        lockfile.unlink()


def save(path, data):
    validate(data)
    temporary = path.with_suffix(".json.tmp")
    try:
        temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def next_id(rows, prefix):
    numbers = [int(row["id"].split("-")[-1]) for row in rows
               if re.fullmatch(prefix + r"-\d+", row["id"])]
    return f"{prefix}-{max(numbers, default=0) + 1:04d}"


def mutate(args):
    path, _ = read(args.app)
    with lock(path):
        _, data = read(args.app)
        if args.command == "membro":
            fabrica.valid_name(args.id)
            if any(m["id"] == args.id for m in data["members"]):
                raise ValueError("Membro ja cadastrado; revise o registro existente")
            data["members"].append({"id": args.id, "name": args.nome, "role": args.papel})
        elif args.command == "tarefa":
            data["tasks"].append({
                "id": next_id(data["tasks"], "T"), "title": args.titulo,
                "owner": args.responsavel, "acceptance": args.aceite,
                "priority": args.prioridade, "status": "a-fazer",
                "evidence": "", "blocker": "", "createdAt": now(),
                "history": [{"at": now(), "status": "a-fazer", "note": "Tarefa cadastrada"}],
            })
        elif args.command == "estado":
            task = next((t for t in data["tasks"] if t["id"] == args.id), None)
            if task is None:
                raise ValueError("Tarefa nao encontrada")
            if args.status == "concluida" and not args.evidencia:
                raise ValueError("Informe --evidencia para concluir")
            if args.status == "bloqueada" and not args.motivo:
                raise ValueError("Informe --motivo para bloquear")
            task.update(status=args.status, blocker=args.motivo if args.status == "bloqueada" else "")
            if args.evidencia:
                task["evidence"] = args.evidencia
            task["history"].append({"at": now(), "status": args.status,
                                    "note": args.motivo or "Estado atualizado", "evidence": args.evidencia or ""})
        elif args.command == "decisao":
            data["decisions"].append({"id": next_id(data["decisions"], "D"), "at": now(),
                "summary": args.resumo, "reason": args.motivo, "evidence": args.evidencia})
        elif args.command == "integracao":
            data["integrations"].append({"id": next_id(data["integrations"], "I"), "at": now(),
                "name": args.nome, "environment": args.ambiente, "identity": args.identidade,
                "evidence": args.evidencia})
        save(path, data)
    print(f"Registro atualizado: {args.app}")


def panel():
    publication = json.loads((ROOT / "reports/publicacao-git.json").read_text(encoding="utf-8"))
    destinations = {row["application"]: row.get("url") or row.get("centralPath") for row in publication}
    snapshot_path = ROOT / "reports/equipes.json"
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8")) if snapshot_path.is_file() else {"applications": []}
    previous = {row["application"]: row for row in snapshot.get("applications", [])}
    rows = []
    lines = ["# Controle da equipe por aplicacao", "", f"Gerado em {now()}.", "",
             "Retrato dos registros locais. Nao comprova deploy, sincronizacao Git ou atividade em tempo real.", "",
             "| Aplicacao | Membros | Tarefas | Bloqueadas | Concluidas |", "| --- | ---: | ---: | ---: | ---: |"]
    for app in applications():
        try:
            _, data = read(app)
        except (FileNotFoundError, ValueError):
            prior = previous.get(app)
            if prior is None:
                raise
            data = {
                "members": [None] * prior["members"],
                "tasks": ([{"status": "bloqueada"}] * prior["blocked"]
                          + [{"status": "concluida"}] * prior["completed"]
                          + [{"status": "a-fazer"}] * (prior["tasks"] - prior["blocked"] - prior["completed"])),
            }
        destination = destinations.get(app, "")
        row = {"application": app, "source": destination, "members": len(data["members"]),
               "tasks": len(data["tasks"]), "blocked": sum(t["status"] == "bloqueada" for t in data["tasks"]),
               "completed": sum(t["status"] == "concluida" for t in data["tasks"]),
               "registration": "sem membros cadastrados" if not data["members"] else "equipe cadastrada"}
        rows.append(row)
        label = f"[{app}]({destination})" if destination else app
        lines.append(f"| {label} | {row['members']} | {row['tasks']} | {row['blocked']} | {row['completed']} |")
    fabrica.dump(ROOT / "reports/equipes.json", {"generatedAt": now(), "applications": rows})
    (ROOT / "PAINEL-EQUIPE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} registros de equipe validados")


def export():
    for app, source in applications().items():
        read(app)
        name = app + "-equipe"
        origin = source / ".agents/skills" / name
        target = ROOT / "plugins" / app / "skills" / name
        if not (origin / "SKILL.md").is_file():
            raise ValueError(f"Skill local ausente: {app}")
        target.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origin / "SKILL.md", target / "SKILL.md")
        for file in (ROOT / "plugins" / app / "plugin.json", ROOT / "plugins" / app / ".codex-plugin/plugin.json"):
            data = json.loads(file.read_text(encoding="utf-8"))
            # This is the first team release. Later release bumps remain an authoring decision.
            if data["version"] == "0.1.0":
                data["version"] = "0.2.0"
            fabrica.dump(file, data)
    fabrica.check_all()
    print("Skills de equipe exportadas da origem dos repositorios")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("membro", "tarefa", "estado", "decisao", "integracao"):
        command = commands.add_parser(name)
        command.add_argument("app")
        if name in ("membro", "estado"):
            command.add_argument("--id", required=True)
        if name == "membro":
            command.add_argument("--nome", required=True)
            command.add_argument("--papel", required=True)
        elif name == "tarefa":
            command.add_argument("--titulo", required=True)
            command.add_argument("--responsavel", required=True)
            command.add_argument("--aceite", required=True)
            command.add_argument("--prioridade", choices=["baixa", "normal", "alta", "urgente"], default="normal")
        elif name == "estado":
            command.add_argument("--status", required=True, choices=sorted(STATES))
            command.add_argument("--evidencia")
            command.add_argument("--motivo")
        elif name == "decisao":
            command.add_argument("--resumo", required=True)
            command.add_argument("--motivo", required=True)
            command.add_argument("--evidencia", required=True)
        else:
            command.add_argument("--nome", required=True)
            command.add_argument("--ambiente", required=True)
            command.add_argument("--identidade", required=True)
            command.add_argument("--evidencia", required=True)
    commands.add_parser("painel")
    commands.add_parser("exportar")
    args = parser.parse_args()
    if args.command == "painel":
        panel()
    elif args.command == "exportar":
        export()
    else:
        mutate(args)


if __name__ == "__main__":
    main()
