"""Regression tests for authoring boundaries and portable package validation."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import fabrica


class FactoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "app"
        self.source.mkdir()
        (self.root / "schemas").mkdir()
        shutil.copy(fabrica.ROOT / "schemas/plugin.schema.json", self.root / "schemas")
        shutil.copy(fabrica.ROOT / "schemas/mcp.schema.json", self.root / "schemas")
        self.override = patch.object(fabrica, "ROOT", self.root)
        self.override.start()
        self.addCleanup(self.override.stop)

    def create(self, name="avila-teste"):
        return fabrica.create(name, self.source, "Aplicacao de teste")

    def test_roundtrip_and_archive_root(self):
        plugin = self.create()
        fabrica.marketplace()
        fabrica.validate(plugin)
        fabrica.package()
        archives = list((self.root / "dist").glob("*.zip"))
        self.assertEqual(len(archives), 1)
        with fabrica.zipfile.ZipFile(archives[0]) as archive:
            self.assertIn("plugin.json", archive.namelist())
            self.assertFalse(any(name.startswith("plugins/") for name in archive.namelist()))

    def test_packaging_removes_stale_plugin_versions(self):
        self.create()
        fabrica.marketplace()
        stale = self.root / "dist/avila-teste-0.0.1.zip"
        stale.parent.mkdir()
        stale.write_bytes(b"stale")
        fabrica.package()
        self.assertFalse(stale.exists())
        self.assertTrue((self.root / "dist/avila-teste-0.1.0.zip").is_file())

    def test_existing_package_preserved(self):
        plugin = self.create()
        before = (plugin / "plugin.json").read_bytes()
        with self.assertRaises(FileExistsError):
            self.create()
        self.assertEqual(before, (plugin / "plugin.json").read_bytes())

    def test_path_traversal_and_blank_description(self):
        with self.assertRaises(ValueError):
            self.create("../escape")
        with self.assertRaises(ValueError):
            fabrica.create("avila-empty", self.source, " ")
        self.assertFalse((self.root / "plugins/avila-empty").exists())

    def test_secret_file_blocks_packaging(self):
        plugin = self.create()
        (plugin / ".env").write_text("TEST_ONLY=1", encoding="utf-8")
        with self.assertRaises(ValueError):
            fabrica.validate(plugin)

    def test_missing_reference_and_overlay_drift(self):
        plugin = self.create()
        reference = next(plugin.glob("skills/*/references/aplicacao.md"))
        reference.unlink()
        with self.assertRaises(ValueError):
            fabrica.validate(plugin)
        reference.write_text("Contexto", encoding="utf-8")
        overlay_path = plugin / ".codex-plugin/plugin.json"
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
        overlay["version"] = "9.0.0"
        fabrica.dump(overlay_path, overlay)
        with self.assertRaises(ValueError):
            fabrica.validate(plugin)

    def test_maximum_plugin_name(self):
        fabrica.validate(self.create("a" * 64))

    def test_validation_remains_active_under_optimized_python(self):
        plugin = self.create()
        (plugin / ".env").write_text("SECRET=test", encoding="utf-8")
        with self.assertRaises(ValueError):
            fabrica.validate(plugin)

    def test_mcp_rejects_client_extensions_unsupported_by_codex(self):
        plugin = self.create()
        config = {
            "$schema": fabrica.SCHEMA + "mcp.schema.json",
            "mcpServers": {
                "teste": {
                    "type": "streamable-http",
                    "url": "https://example.com/mcp",
                    "extensions": {"com.openai": {"auth": {"type": "api_key"}}},
                }
            },
        }
        fabrica.dump(plugin / "mcp.json", config)
        with self.assertRaises(fabrica.jsonschema.ValidationError):
            fabrica.validate(plugin)

    def test_archive_matches_validated_source(self):
        plugin = self.create()
        fabrica.marketplace()
        fabrica.package()
        archive = next((self.root / "dist").glob("*.zip"))
        with fabrica.zipfile.ZipFile(archive) as bundle:
            member = "plugin.json"
            self.assertEqual(
                fabrica.hashlib.sha256(bundle.read(member)).hexdigest(),
                fabrica.hashlib.sha256((plugin / member).read_bytes()).hexdigest(),
            )

    def test_marketplace_rejects_duplicate_mcp_server_names(self):
        first = self.create("avila-primeiro")
        second = self.create("avila-segundo")
        for plugin in (first, second):
            fabrica.dump(plugin / "mcp.json", {
                "$schema": fabrica.SCHEMA + "mcp.schema.json",
                "mcpServers": {
                    "avilaops-central": {
                        "type": "streamable-http",
                        "url": "https://example.com/mcp",
                    }
                },
            })
        fabrica.marketplace()
        with self.assertRaisesRegex(ValueError, "Servidor MCP duplicado"):
            fabrica.check_all()

    def test_markdown_links_must_resolve(self):
        docs = self.root / "docs"
        docs.mkdir()
        guide = docs / "guide.md"
        guide.write_text("[válido](../README.md) [modelo]({skill-folder}/SKILL.md)", encoding="utf-8")
        (self.root / "README.md").write_text("# Marketplace\n", encoding="utf-8")
        fabrica.validate_markdown_links(self.root)
        guide.write_text("[quebrado](ausente.md)", encoding="utf-8")
        with self.assertRaises(ValueError):
            fabrica.validate_markdown_links(self.root)


if __name__ == "__main__":
    unittest.main()
