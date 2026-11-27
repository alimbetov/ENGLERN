# Acceptance matrix
Evidence for each gate: commit SHA, lock hash, OS build/arch, device CPU/RAM, model hashes, command, expected/actual, test IDs, report path, date, PASS/FAIL/SKIP with reason. SKIP on required case = HOLD. CI headless never substitutes real devices. Tests below mandatory for affected stage.
| ID | Stage | Scenario / expected |
|---|---|---|
| Q00 | R0 | inventory SHA256, source provenance, exclusions and original/adapted diff; clean clone source reproducible or blocker explicitly logged (import gate only, not runtime PASS) |
| Q01 | R1 | native locked install both targets, dependency check/imports, verified arch; no Python needed for packaged artifact |
| Q02 | R1 | first run writable paths, same data after update/restart, second instance controlled |
| Q03 | R1 | model bundle hash/config validation, offline load and valid WAV; corrupt/interrupted download not READY |
| Q04 | R1 | single word/multilingual/batch mixed results, cache hit, cancel and late callback, disk full |
| Q05 | R1 | real speakers play/pause/seek/stop and speed on both OS; no unhandled media errors |
| Q06 | R1 | migrations, file reconciliation, backup/restore, unsupported schema safe |
| Q07 | R2 | 18 reviewed lessons, schema invalid fixtures, import round trip, revision pin, abbreviation/decimal segmentation |
| Q08 | R2 | sentence repeat 1/3/10/infinite, pause 0/10, pause/resume/skip/cancel while pending; no stale audio |
| Q09 | R2 | restart resumes sentence, user text and WAV export, offline session |
| Q10 | R2.5 | dictation oracle and comprehension choice/open answer |
| Q11 | R3.A/B | real microphone permission grant/deny, device unplug, silence/clipping, save/discard, A/B, restart and delete |
| Q12 | R3.C | local ASR native CPU, no network, no-speech handling, deterministic WER examples including >100% and N/A |
| Q13 | R4 | dictionary source/license, senses and IPA variants, phrase CRUD, Unicode round trip, scheduler dates and duplicate review |
| Q14 | R5 | 20 reviewed scenarios, custom import, recorded response, self-rubric, export, offline |
| Q15 | R6 | deterministic plan, due ordering, zero/missing, timezone, budget, duplicate attempts, metric oracle |
| Q16 | MVP/R7 | clean install without Python, upgrade preserves data, uninstall policy, offline, backup recovery, OS permission and UI keyboard/HiDPI |
| Q17 | R7 | signed/notarized where credentials available, explicit unsigned internal status otherwise; public release policy approved, licenses/SBOM/security scan, hashes and release notes |
| Q18 | R1 onward | 20 warm startups p95 <=5s, 100 GUI input-to-response samples p95 <=200ms on declared reference devices; exclude model loading for startup, measure under background TTS; initial targets confirmed/revised at R1 with rationale |
Unit/domain and affected integration tests every commit; native packaging on relevant changes; both OS exact-SHA full matrix for MVP and v1.0. Native user device checklist required before release. No critical/high unresolved defects affecting required scope. Public release blocked by unresolved licensing, security, or unapproved signing policy. Internal unsigned builds labeled and limited to controlled testing. R7 includes initial packaging at R1 and MVP subset before v0.5; no contradiction with final v1.0 gate.
