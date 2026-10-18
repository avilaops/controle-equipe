import copy
import json
from pathlib import Path
import tempfile
import unittest

import equipe


class TeamTests(unittest.TestCase):
    def setUp(self):
        self.data = {"schemaVersion": 1, "application": "avila-teste",
                     "members": [{"id": "dev", "name": "Pessoa", "role": "Desenvolvimento"}],
                     "tasks": [{"id": "T-0001", "title": "Demanda", "owner": "dev",
                                "acceptance": "Resultado comprovado", "status": "a-fazer", "history": []}],
                     "decisions": [], "integrations": []}

    def test_reject_unknown_owner_and_duplicate_ids(self):
        wrong = copy.deepcopy(self.data)
        wrong["tasks"][0]["owner"] = "ausente"
        with self.assertRaises(ValueError):
            equipe.validate(wrong)
        self.data["tasks"].append(copy.deepcopy(self.data["tasks"][0]))
        with self.assertRaises(ValueError):
            equipe.validate(self.data)

    def test_accept_unassigned_task_without_inventing_owner(self):
        self.data["tasks"][0]["owner"] = None

        equipe.validate(self.data)

    def test_completion_and_blocking_require_evidence(self):
        task = self.data["tasks"][0]
        task["status"] = "concluida"
        with self.assertRaises(ValueError):
            equipe.validate(self.data)
        task["evidence"] = "Teste executado e revisado"
        equipe.validate(self.data)
        task["status"] = "bloqueada"
        with self.assertRaises(ValueError):
            equipe.validate(self.data)
        task["blocker"] = "Dependencia indisponivel"
        equipe.validate(self.data)

    def test_atomic_save_and_mutual_exclusion(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "controle.json"
            with equipe.lock(path):
                with self.assertRaises(FileExistsError):
                    with equipe.lock(path):
                        pass
                equipe.save(path, self.data)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), self.data)
            self.assertFalse(path.with_suffix(".lock").exists())
            self.assertFalse(path.with_suffix(".json.tmp").exists())

    def test_numbering_does_not_reuse_existing_id(self):
        self.assertEqual(equipe.next_id([{"id": "T-0001"}, {"id": "T-0003"}], "T"), "T-0004")

    def test_normalize_legacy_record_preserves_data_and_uses_canonical_fields(self):
        import migrar_controle

        legacy = {
            "schemaVersion": 1,
            "application": "avila-teste",
            "members": [],
            "tasks": [{
                "id": "T-0001", "title": "Demanda legada",
                "objective": "Resultado verificavel", "assignee": "agente-nao-cadastrado",
                "acceptanceCriteria": ["Primeiro aceite", "Segundo aceite"],
                "status": "em_revisao", "evidence": ["teste aprovado"],
            }],
            "decisions": [{
                "id": "D-0001", "title": "Decisao preservada",
                "decision": "Manter o contrato", "date": "2026-10-18",
            }],
            "integrations": [{
                "id": "I-0001", "system": "ERP", "direction": "ERP -> Loja",
                "contract": "GET /v1/recurso", "status": "em_revisao",
            }],
        }

        normalized = migrar_controle.normalize(legacy)

        task = normalized["tasks"][0]
        self.assertIsNone(task["owner"])
        self.assertEqual("em-revisao", task["status"])
        self.assertEqual("Primeiro aceite\nSegundo aceite", task["acceptance"])
        self.assertEqual("teste aprovado", task["evidence"])
        self.assertEqual("agente-nao-cadastrado", task["assignee"])
        self.assertEqual("Decisao preservada", normalized["decisions"][0]["summary"])
        self.assertEqual("ERP", normalized["integrations"][0]["name"])
        equipe.validate(normalized)

    def test_normalize_preserves_unknown_explicit_owner_as_legacy_metadata(self):
        import migrar_controle

        legacy = copy.deepcopy(self.data)
        legacy["tasks"][0]["owner"] = "responsavel-legado"

        normalized = migrar_controle.normalize(legacy)

        self.assertIsNone(normalized["tasks"][0]["owner"])
        self.assertEqual(
            "responsavel-legado", normalized["tasks"][0].get("legacyOwner")
        )

    def test_normalize_does_not_relabel_integration_metadata(self):
        import migrar_controle

        legacy = copy.deepcopy(self.data)
        legacy["integrations"] = [{
            "id": "I-0001", "system": "ERP", "status": "em_revisao",
            "direction": "ERP -> Loja", "contract": "GET /v1/recurso",
        }]

        normalized = migrar_controle.normalize(legacy)
        integration = normalized["integrations"][0]

        self.assertEqual("em_revisao", integration["status"])
        self.assertEqual("ERP -> Loja", integration["direction"])
        self.assertEqual(
            "Ambiente não informado no registro original",
            integration["environment"],
        )
        self.assertEqual(
            "Identidade não informada no registro original",
            integration["identity"],
        )

    def test_migration_respects_active_record_lock(self):
        import migrar_controle

        self.assertTrue(hasattr(migrar_controle, "migrate"))

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "controle.json"
            path.write_text(
                json.dumps(self.data, ensure_ascii=False), encoding="utf-8"
            )
            original = path.read_bytes()

            with equipe.lock(path):
                with self.assertRaises(FileExistsError):
                    migrar_controle.migrate(path)

            self.assertEqual(original, path.read_bytes())


if __name__ == "__main__":
    unittest.main()
