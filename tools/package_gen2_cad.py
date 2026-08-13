"""Create and verify deterministic Gen2 STEP/STL download archives."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "cad" / "BUILD_GEN2.json"
OUTPUT = ROOT / "cad" / "exports" / "gen2"
MANIFEST = OUTPUT / "PACKAGE.json"
FIXED_ZIP_TIME = (2026, 8, 13, 0, 0, 0)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_archive(kind: str, manifest: dict) -> dict:
    archive = OUTPUT / f"Bolley_Gen2_{kind.upper()}.zip"
    records = []
    with zipfile.ZipFile(archive, "w") as handle:
        for part_name, part in sorted(manifest["artifacts"].items()):
            source = ROOT / part[kind]["path"]
            if not source.exists():
                raise SystemExit(
                    f"missing {kind.upper()} source; run cad/build_gen2.py --write"
                )
            payload = source.read_bytes()
            member = source.name
            info = zipfile.ZipInfo(member, date_time=FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            handle.writestr(info, payload, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
            records.append(
                {
                    "part": part_name,
                    "source_path": str(source.relative_to(ROOT)),
                    "archive_member": member,
                    "bytes": len(payload),
                    "sha256": sha256_bytes(payload),
                }
            )
    return {
        "path": str(archive.relative_to(ROOT)),
        "bytes": archive.stat().st_size,
        "sha256": sha256(archive),
        "member_count": len(records),
        "members": records,
    }


def write() -> None:
    manifest = json.loads(BUILD.read_text(encoding="utf-8"))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    packages = {
        kind: build_archive(kind, manifest) for kind in ("step", "stl")
    }
    payload = {
        "schema_version": 1,
        "generation": "Gen2",
        "evidence": "DETERMINISTIC ARCHIVES OF CAD OUTPUT; not a manufacturing release",
        "build_manifest": str(BUILD.relative_to(ROOT)),
        "build_manifest_sha256": sha256(BUILD),
        "fixed_zip_timestamp": "2026-08-13T00:00:00",
        "packages": packages,
        "regeneration": [
            "python cad/build_gen2.py --write",
            "python tools/package_gen2_cad.py --write",
        ],
    }
    MANIFEST.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def check() -> None:
    if not MANIFEST.exists():
        raise SystemExit("missing cad/exports/gen2/PACKAGE.json")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["build_manifest_sha256"] != sha256(BUILD):
        raise SystemExit("Gen2 CAD package is stale relative to BUILD_GEN2.json")
    for package in manifest["packages"].values():
        archive = ROOT / package["path"]
        if (
            not archive.exists()
            or archive.stat().st_size != package["bytes"]
            or sha256(archive) != package["sha256"]
        ):
            raise SystemExit(f"stale Gen2 archive: {archive.relative_to(ROOT)}")
        with zipfile.ZipFile(archive) as handle:
            if len(handle.namelist()) != package["member_count"]:
                raise SystemExit(f"member-count mismatch: {archive.relative_to(ROOT)}")
            for record in package["members"]:
                payload = handle.read(record["archive_member"])
                if len(payload) != record["bytes"] or sha256_bytes(payload) != record["sha256"]:
                    raise SystemExit(
                        f"member mismatch: {archive.relative_to(ROOT)}::{record['archive_member']}"
                    )
    print("OK: deterministic Gen2 STEP/STL archives match PACKAGE.json")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("choose exactly one of --write or --check")
    write() if args.write else check()


if __name__ == "__main__":
    main()
