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


if __name__ == "__main__":
    unittest.main()
