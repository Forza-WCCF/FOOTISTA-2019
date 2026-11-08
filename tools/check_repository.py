"""Check the small public inventory, release records and relative Markdown links."""

import hashlib
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

from verify_download import ASSETS, ROOT, load_record

ROOT_FILES = {".gitattributes", ".gitignore", "README.md", "CHANGELOG.md", "CONTRIBUTING.md", "SUPPORT.md"}
FOLDERS = {".github", "assets", "docs", "releases", "tools", "tests"}
EXTENSIONS = {".md", ".py", ".json", ".yml", ".svg", ".ed25519"}


def check(root=ROOT):
    root = Path(root).resolve()
    files = [p for p in root.rglob("*") if p.is_file() and not set(p.relative_to(root).parts) & {".git", "__pycache__"}]
    for path in files:
        rel = path.relative_to(root)
        if path.is_symlink() or path.stat().st_size > 256_000:
            raise ValueError("Unexpected file or size: " + rel.as_posix())
        if len(rel.parts) == 1:
            if rel.as_posix() not in ROOT_FILES:
                raise ValueError("Unexpected root file: " + rel.as_posix())
        elif rel.parts[0] not in FOLDERS or path.suffix not in EXTENSIONS:
            raise ValueError("Unexpected public file: " + rel.as_posix())
        if path.suffix == ".md":
            text = path.read_text(encoding="utf-8")
            links = re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text)
            links += re.findall(r'(?:src|href)="([^"]+)"', text)
            for raw in links:
                parts = urlsplit(raw)
                if parts.scheme or parts.netloc or not parts.path:
                    continue
                target = (path.parent / unquote(parts.path)).resolve()
                if not target.is_relative_to(root) or not target.exists():
                    raise ValueError("Broken local link in " + rel.as_posix() + ": " + raw)
    key = (root / "releases/public-key.ed25519").read_bytes()
    if len(key) != 32:
        raise ValueError("Expected a 32-byte public Ed25519 key")
    records = list((root / "releases").glob("*.json"))
    if not records:
        raise ValueError("At least one explicit release-status record is required")
    for path in records:
        record = load_record(path.stem, root)
        if record.get("public_key_sha256") != hashlib.sha256(key).hexdigest():
            raise ValueError("Publisher fingerprint differs: " + path.name)
        if set(record["assets"]) != ASSETS:
            raise ValueError("Unexpected asset inventory")
    svg = ET.parse(root / "assets/banner.svg")
    for node in svg.iter():
        if node.tag.rsplit("}", 1)[-1] in {"script", "foreignObject", "image"}:
            raise ValueError("Banner must be self-contained SVG")
        if any(k.rsplit("}", 1)[-1] in {"href", "src"} for k in node.attrib):
            raise ValueError("Banner must not fetch external resources")
    total = sum(p.stat().st_size for p in files)
    if total > 512_000:
        raise ValueError("Public repository exceeded its small-documentation budget")
    print(f"Checked {len(files)} files, {len(records)} release record(s), local links and banner; {total:,} bytes.")


if __name__ == "__main__":
    try:
        check()
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
