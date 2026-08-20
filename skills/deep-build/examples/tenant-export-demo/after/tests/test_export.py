import sys
from pathlib import Path
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from export import export_rows


class ExportRowsTest(unittest.TestCase):
    def test_export_filters_to_requested_tenant(self):
        rows = [
            {"tenant_id": "tenant-a", "id": 1},
            {"tenant_id": "tenant-b", "id": 2},
        ]
        self.assertEqual(export_rows(rows, "tenant-a"), [{"tenant_id": "tenant-a", "id": 1}])


if __name__ == "__main__":
    unittest.main()
