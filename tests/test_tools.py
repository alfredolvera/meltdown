from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import struct
import tempfile
import unittest
import zipfile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ki_project", PROJECT_ROOT / "tools" / "ki_project.py")
assert SPEC is not None and SPEC.loader is not None
KI_PROJECT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(KI_PROJECT)


class ToolTests(unittest.TestCase):
    def test_zip_inventory_hashes_uncompressed_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "sample.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("sample.bin", b"killer-instinct-test")
            result = KI_PROJECT.inspect_zip(archive_path)
            self.assertEqual(result["kind"], "zip")
            self.assertEqual(result["entries"][0]["name"], "sample.bin")
            self.assertEqual(result["entries"][0]["size"], 20)
            self.assertEqual(len(result["entries"][0]["sha256"]), 64)

    def test_valid_provenance_record(self) -> None:
        record = {
            "schema_version": 1,
            "id": "ki15d_80001234",
            "name": "test_function",
            "game": {
                "mame_set": "kinst",
                "revision": "v1.5d",
                "input_manifest": "work/input-inventory.json",
            },
            "original": {
                "cpu": "R4600LE",
                "virtual_address": "0x80001234",
                "assembly_path": "work/asm/ki15d_80001234.s",
            },
            "reconstruction": {
                "kind": "decompilation",
                "status": "stub",
                "source_path": "native/src/original/ki15d_80001234.c",
                "hardware_dependencies": [],
            },
            "verification": {
                "status": "unverified",
                "fixtures": [],
                "commands": [],
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ki15d_80001234.json"
            path.write_text(json.dumps(record), encoding="utf-8")
            self.assertEqual(KI_PROJECT.validate_record(path), [])

    def test_invalid_address_is_rejected(self) -> None:
        template = json.loads(
            (PROJECT_ROOT / "provenance" / "functions" / "TEMPLATE.json").read_text(
                encoding="utf-8"
            )
        )
        template.pop("_template")
        template["original"]["virtual_address"] = "80001234"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ki15d_80001234.json"
            path.write_text(json.dumps(template), encoding="utf-8")
            errors = KI_PROJECT.validate_record(path)
            self.assertTrue(any("hexadecimal" in error for error in errors))

    def test_chd_v5_identity_is_read_from_header(self) -> None:
        combined_sha1 = bytes.fromhex("81d833236e994528d1482979261401b198d1ca53")
        header = bytearray(124)
        header[:8] = b"MComprHD"
        header[8:12] = struct.pack(">I", 124)
        header[12:16] = struct.pack(">I", 5)
        header[16:32] = b"lzmazlibhuffflac"
        header[32:40] = struct.pack(">Q", 131076608)
        header[56:60] = struct.pack(">I", 4096)
        header[60:64] = struct.pack(">I", 512)
        header[64:84] = bytes.fromhex("a37a2c5e52ea936a715210d237874dd573bb002f")
        header[84:104] = combined_sha1
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.chd"
            path.write_bytes(header)
            result = KI_PROJECT.inspect_chd_header(path)
            self.assertTrue(result["valid"])
            self.assertEqual(result["version"], 5)
            self.assertEqual(result["logical_bytes"], 131076608)
            self.assertEqual(result["known_input"]["role"], "ata_disk_chd_logical")

    def test_compare_loaded_segments_reports_runtime_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            segments = root / "segments"
            segments.mkdir()
            (segments / "rom-0.addr").write_bytes(struct.pack("=I", 0x08000002))
            (segments / "rom-0.bin").write_bytes(b"CDEF")
            memory = root / "memory.bin"
            memory.write_bytes(b"ABCDXF")
            result = KI_PROJECT.compare_loaded_segments(segments, memory, 0x08000000)
            item = result["segments"][0]
            self.assertEqual(item["matching_bytes"], 3)
            self.assertEqual(item["differing_bytes"], 1)
            self.assertEqual(
                item["first_differing_ranges"],
                [{"start": "0x08000004", "end": "0x08000004"}],
            )


if __name__ == "__main__":
    unittest.main()
