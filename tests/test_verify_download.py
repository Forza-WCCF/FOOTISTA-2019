import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from verify_download import ASSETS, load_record, main, verify


class VerificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="footista-public-check-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.file = self.root / "installer.zip"
        self.file.write_bytes(b"tiny test asset")
        asset = {"bytes": self.file.stat().st_size,
                 "sha256": hashlib.sha256(self.file.read_bytes()).hexdigest()}
        self.record = {"version": "1.2.3", "sequence": 1, "status": "unreleased-candidate",
                       "assets": {name: dict(asset) for name in ASSETS}}
        (self.root / "releases").mkdir()
        self.save_record()

    def save_record(self):
        (self.root / "releases/1.2.3.json").write_text(json.dumps(self.record), encoding="utf-8")

    def test_matching_asset_keeps_candidate_status(self):
        result = verify(self.file, load_record("1.2.3", self.root))
        self.assertEqual(result["status"], "unreleased-candidate")

    def test_altered_same_size_bytes_are_rejected(self):
        self.file.write_bytes(b"x" * self.file.stat().st_size)
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            verify(self.file, self.record)

    def test_truncated_asset_is_rejected(self):
        self.file.write_bytes(b"short")
        with self.assertRaisesRegex(ValueError, "size"):
            verify(self.file, self.record)

    def test_renamed_asset_requires_explicit_name(self):
        renamed = self.root / "installer (1).zip"
        renamed.write_bytes(self.file.read_bytes())
        with self.assertRaisesRegex(ValueError, "Unknown asset"):
            verify(renamed, self.record)
        self.assertEqual(verify(renamed, self.record, "installer.zip")["artifact"], "installer.zip")

    def test_version_cannot_escape_releases(self):
        for version in ("../1.2.3", "1.2.3/other", "C:\\1.2.3", ""):
            with self.subTest(version=version), self.assertRaises(ValueError):
                load_record(version, self.root)

    def test_unknown_status_and_mismatched_version_are_rejected(self):
        for change in ({"status": "accepted-ish"}, {"version": "4.5.6"}):
            with self.subTest(change=change):
                original = dict(self.record)
                self.record.update(change)
                self.save_record()
                with self.assertRaises(ValueError):
                    load_record("1.2.3", self.root)
                self.record = original

    def test_invalid_size_and_hash_are_rejected(self):
        for change in ({"bytes": True}, {"bytes": 0}, {"sha256": "f" * 63}):
            with self.subTest(change=change):
                original = dict(self.record["assets"]["installer.zip"])
                self.record["assets"]["installer.zip"].update(change)
                self.save_record()
                with self.assertRaises(ValueError):
                    load_record("1.2.3", self.root)
                self.record["assets"]["installer.zip"] = original

    def test_unknown_or_missing_asset_is_rejected(self):
        self.record["assets"].pop("release.json")
        self.save_record()
        with self.assertRaises(ValueError):
            load_record("1.2.3", self.root)

    def test_cli_failure_returns_nonzero_without_traceback(self):
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            result = main([str(self.file), "--version", "../bad"])
        self.assertEqual(result, 1)
        self.assertIn("Verification failed", error.getvalue())
        self.assertNotIn("Traceback", error.getvalue())


if __name__ == "__main__":
    unittest.main()
