from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def encode_ndjson(message: dict[str, object]) -> bytes:
    return (json.dumps(message, separators=(",", ":")) + "\n").encode("utf-8")


def encode_content_length(message: dict[str, object]) -> bytes:
    body = json.dumps(message, separators=(",", ":")).encode("utf-8")
    return f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body


def initialize_request() -> dict[str, object]:
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "protocol-test", "version": "1.0"},
        },
    }


class StdioProtocolTests(unittest.TestCase):
    def run_server(self, input_bytes: bytes) -> subprocess.CompletedProcess[bytes]:
        env = os.environ.copy()
        source_path = str(PROJECT_ROOT / "src")
        env["PYTHONPATH"] = source_path + os.pathsep + env.get("PYTHONPATH", "")
        return subprocess.run(
            [sys.executable, "-u", "-m", "beget_mcp.server"],
            cwd=PROJECT_ROOT,
            env=env,
            input=input_bytes,
            capture_output=True,
            timeout=5,
            check=False,
        )

    def test_cursor_ndjson_handshake_and_tool_discovery(self) -> None:
        initialized = {"jsonrpc": "2.0", "method": "notifications/initialized"}
        tools_list = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}

        result = self.run_server(
            encode_ndjson(initialize_request()) + encode_ndjson(initialized) + encode_ndjson(tools_list)
        )

        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", errors="replace"))
        self.assertEqual(result.stderr, b"")
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual([response["id"] for response in responses], [1, 2])
        self.assertEqual(responses[0]["result"]["protocolVersion"], "2025-06-18")
        self.assertEqual(
            [tool["name"] for tool in responses[1]["result"]["tools"]],
            [
                "beget_list_methods",
                "beget_get_method_docs",
                "beget_call",
                "beget_get_account_info",
            ],
        )

    def test_content_length_clients_remain_supported(self) -> None:
        result = self.run_server(encode_content_length(initialize_request()))

        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", errors="replace"))
        header, body = result.stdout.split(b"\r\n\r\n", 1)
        self.assertEqual(header, f"Content-Length: {len(body)}".encode("ascii"))
        response = json.loads(body)
        self.assertEqual(response["id"], 1)
        self.assertIn("tools", response["result"]["capabilities"])

    def test_latest_legacy_protocol_and_structured_tool_contracts(self) -> None:
        request = initialize_request()
        request["params"]["protocolVersion"] = "2025-11-25"
        tools_list = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}

        result = self.run_server(encode_ndjson(request) + encode_ndjson(tools_list))

        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", errors="replace"))
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(responses[0]["result"]["protocolVersion"], "2025-11-25")
        for tool in responses[1]["result"]["tools"]:
            self.assertEqual(tool["outputSchema"]["required"], ["result"])


if __name__ == "__main__":
    unittest.main()
