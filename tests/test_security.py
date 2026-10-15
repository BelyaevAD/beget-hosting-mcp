from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from beget_mcp.server import call_beget_api, handle_request, make_error_response, redact


class SecurityTests(unittest.TestCase):
    def test_redact_covers_common_credential_field_names(self) -> None:
        value = {
            "BEGET_API_PASSWORD": "password-value",
            "Authorization": "Bearer token-value",
            "nested": {"api-token": "token-value", "method": "getList"},
        }

        result = redact(value)

        self.assertEqual(result["BEGET_API_PASSWORD"], "***REDACTED***")
        self.assertEqual(result["Authorization"], "***REDACTED***")
        self.assertEqual(result["nested"]["api-token"], "***REDACTED***")
        self.assertEqual(result["nested"]["method"], "getList")

    def test_internal_exception_details_are_not_returned_to_client(self) -> None:
        response = make_error_response(7, RuntimeError("sensitive internal detail"))

        self.assertEqual(response["error"]["message"], "Internal server error.")
        self.assertEqual(response["error"]["data"], {"code": "INTERNAL_ERROR"})
        self.assertNotIn("sensitive internal detail", str(response))

    def test_redact_removes_password_from_free_form_text(self) -> None:
        with patch.dict(os.environ, {"BEGET_API_PASSWORD": "test-secret-value"}):
            result = redact("request failed for test-secret-value")

        self.assertEqual(result, "request failed for ***REDACTED***")

    def test_dry_run_does_not_require_credentials(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            result = call_beget_api(
                "site",
                "add",
                {"name": "example.test"},
                dry_run=True,
            )

        self.assertTrue(result["dry_run"])
        self.assertEqual(result["request"]["body"]["passwd"], "***REDACTED***")
        self.assertNotIn("<BEGET_API_PASSWORD>", result["request"]["sanitized_url"])

    def test_string_confirm_write_is_rejected_by_server(self) -> None:
        response = handle_request(
            {
                "jsonrpc": "2.0",
                "id": 9,
                "method": "tools/call",
                "params": {
                    "name": "beget_call",
                    "arguments": {
                        "section": "site",
                        "method": "add",
                        "params": {"name": "example.test"},
                        "confirm_write": "true",
                    },
                },
            }
        )

        self.assertIsNotNone(response)
        result = response["result"]
        self.assertTrue(result["isError"])
        self.assertIn("confirm_write must be a boolean", result["content"][0]["text"])

    def test_tool_errors_use_mcp_tool_error_result(self) -> None:
        response = handle_request(
            {
                "jsonrpc": "2.0",
                "id": 10,
                "method": "tools/call",
                "params": {"name": "unknown", "arguments": {}},
            }
        )

        self.assertIsNotNone(response)
        self.assertNotIn("error", response)
        self.assertTrue(response["result"]["isError"])
        self.assertIn("UNKNOWN_TOOL", response["result"]["content"][0]["text"])


if __name__ == "__main__":
    unittest.main()
