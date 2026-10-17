"""Import the reviewed operational catalog into the shared marketplace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path(r"D:\Projetos\Plugins")
RENAMES = {
    "avila-cms": "avila-cms-operacoes",
    "avila-tms": "avila-tms-operacoes",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_tree(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def rename_identity(target: Path, name: str) -> None:
    for relative in ("plugin.json", ".codex-plugin/plugin.json"):
        path = target / relative
        data = load(path)
        data["name"] = name
        if name in RENAMES.values():
            data["version"] = "1.0.0"
        dump(path, data)


def import_plugins(source: Path) -> list[str]:
    imported = []
    for plugin in sorted((source / "plugins").iterdir()):
        if not plugin.is_dir():
            continue
        name = RENAMES.get(plugin.name, plugin.name)
        target = ROOT / "plugins" / name
        if target.exists() and plugin.name not in RENAMES:
            raise FileExistsError(f"Plugin identity already exists: {name}")
        copy_tree(plugin, target)
        rename_identity(target, name)
        imported.append(name)
    return imported


def import_standalone_skills(source: Path) -> str:
    name = "avila-skills"
    target = ROOT / "plugins" / name
    target.mkdir(parents=True, exist_ok=True)
    skills = target / "skills"
    if skills.exists():
        shutil.rmtree(skills)
    skills.mkdir()
    for skill in sorted((source / "skills").iterdir()):
        if skill.is_dir():
            copy_tree(skill, skills / skill.name)

    icon_source = source / "plugins" / "avila-ops-skills" / "assets" / "plugin-icon.svg"
    assets = target / "assets"
    assets.mkdir(exist_ok=True)
    shutil.copyfile(icon_source, assets / "plugin-icon.svg")
    interface = {
        "displayName": "Ávila Skills",
        "shortDescription": "Biblioteca de workflows",
        "longDescription": "Biblioteca compartilhada de skills especializadas para desenvolvimento, integração, design, conteúdo e operações.",
        "developerName": "Ávila Ops",
        "category": "Developer Tools",
        "capabilities": [],
        "defaultPrompt": "Liste as skills Ávila disponíveis e escolha somente a adequada para a tarefa solicitada.",
        "logo": "./assets/plugin-icon.svg",
        "composerIcon": "./assets/plugin-icon.svg",
    }
    manifest = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": name,
        "version": "1.0.0",
        "description": "Biblioteca compartilhada de workflows especializados da Ávila Ops.",
        "author": {"name": "Ávila Ops"},
        "extensions": {"com.openai": {"interface": interface}},
    }
    dump(target / "plugin.json", manifest)
    dump(target / ".codex-plugin/plugin.json", {
        "name": name,
        "version": "1.0.0",
        "description": manifest["description"],
        "author": manifest["author"],
        "skills": "./skills/",
        "interface": interface,
    })
    (target / "README.md").write_text(
        "# Ávila Skills\n\nPlugin que distribui 20 workflows especializados revisados. "
        "As skills são carregadas sob demanda conforme a descrição de cada `SKILL.md`.\n\n"
        "Não contém credenciais nem concede acesso a sistemas. Operações externas dependem "
        "das ferramentas e permissões disponíveis no host.\n",
        encoding="utf-8",
    )
    return name


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()
    source = args.source.resolve(strict=True)
    if not (source / "plugins").is_dir() or not (source / "skills").is_dir():
        raise ValueError("Source does not contain the reviewed plugins and skills catalogs")
    imported = import_plugins(source)
    imported.append(import_standalone_skills(source))
    print(json.dumps({"imported": imported, "count": len(imported)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
