"""Fail closed: evidence checks are not a distribution authorization."""
import json
import os
from pathlib import Path

ROOT = Path("reports")
DIGEST = "c68e7e8cb941f0f21892f27f2b7ab03e619b0f19763cbe8478eb4195643e3c98"
EXPECTED = {"Windows": ["win32", "amd64"], "macOS": ["darwin", "arm64"]}
for os_name, target in EXPECTED.items():
    root = ROOT / ("evidence-" + os_name)
    native = json.loads((root / "native.json").read_text(encoding="utf-8"))
    assert native["sha"] == os.environ["GITHUB_SHA"]
    assert native["lock_sha256"] == DIGEST and native["platform"] == target
    assert native["onnx_inference"] == "PASS" and native["piper_api"] == "PASS"
    inventory = json.loads((root / "licenses.json").read_text(encoding="utf-8"))
    audit = json.loads((root / "vulnerabilities.json").read_text(encoding="utf-8"))
    installed = {(d["name"], d["version"]) for d in inventory}
    scanned = {(d["name"].lower().replace("_", "-"), d["version"]) for d in audit["dependencies"] if "skip_reason" not in d}
    assert installed and installed == scanned, "incomplete vulnerability coverage"
    assert not any(d.get("vulns") or d.get("skip_reason") for d in audit["dependencies"])
    sbom = json.loads((root / "sbom.json").read_text(encoding="utf-8"))
    assert sbom["bomFormat"] == "CycloneDX" and sbom["components"]
    components = {(d["name"].lower().replace("_", "-"), d["version"]) for d in sbom["components"]}
    assert installed <= components, "incomplete SBOM"
    print(os_name, "runtime/security evidence accepted; license inventory is not approval")
print("HOLD: Piper WAV fixture and distribution license approval absent; source admission pending.")
raise SystemExit(1)
