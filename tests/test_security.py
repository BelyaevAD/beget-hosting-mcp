from __future__ import annotations

import unittest

from beget_mcp.server import make_error_response, redact


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


if __name__ == "__main__":
    unittest.main()
