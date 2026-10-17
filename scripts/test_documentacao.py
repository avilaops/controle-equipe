"""Validate repository-local Markdown links."""

from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


class DocumentationTests(unittest.TestCase):
    def test_local_links_exist(self):
        broken = []
        for path in ROOT.rglob("*.md"):
            if any(part in {".git", "dist", ".venv", "node_modules"} for part in path.parts):
                continue
            text = path.read_text(encoding="utf-8-sig")
            for raw in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", text):
                target = unquote(raw.split("#", 1)[0])
                if not target or urlsplit(target).scheme or target.startswith("/") or any(char in target for char in "{}<>"):
                    continue
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    broken.append(f"{path.relative_to(ROOT).as_posix()} -> {target}")
        self.assertEqual([], broken, "Links locais quebrados:\n" + "\n".join(broken))


if __name__ == "__main__":
    unittest.main()
