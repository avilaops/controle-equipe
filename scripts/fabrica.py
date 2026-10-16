"""Author, inspect and package Avila Ops plugins without changing source apps."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
import zipfile
from pathlib import Path

import yaml
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/"
APPLICATIONS = {
    "arxisbim.com.br": "Plataforma BIM Arxis",
    "auth.avilaops.com": "Autenticacao compartilhada",
    "avilaops-site": "Site institucional Avila Ops",
    "CMS": "Plataforma de sites CMS",
    "crm.avilaops.com": "CRM e atendimento omnichannel",
    "engops.avilaops.com": "Operacao de demandas de engenharia",
    "ERP": "ERP comercial multiempresa",
    "extension-brave": "Extensao de navegador",
    "Gerador-3d": "Gerador parametrico 3D",
    "infra": "Infraestrutura compartilhada",
    "investigacao": "Ferramentas de investigacao autorizada",
    "lojas.avilaops.com": "Plataforma de lojas virtuais",
    "Ludusequipamentos-website": "Site Ludus Equipamentos",
    "mail.avilaops.com": "Servico de email",
    "mcp-unificado": "Integracao MCP local",
    "mcp.avilaops.com": "Gateway MCP Avila Ops",
    "mellotransportesriopreto.com.br": "Site Mello Transportes",
    "motor-web": "Regras de conteudo compartilhadas",
    "n8n.avilaops.com": "Modulos e automacoes n8n",
    "notas.avilaops.com": "Notas e documentacao",
    "painel-wifi": "Painel local de rede",
    "pentest": "Testes de seguranca autorizados",
    "saudepet.app.br": "Aplicacao Saude Pet",
    "Scrapper": "Catalogos de fornecedores",
    "sinapsemed": "Plataforma de estudo SinapseMed",
    "TMS": "Sistema de gestao de transportes",
    "notas-integracao": "Sincronizacao de notas Obsidian e n8n",
    "ferramentas": "Ferramentas locais do workspace",
    "tagflow": "Desenvolvimento local Tagflow",
}
EXTERNAL = {"chrome-devtools-mcp", "mcp-gsc", "onetool-mcp-2.2.2"}
ARTIFACTS = {
    "node_modules", ".claude", ".codex", "outputs", "test-results",
    "playwright-report", "Nova pasta", "2026-10-14", "previews-arxisbim",
    "sharp-libvips-1.3.4", "central-integracoes", "specs", "tests",
    "mcp-gsc-revalidate-20261015",
    "DOMIRIO", "GRB", "LLMS", "Ludus Equipamentos", "Notas",
}


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def valid_name(value: str) -> str:
    if len(value) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise ValueError("Use um nome kebab-case com ate 64 caracteres.")
    return value


def create(name: str, source: Path, description: str) -> Path:
    name = valid_name(name)
    if not description.strip():
        raise ValueError("A descricao nao pode estar vazia.")
    skill_name = valid_name(name[:52].rstrip("-") + "-desenvolver")
    source = source.resolve(strict=True)
    if not source.is_dir():
        raise ValueError("A origem deve ser um diretorio.")
    target = ROOT / "plugins" / name
    if target.exists():
        raise FileExistsError(f"Pacote preservado; ja existe: {target}")
    manifest = {
        "$schema": SCHEMA + "plugin.schema.json", "name": name,
        "version": "0.1.0", "description": description,
        "author": {"name": "Avila Ops"},
        "extensions": {"com.openai": {"interface": {
            "displayName": description, "shortDescription": "Desenvolvimento da aplicacao",
            "developerName": "Avila Ops", "capabilities": [],
        }}},
    }
    dump(target / "plugin.json", manifest)
    # Compatibility overlay mirrors inline settings, rather than inventing app IDs.
    dump(target / ".codex-plugin" / "plugin.json", {
        "name": name, "version": "0.1.0", "description": description,
        "author": {"name": "Avila Ops"}, "skills": "./skills/",
        "interface": manifest["extensions"]["com.openai"]["interface"],
    })
    skill = target / "skills" / skill_name
    skill.mkdir(parents=True)
    front = yaml.safe_dump({
        "name": skill_name,
        "description": f"Use para analisar, implementar e verificar alteracoes em {description}, quando o usuario indicar esta aplicacao.",
    }, allow_unicode=True, sort_keys=False).strip()
    (skill / "SKILL.md").write_text(
        f"---\n{front}\n---\n\n# {description}\n\n"
        "1. Leia [o contexto da aplicacao](references/aplicacao.md). Localize o checkout; "
        "se nao estiver acessivel, solicite sua localizacao.\n"
        "2. Leia AGENTS.md na raiz e nos diretorios afetados, README e os manifestos reais. "
        "Confira git status e preserve alteracoes existentes.\n"
        "3. Localize os simbolos envolvidos, consumidores, configuracoes e testes. "
        "Derive os comandos dos arquivos do projeto; nao suponha framework ou gerenciador.\n"
        "4. Implemente apenas o escopo pedido seguindo as convencoes locais. "
        "Verifique identidade e empresa/tenant antes de qualquer operacao com dados.\n"
        "5. Execute as verificacoes pertinentes e examine o diff. Para mudancas visuais, "
        "verifique os fluxos afetados no navegador quando disponivel.\n"
        "6. Informe arquivos alterados, resultado das verificacoes e limitacoes. "
        "Diferencie implementacao local, publicacao e validacao em producao.\n\n"
        "## Acesso a ferramentas\n\n"
        "Este pacote fornece um fluxo de desenvolvimento com acesso ao checkout. "
        "Nao declara ferramentas de negocio nem conexao MCP. Descubra as ferramentas "
        "realmente disponiveis antes de usa-las. Nunca invente nomes, endpoints, "
        "identificadores de apps ou provas de acesso. Nunca copie segredos para o pacote.\n",
        encoding="utf-8",
    )
    (skill / "references").mkdir()
    (skill / "references" / "aplicacao.md").write_text(
        f"# Contexto local\n\n- Aplicacao: {description}.\n- Checkout observado: `{source.as_posix()}`.\n"
        "- O caminho e uma referencia desta maquina; em outro host, localize o checkout equivalente.\n"
        "- Estado do pacote: fluxo de desenvolvimento local; operacoes de negocio nao implementadas.\n"
        "- Consulte a documentacao atual na origem. Este pacote nao replica seu codigo nem suas credenciais.\n",
        encoding="utf-8",
    )
    (target / "README.md").write_text(
        f"# {description}\n\nPlugin `{name}` com uma skill de desenvolvimento local.\n\n"
        "Para criar workflows de negocio, adicione skills focadas em `skills/<nome>/SKILL.md`, "
        "com entradas, passos, saida e verificacao especificos. Siga `docs/AUTORIA.md` na fabrica.\n\n"
        "Nao instalado nem conectado automaticamente. Este pacote nao concede acesso ao sistema.\n",
        encoding="utf-8",
    )
    return target


def marketplace() -> None:
    entries = []
    for path in sorted((ROOT / "plugins").glob("*/plugin.json")):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        entries.append({"name": manifest["name"], "source": {
            "source": "local", "path": "./" + path.parent.relative_to(ROOT).as_posix(),
        }, "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Productivity"})
    dump(ROOT / ".agents/plugins/marketplace.json", {
        "name": "avilaops-desenvolvimento", "interface": {"displayName": "Avila Ops - Desenvolvimento"},
        "plugins": entries,
    })


def inventory(workspace: Path) -> None:
    records = []
    for source in sorted(workspace.iterdir()):
        if not source.is_dir():
            continue
        name = source.name
        category = ("aplicacao" if name in APPLICATIONS else "terceiro" if name in EXTERNAL
                    else "artefato-ou-suporte" if name in ARTIFACTS else "classificacao-pendente")
        plugin = "avila-" + slug(name) if category == "aplicacao" else None
        records.append({"directory": str(source), "category": category, "plugin": plugin,
                        "evidence": [file for file in ("README.md", "package.json", "Cargo.toml", "AGENTS.md", "pyproject.toml")
                                     if (source / file).is_file()]})
        if plugin and not (ROOT / "plugins" / plugin).exists():
            create(plugin, source, APPLICATIONS[name])
    dump(ROOT / "catalogo/aplicacoes.json", {"workspace": str(workspace),
        "scope": "Diretorios imediatos do workspace; subaplicacoes devem ser cadastradas com create.",
        "records": records})
    marketplace()


def validate(path: Path) -> None:
    if path.is_symlink() or any(p.is_symlink() for p in path.rglob("*")):
        raise ValueError("Links simbolicos nao sao permitidos no pacote.")
    manifest = json.loads((path / "plugin.json").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "schemas/plugin.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(manifest)
    assert manifest["$schema"] == SCHEMA + "plugin.schema.json", "Schema incorreto"
    valid_name(manifest["name"])
    assert path.name == manifest["name"], "Diretorio e nome divergentes"
    assert re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", manifest["version"]), "SemVer invalido"
    interface = manifest["extensions"]["com.openai"]["interface"]
    assert 0 < len(interface["shortDescription"]) <= 30, "Subtitulo invalido"
    assert isinstance(interface["capabilities"], list)
    assert not {"skills", "mcpServers", "apps", "interface"}.intersection(manifest)
    overlay = json.loads((path / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    for key in ("name", "version", "description", "author"):
        assert overlay[key] == manifest[key], f"Overlay divergente: {key}"
    assert overlay["interface"] == interface
    skills = list((path / "skills").glob("*/SKILL.md"))
    assert skills, "Nenhuma skill utilizavel"
    names = set()
    for skill in skills:
        content = skill.read_text(encoding="utf-8")
        assert skill.stat().st_size <= 1024 * 1024
        assert content.startswith("---\n"), "Frontmatter ausente"
        _, front, body = content.split("---", 2)
        data = yaml.safe_load(front)
        assert isinstance(data, dict)
        for key in ("name", "description"):
            assert isinstance(data.get(key), str) and data[key].strip()
        valid_name(data["name"])
        assert data["name"] == skill.parent.name and data["name"] not in names
        names.add(data["name"])
        assert body.strip()
        for ref in re.findall(r"\]\(([^)]+)\)", body):
            if "://" not in ref:
                resolved = (skill.parent / ref).resolve()
                assert resolved.is_relative_to(path.resolve()) and resolved.is_file(), f"Referencia invalida: {ref}"
    for file in path.rglob("*"):
        assert file.name not in {".env", "node_modules", "__pycache__"}, f"Arquivo proibido: {file}"
        assert file.suffix.lower() not in {".pem", ".key", ".pfx", ".p12"}, f"Chave privada: {file}"
    if (path / "mcp.json").exists():
        mcp = json.loads((path / "mcp.json").read_text(encoding="utf-8"))
        assert mcp["$schema"] == SCHEMA + "mcp.schema.json"
        assert isinstance(mcp["mcpServers"], dict) and mcp["mcpServers"]
        for server in mcp["mcpServers"].values():
            assert server["type"] in {"stdio", "streamable-http", "sse"}
            if server["type"] == "stdio":
                assert server.get("command")
            else:
                assert server.get("url", "").startswith("https://")


def check_all() -> list[dict]:
    results = []
    for path in sorted((ROOT / "plugins").iterdir()):
        if path.is_dir():
            try:
                validate(path)
                results.append({"plugin": path.name, "status": "passed"})
            except (AssertionError, ValueError, KeyError, OSError, jsonschema.ValidationError) as error:
                results.append({"plugin": path.name, "status": "failed", "error": str(error)})
    market = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    assert {r["plugin"] for r in results} == {p["name"] for p in market["plugins"]}
    for entry in market["plugins"]:
        target = (ROOT / entry["source"]["path"]).resolve()
        assert target.is_relative_to(ROOT) and (target / "plugin.json").is_file()
    dump(ROOT / "reports/validacao.json", {"validation": "Estrutural local; nao comprova instalacao ou conexao.", "results": results})
    if not results or any(r["status"] == "failed" for r in results):
        raise ValueError("Validacao falhou; consulte reports/validacao.json")
    return results


def package() -> None:
    check_all()
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    hashes = {}
    for plugin in sorted((ROOT / "plugins").iterdir()):
        if not plugin.is_dir():
            continue
        manifest = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))
        archive = output / f"{plugin.name}-{manifest['version']}.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
            for file in sorted(plugin.rglob("*")):
                if file.is_file():
                    bundle.write(file, file.relative_to(plugin))
        with zipfile.ZipFile(archive) as bundle:
            assert bundle.testzip() is None
            assert "plugin.json" in bundle.namelist()
        hashes[archive.name] = hashlib.sha256(archive.read_bytes()).hexdigest()
    dump(output / "sha256.json", hashes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    scan = commands.add_parser("inventory")
    scan.add_argument("workspace", type=Path)
    new = commands.add_parser("create")
    new.add_argument("name")
    new.add_argument("--source", required=True, type=Path)
    new.add_argument("--description", required=True)
    commands.add_parser("validate")
    commands.add_parser("package")
    args = parser.parse_args()
    if args.command == "inventory":
        inventory(args.workspace.resolve(strict=True))
    elif args.command == "create":
        create(args.name, args.source, args.description)
        marketplace()
    elif args.command == "validate":
        print(f"{len(check_all())} plugins validados")
    else:
        package()


if __name__ == "__main__":
    main()
