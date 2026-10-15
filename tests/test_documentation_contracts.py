from __future__ import annotations

import json
import unittest
from pathlib import Path
from urllib.parse import urlsplit

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOC_METHODS = PROJECT_ROOT / "docs" / "schema" / "methods.json"
PACKAGE_METHODS = PROJECT_ROOT / "src" / "beget_mcp" / "data" / "methods.json"
PAGES = PROJECT_ROOT / "docs" / "schema" / "pages.json"


class DocumentationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.methods = json.loads(DOC_METHODS.read_text(encoding="utf-8"))
        cls.pages = json.loads(PAGES.read_text(encoding="utf-8"))

    def test_documentation_and_package_catalogs_are_identical(self) -> None:
        self.assertEqual(DOC_METHODS.read_bytes(), PACKAGE_METHODS.read_bytes())

    def test_expected_inventory_is_complete_and_unique(self) -> None:
        self.assertEqual(len(self.pages), 12)
        self.assertEqual(len(self.methods), 65)
        keys = [(item["section"], item["method"]) for item in self.methods]
        self.assertEqual(len(keys), len(set(keys)))

    def test_all_endpoints_are_https_on_the_fixed_beget_host(self) -> None:
        for item in self.methods:
            with self.subTest(method=f"{item['section']}.{item['method']}"):
                endpoint = urlsplit(item["endpoint"])
                self.assertEqual(endpoint.scheme, "https")
                self.assertEqual(endpoint.netloc, "api.beget.com")
                self.assertEqual(
                    endpoint.path,
                    f"/api/{item['section']}/{item['endpoint_method']}",
                )

    def test_structured_parameter_metadata_is_preserved(self) -> None:
        dns_get_data = next(
            item
            for item in self.methods
            if item["section"] == "dns" and item["method"] == "getData"
        )
        self.assertEqual([item["name"] for item in dns_get_data["parameters"]], ["fqdn"])

        create_mailbox = next(
            item
            for item in self.methods
            if item["section"] == "mail" and item["method"] == "createMailbox"
        )
        password = next(item for item in create_mailbox["parameters"] if item["name"] == "mailbox_password")
        self.assertTrue(password["sensitive"])

    def test_known_upstream_documentation_defects_are_explicit(self) -> None:
        warnings = {
            (item["section"], item["method"]): item["notes"]
            for item in self.methods
            if item["notes"]
        }
        self.assertIn(("cron", "edit"), warnings)
        self.assertIn(("dns", "changeRecords"), warnings)
        self.assertIn(("domain", "getPhpVersion"), warnings)
        self.assertIn(("mail", "forwardListAddMailbox"), warnings)
        self.assertIn(("mail", "forwardListDeleteMailbox"), warnings)
        self.assertIn(("stat", "getSiteListLoad"), warnings)


if __name__ == "__main__":
    unittest.main()
