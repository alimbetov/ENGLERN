# ENGLERN-DIST-R1 — Product Website, Distribution & Release Management
Status: approved distribution matrix; implementation pending. Design branch only. Existing R1.2–R7 scope remains unchanged. No backend, accounts, telemetry or new development branches required.

## DIST-R1.1 — Four native installers
One codebase, one version, one source SHA, one dependency lock. Edition is packaging only, not a feature tier.
| OS | Standard (no bundled voice) | Offline (bundled English voice) |
|---|---|---|
| Windows x64 | ENGLERN-{version}-windows-x64-standard-setup.exe | ENGLERN-{version}-windows-x64-offline-setup.exe |
| macOS Apple Silicon ARM64 | ENGLERN-{version}-macos-arm64-standard.dmg | ENGLERN-{version}-macos-arm64-offline.dmg |

Standard includes all runtime libraries and voice downloader; existing compatible user-installed voices remain usable offline. Offline includes verified ONNX and matching ONNX.JSON and works immediately after installation with network disabled. No separate script or model ZIP required for Offline. Both support additional voices and user imports under the model lifecycle contract; no automatic replacement of user data or custom voices. Intel macOS and Windows ARM64 out of scope. Approximate compressed sizes based on earlier packages, not acceptance criteria: Windows 70/185 MB, macOS 100/220 MB.

## DIST-R1.2 — Release storage
GitHub Releases immutable versioned assets; Actions artifacts are temporary internal evidence only. Release manifest release.json: schemaVersion, version, channel, sourceSha, publishedAt, assets[{os,arch,edition,name,url,sizeBytes,sha256,modelId,modelVersion,modelSha256,configSha256}]. Standard model fields null. Offline model identity, license and provenance required; HTTPS links to same versioned release, no secrets or mutable upstream refs. SHA256SUMS and third-party notices included. Alpha/Beta/Stable channels; prereleases never advertised as stable. No overwrite of published version; repair via new version. Public distribution only after license and applicable signing approval.

## DIST-R1.3 — Product site
Static HTML/CSS/JS on GitHub Pages, initially en/ru, responsive and accessible; four clearly labeled download options, OS/architecture, edition, actual size, version, release notes, installation instructions, checksum and license links. Default recommend Offline for new users when available; Standard for existing models or limited bandwidth. No automatic downloads. Explicit unavailable state for unqualified edition. Site consumes published manifest; no Actions artifact links as official download. Custom domain optional later.

## DIST-R1.4 — Build and admission
Native 2x2 matrix on Windows and macOS; use existing uv lock and PyInstaller, Inno Setup/hdiutil. Edition passed explicitly, output names distinct; Offline must fail if voice pair missing or hash/config mismatch. Model source and license approved and pinned before CI download; do not commit large ONNX binaries into source or expose supplied Lessac model without redistribution clearance. Lessac is candidate only, alternative requires confirmed redistribution rights. License review includes Piper, Qt and bundled model/dataset obligations. No public release based solely on source ownership. Standard must exclude model binaries. Verify each final installer independently; GUI startup, install/upgrade/uninstall, preserve user data, audio playback, artifact checksum. Offline: clean user profile, block network, load bundled model, synthesize non-silent PCM WAV and play; verify no downloads. Standard: clean profile missing voice gives actionable prompt, then install approved model and synthesize offline. Reject edition mismatch or missing assets. Real device UAT and applicable signature/notarization evidence separate from runner smoke. Four successful packaging jobs do not alone constitute release admission. Publish only after required checks on exact SHA and explicit release approval; atomically expose manifest after assets verified. If Offline license gate is blocked, Standard can be independently approved, site marks Offline unavailable; never mislabel as complete four-edition release.

## DIST-R1.5–R1.7
Version history and release notes; optional custom domain; explicit opt-in/manual update checker using channel manifest, HTTPS, checksum verification and user-confirmed installer launch (no silent execution). Preserve offline application use when update service unavailable.

## Implementation order
DIST-R1.1 packaging matrix and local qualification; DIST-R1.2 manifest/storage; DIST-R1.3 static site; DIST-R1.4 gated publication automation; DIST-R1.5 notes; DIST-R1.6 optional domain; DIST-R1.7 update checker. Implement in base_dev. Keep main stable until release admission. No claim that four installers or website already exist.
