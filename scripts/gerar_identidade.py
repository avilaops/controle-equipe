"""Add deterministic Avila Ops icons to plugins that do not have one."""

from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACCENTS = ("#38BDF8", "#2DD4BF", "#A78BFA", "#F59E0B", "#FB7185")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def initials(name: str) -> str:
    ignored = {"avila", "com", "br"}
    words = [word for word in name.split("-") if word not in ignored]
    return "".join(word[0] for word in words[:2]).upper() or "AO"


def add_icon(plugin: Path) -> None:
    icon = plugin / "assets/plugin-icon.svg"
    if not icon.is_file():
        accent = ACCENTS[int(hashlib.sha256(plugin.name.encode()).hexdigest()[:2], 16) % len(ACCENTS)]
        label = initials(plugin.name)
        icon.parent.mkdir(parents=True, exist_ok=True)
        icon.write_text(
            f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" role="img" aria-labelledby="title">
  <title id="title">{html.escape(plugin.name)}</title>
  <rect width="256" height="256" rx="52" fill="#10243A"/>
  <path d="M48 174 94 70h68l46 104h-38l-9-23H95l-9 23H48Zm59-55h42l-21-52-21 52Z" fill="#F8FAFC"/>
  <circle cx="194" cy="62" r="22" fill="{accent}"/>
  <text x="128" y="218" text-anchor="middle" font-family="Arial,sans-serif" font-size="25" font-weight="700" fill="{accent}">{label}</text>
</svg>''',
            encoding="utf-8",
        )
    manifest_path = plugin / "plugin.json"
    overlay_path = plugin / ".codex-plugin/plugin.json"
    manifest = load(manifest_path)
    interface = manifest["extensions"]["com.openai"]["interface"]
    interface["logo"] = "./assets/plugin-icon.svg"
    interface["composerIcon"] = "./assets/plugin-icon.svg"
    dump(manifest_path, manifest)
    overlay = load(overlay_path)
    overlay["interface"] = interface
    dump(overlay_path, overlay)


def gallery(plugins: list[Path]) -> None:
    cards = []
    for plugin in plugins:
        manifest = load(plugin / "plugin.json")
        display = manifest["extensions"]["com.openai"]["interface"].get("displayName", plugin.name)
        cards.append(
            f'<a class="card" href="../plugins/{plugin.name}/README.md">'
            f'<img src="../plugins/{plugin.name}/assets/plugin-icon.svg" alt="">'
            f'<strong>{html.escape(display)}</strong><small>{plugin.name}</small></a>'
        )
    document = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Plugins Ávila Ops</title><style>
body{{margin:0;background:#071421;color:#f8fafc;font:16px system-ui,sans-serif}}main{{max-width:1180px;margin:auto;padding:48px 24px}}h1{{font-size:clamp(32px,5vw,58px);margin:0 0 12px}}p{{color:#a9bdd0;margin:0 0 36px}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:18px}}.card{{background:#10243a;border:1px solid #25425e;border-radius:20px;padding:22px;color:inherit;text-decoration:none;display:grid;gap:10px;transition:.15s}}.card:hover{{transform:translateY(-3px);border-color:#38bdf8}}img{{width:82px;height:82px}}strong{{font-size:17px}}small{{color:#8fa9bf;overflow-wrap:anywhere}}</style></head><body><main><h1>Marketplace Ávila Ops</h1><p>{len(plugins)} plugins privados para desenvolvimento e operações.</p><section class="grid">{''.join(cards)}</section></main></body></html>'''
    (ROOT / "docs/GALERIA.html").write_text(document, encoding="utf-8")


def main() -> None:
    plugins = sorted(path for path in (ROOT / "plugins").iterdir() if path.is_dir())
    for plugin in plugins:
        add_icon(plugin)
    gallery(plugins)
    print(f"{len(plugins)} identidades verificadas")


if __name__ == "__main__":
    main()
