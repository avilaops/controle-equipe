"""Author, inspect and package Avila Ops plugins without changing source apps."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import tempfile
import unicodedata
from urllib.parse import unquote, urlsplit
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/"
EXCLUDED = {"__pycache__", "node_modules", ".git", ".venv", "venv"}
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


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def contained(root: Path, target: str) -> Path:
    require(isinstance(target, str) and target.startswith("./"), "Caminho do pacote deve iniciar com ./")
    path = (root / target).resolve()
    require(path.is_relative_to(root.resolve()) and ".." not in Path(target).parts, "Caminho escapa do pacote")
    require(path.exists(), "Recurso referenciado ausente")
    return path


def package_files(root: Path) -> list[Path]:
    files = []
    for path in sorted(root.rglob("*")):
        require(not path.is_symlink(), "Link simbolico nao permitido")
        if any(part in EXCLUDED for part in path.relative_to(root).parts):
            continue
        if path.is_file():
            require(path.name != ".env" and not (path.name.startswith(".env.") and not path.name.endswith(".example")), "Arquivo de ambiente privado")
            require(path.suffix.lower() not in {".pem", ".key", ".pfx", ".p12"}, "Credencial ou certificado no pacote")
            files.append(path)
    return files


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
        category = manifest.get("extensions", {}).get("com.openai", {}).get("interface", {}).get("category", "Productivity")
        entries.append({"name": manifest["name"], "source": {
            "source": "local", "path": "./" + path.parent.relative_to(ROOT).as_posix(),
        }, "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": category})
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
    files = package_files(path)
    manifest = json.loads((path / "plugin.json").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "schemas/plugin.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(manifest)
    require(manifest["$schema"] == SCHEMA + "plugin.schema.json", "Schema incorreto")
    valid_name(manifest["name"])
    require(path.name == manifest["name"], "Diretorio e nome divergentes")
    require(re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", manifest["version"]), "SemVer invalido")
    interface = manifest["extensions"]["com.openai"]["interface"]
    require(0 < len(interface["shortDescription"]) <= 30, "Subtitulo invalido")
    require(isinstance(interface["capabilities"], list), "Capacidades invalidas")
    require(not {"skills", "mcpServers", "apps", "interface"}.intersection(manifest), "Campo portatil em local incorreto")
    for key in ("logo", "composerIcon", "logoDark", "composerIconDark"):
        if key in interface:
            contained(path, interface[key])
    overlay = json.loads((path / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    for key in ("name", "version", "description", "author"):
        require(overlay[key] == manifest[key], f"Overlay divergente: {key}")
    require(overlay["interface"] == interface, "Apresentacao do overlay divergente")
    for key in ("skills", "mcpServers", "apps"):
        if key in overlay:
            contained(path, overlay[key])
    skills = list((path / "skills").glob("*/SKILL.md"))
    names = set()
    for skill in skills:
        content = skill.read_text(encoding="utf-8")
        require(skill.stat().st_size <= 1024 * 1024, "Skill excede 1 MiB")
        require(content.startswith("---\n"), "Frontmatter ausente")
        _, front, body = content.split("---", 2)
        data = yaml.safe_load(front)
        require(isinstance(data, dict), "Frontmatter invalido")
        for key in ("name", "description"):
            require(isinstance(data.get(key), str) and data[key].strip(), f"Campo ausente: {key}")
        valid_name(data["name"])
        require(data["name"] == skill.parent.name and data["name"] not in names, "Nome de skill divergente ou duplicado")
        names.add(data["name"])
        require(body.strip(), "Corpo da skill vazio")
        for ref in re.findall(r"\]\(([^)]+)\)", body):
            if "://" not in ref and not any(char in ref for char in "{}<>"):
                resolved = (skill.parent / ref).resolve()
                require(resolved.is_relative_to(path.resolve()) and resolved.is_file(), f"Referencia invalida: {ref}")
    has_mcp = (path / "mcp.json").exists()
    has_apps = "apps" in overlay
    if (path / "mcp.json").exists():
        mcp = json.loads((path / "mcp.json").read_text(encoding="utf-8"))
        require(mcp["$schema"] == SCHEMA + "mcp.schema.json", "Schema MCP incorreto")
        mcp_schema = json.loads((ROOT / "schemas/mcp.schema.json").read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(mcp_schema).validate(mcp)
        compatibility_path = path / ".mcp.json"
        if compatibility_path.exists():
            compatibility = json.loads(compatibility_path.read_text(encoding="utf-8"))
            compatibility_with_schema = {"$schema": SCHEMA + "mcp.schema.json", **compatibility}
            jsonschema.Draft202012Validator(mcp_schema).validate(compatibility_with_schema)
        require(isinstance(mcp["mcpServers"], dict) and mcp["mcpServers"], "MCP vazio")
        for server in mcp["mcpServers"].values():
            require(server["type"] in {"stdio", "streamable-http", "sse"}, "Transporte MCP invalido")
            if server["type"] == "stdio":
                require(server.get("command"), "Comando MCP ausente")
            else:
                url = urlsplit(server.get("url", ""))
                require(url.scheme == "https" and url.netloc and not url.username and not url.fragment, "URL MCP insegura")
    require(bool(skills) or has_mcp or has_apps, "Plugin sem componente utilizavel")
    for file in files:
        if file.suffix == ".json":
            json.loads(file.read_text(encoding="utf-8-sig"))
        elif file.suffix in {".yaml", ".yml"}:
            yaml.safe_load(file.read_text(encoding="utf-8-sig"))
        elif file.suffix == ".py":
            ast.parse(file.read_text(encoding="utf-8-sig"), filename=str(file))
        elif file.suffix == ".svg":
            ET.parse(file)


def validate_markdown_links(root: Path) -> None:
    """Require every local Markdown link in the repository to resolve."""
    for document in sorted(root.rglob("*.md")):
        if any(part in EXCLUDED or part == "dist" for part in document.relative_to(root).parts):
            continue
        content = document.read_text(encoding="utf-8-sig")
        for reference in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", content):
            target = unquote(reference.split("#", 1)[0].strip())
            if (not target or "://" in target or target.startswith(("mailto:", "#"))
                    or any(char in target for char in "{}<>")):
                continue
            resolved = (document.parent / target).resolve()
            require(resolved.is_relative_to(root.resolve()) and resolved.exists(),
                    f"Referencia Markdown invalida em {document.relative_to(root)}: {reference}")


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
    require({r["plugin"] for r in results} == {p["name"] for p in market["plugins"]}, "Marketplace divergente dos plugins")
    for entry in market["plugins"]:
        target = (ROOT / entry["source"]["path"]).resolve()
        require(target.is_relative_to(ROOT) and (target / "plugin.json").is_file(), "Origem invalida no marketplace")
    validate_markdown_links(ROOT)
    dump(ROOT / "reports/validacao.json", {"validation": "Estrutural local; nao comprova instalacao ou conexao.", "results": results})
    if not results or any(r["status"] == "failed" for r in results):
        raise ValueError("Validacao falhou; consulte reports/validacao.json")
    catalogue(results)
    return results


def catalogue(results: list[dict]) -> None:
    (ROOT / "docs").mkdir(parents=True, exist_ok=True)
    lines = [
        "# Catálogo compartilhado Ávila Ops", "",
        "Plugins disponíveis no marketplace oficial `avilaops-desenvolvimento`.", "",
        "| Plugin | Versão | Skills | MCP | Finalidade | Validação |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for result in results:
        root = ROOT / "plugins" / result["plugin"]
        manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
        skills = len(list((root / "skills").glob("*/SKILL.md")))
        mcp = "sim" if (root / "mcp.json").is_file() else "não"
        lines.append(
            f"| [{manifest['name']}](../plugins/{manifest['name']}/README.md) | "
            f"{manifest['version']} | {skills} | {mcp} | {manifest['description']} | {result['status']} |"
        )
    lines += ["", "Validação estrutural não substitui autenticação nem execução funcional no host.", ""]
    (ROOT / "docs/CATALOGO.md").write_text("\n".join(lines), encoding="utf-8")


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
        files = package_files(plugin)
        expected = {file.relative_to(plugin).as_posix(): hashlib.sha256(file.read_bytes()).hexdigest() for file in files}
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, strict_timestamps=False) as bundle:
            for file in files:
                bundle.write(file, file.relative_to(plugin))
        with zipfile.ZipFile(archive) as bundle:
            require(bundle.testzip() is None, "ZIP corrompido")
            require(set(bundle.namelist()) == set(expected), "Conteudo do ZIP divergente")
            for name, digest in expected.items():
                require(hashlib.sha256(bundle.read(name)).hexdigest() == digest, "Arquivo do ZIP diverge da fonte")
            with tempfile.TemporaryDirectory(prefix="avila-marketplace-") as temporary:
                staging = Path(temporary) / plugin.name
                staging.mkdir(parents=True)
                for member in bundle.namelist():
                    require((staging / member).resolve().is_relative_to(staging.resolve()), "Membro do ZIP escapa do destino")
                bundle.extractall(staging)
                validate(staging)
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
