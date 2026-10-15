from __future__ import annotations

import json
import os
import unittest
from unittest.mock import patch

from beget_mcp.server import (
    BegetApiError,
    BegetMcpError,
    build_request_data,
    call_beget_api,
    unwrap_response,
)


class ApiContractTests(unittest.TestCase):
    def test_json_input_format_uses_input_data(self) -> None:
        data = build_request_data("login", "secret", {"fqdn": "пример.рф"}, "json")

        self.assertEqual(data["input_format"], "json")
        self.assertEqual(json.loads(data["input_data"]), {"fqdn": "пример.рф"})
        self.assertEqual(data["output_format"], "json")

    def test_plain_input_format_flattens_scalars_and_serializes_collections(self) -> None:
        data = build_request_data(
            "login",
            "secret",
            {"fqdn": "example.test", "records": [{"value": "127.0.0.1"}]},
            "plain",
        )

        self.assertNotIn("input_data", data)
        self.assertEqual(data["fqdn"], "example.test")
        self.assertEqual(json.loads(data["records"]), [{"value": "127.0.0.1"}])

    def test_success_envelope_returns_nested_result(self) -> None:
        result = unwrap_response(
            {"status": "success", "answer": {"status": "success", "result": [1, 2]}},
            return_raw=False,
        )

        self.assertEqual(result, [1, 2])

    def test_request_and_method_errors_remain_distinct(self) -> None:
        with self.assertRaises(BegetApiError) as request_error:
            unwrap_response(
                {"status": "error", "error_code": "AUTH_ERROR", "error_text": "Denied"},
                return_raw=False,
            )
        self.assertEqual(request_error.exception.code, "AUTH_ERROR")

        with self.assertRaises(BegetApiError) as method_error:
            unwrap_response(
                {
                    "status": "success",
                    "answer": {
                        "status": "error",
                        "errors": [{"error_code": "INVALID_DATA"}],
                    },
                },
                return_raw=False,
            )
        self.assertEqual(method_error.exception.code, "METHOD_ERROR")

    def test_side_effectful_call_requires_both_write_gates(self) -> None:
        with patch.dict(
            os.environ,
            {"BEGET_LOGIN": "login", "BEGET_API_PASSWORD": "secret"},
            clear=True,
        ):
            with self.assertRaises(BegetMcpError) as disabled:
                call_beget_api("site", "add", {"name": "example.test"})
            self.assertEqual(disabled.exception.code, "WRITE_DISABLED")

        with patch.dict(
            os.environ,
            {
                "BEGET_LOGIN": "login",
                "BEGET_API_PASSWORD": "secret",
                "BEGET_ALLOW_WRITE": "true",
            },
            clear=True,
        ):
            with self.assertRaises(BegetMcpError) as unconfirmed:
                call_beget_api("site", "add", {"name": "example.test"})
            self.assertEqual(unconfirmed.exception.code, "WRITE_NOT_CONFIRMED")

    def test_documented_statistics_alias_uses_real_endpoint(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            result = call_beget_api("stat", "getSiteListLoad", {}, dry_run=True)

        self.assertEqual(result["method"]["endpoint_method"], "getSitesListLoad")
        self.assertEqual(
            result["request"]["endpoint"],
            "https://api.beget.com/api/stat/getSitesListLoad",
        )


if __name__ == "__main__":
    unittest.main()
