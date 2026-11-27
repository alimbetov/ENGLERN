# ENGLERN-SPEC-R1.1 — Implementation Readiness & Architecture Hardening
Status: PROPOSED FOR APPROVAL. Normative successor to R1 upon approval. No implementation or platform qualification claimed. Original R1 retained for history.
## Scope and decisions
Local-first single-user desktop, Windows 11 x64 and macOS 14+ arm64 candidate minimum (actual floor determined by all native dependencies and native tests; raising it requires decision). Windows 10 and Intel Mac deferred. Python 3.12, PySide6, Piper, SQLite, PyInstaller; optional ASR at R3.C. No backend, mandatory account, cloud or telemetry. Preserve existing multilingual text/batch synthesis, voice selection and WAV export. English learning A1–C2, initial 3 original/licensed lessons per level, Russian/English UI. CEFR tags are editorial, not certification.
MVP v0.5 = R0, R1, R2.1–4, R3.A/B and MVP subset of R7. Dictation/comprehension R2.5 before v1.0; retelling and free speaking via recording at R3.B, expanded R5. v1.0 includes R3.C/R4/R5/R6/R7; experimental phoneme assessment explicitly excluded from release critical path. No automatic pronunciation score from ASR.
## Normative documents
- architecture/CORE-CONTRACTS.md (ENG-CORE-01–12)
- architecture/AUDIO-ENGINE.md
- architecture/MODEL-LIFECYCLE.md
- architecture/PERSISTENCE.md
- architecture/LEARNING-CONTENT.md and learning-content.schema.json
- architecture/DEPENDENCY-BASELINE.md
- ui/UI-DESIGN-SYSTEM.md
- qualification/ACCEPTANCE-MATRIX.md
- IMPLEMENTATION-ROADMAP.md
This index defines scope; specialized contracts define details. Conflicts stop the affected work and require documented resolution, not silent overrides. Existing R1 requirements retained unless explicitly replaced here. R1 numbering superseded by roadmap; R3.1=R3.A, R3.2=R3.B, R3.3=R3.C plus deferred research R3.D.
## Architecture
Presentation -> application use cases -> pure domain; infrastructure implements application ports, composition root wires concrete adapters. Domain does not import Qt/Piper/SQLite. Keep existing code via adapters, no wholesale rewrite or speculative abstractions. Shared audio, task, model and persistence modules. Module structure target src/englern/{platform,audio,learning,pronunciation,vocabulary,professional,adaptive,persistence,ui}; actual migration mapping at R0. Single instance per data root. Application ID io.github.alimbetov.englern. Data separate from installation and cache.
## Readiness
R0 may start immediately. R1 implementation after R0 inventory and approval of these contracts; dependency resolution is an R1 deliverable, not a prerequisite for writing its qualification task. Later stage-specific decisions are explicit gates: concrete dictionary source before R4, ASR runtime before R3.C, signing and licensing before public distribution. Do not mark these qualified in advance. No new feature beyond R0–R7 without scope approval. Original ZIP and adapted source not imported by this documentation change.
