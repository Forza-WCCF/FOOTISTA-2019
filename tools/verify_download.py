"""Check a local release asset against this repository's public version record."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {"unreleased-candidate", "prerelease", "released"}
ASSETS = {"installer.zip", "client.zip", "release.json"}


def load_record(version, root=ROOT):
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[A-Za-z0-9._-]+)?", version):
        raise ValueError("Use a version such as 0.2.18")
    record = json.loads((Path(root) / "releases" / (version + ".json")).read_text(encoding="utf-8"))
    if record.get("version") != version or record.get("status") not in STATUSES:
        raise ValueError("Invalid public release record")
    if type(record.get("sequence")) is not int or record["sequence"] < 1:
        raise ValueError("Invalid release sequence")
    if set(record.get("assets", {})) != ASSETS:
        raise ValueError("Release record must describe the installer, client and signed metadata")
    for asset in record["assets"].values():
        if type(asset.get("bytes")) is not int or asset["bytes"] <= 0:
            raise ValueError("Invalid asset size")
        if not re.fullmatch(r"[a-f0-9]{64}", asset.get("sha256", "")):
            raise ValueError("Invalid SHA-256")
    return record


def verify(path, record, artifact=None):
    path = Path(path)
    artifact = artifact or path.name
    if artifact not in ASSETS or artifact not in record["assets"]:
        raise ValueError("Unknown asset name; use --artifact for a renamed download")
    expected = record["assets"][artifact]
    if path.stat().st_size != expected["bytes"]:
        raise ValueError("File size differs from the release record")
    with path.open("rb") as stream:
        actual = hashlib.file_digest(stream, "sha256").hexdigest()
    if actual != expected["sha256"]:
        raise ValueError("SHA-256 differs from the release record")
    return {"version": record["version"], "status": record["status"],
            "artifact": artifact, "bytes": expected["bytes"], "sha256": actual}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--version", required=True)
    parser.add_argument("--artifact", choices=sorted(ASSETS))
    args = parser.parse_args(argv)
    try:
        result = verify(args.file, load_record(args.version), args.artifact)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Verification failed: " + str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    if result["status"] == "unreleased-candidate":
        print("Bytes match an UNRELEASED CANDIDATE, not an accepted public release.")
    else:
        print("Size and SHA-256 match. The installer also verifies the signed release.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
