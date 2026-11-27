# Implementation backlog and handoff
Status all PLANNED except repository initialization; no source import claimed. R0 GO, R1 conditional on R0 and design approval. Each task PR/commit references requirement, tests, evidence, known limits. main stable, base_dev implementation (create only when starting R0), design/englern-r1 spec. Baseline tag after import qualification, not before.
| Task | Deliverable | Depends | Gate |
|---|---|---|---|
| R0.1 | archive hashes, inventory, rights, excluded files | none | Q00 |
| R0.2 | original source import, gitignore, restoration guide, adapted diff | R0.1 rights | Q00 |
| R0.3 | original launch/regression inventory, tag | R0.2 | Q00 |
| R1.1 | pyproject/uv.lock, native resolver, dependency evidence | R0.3 | Q01 |
| R1.2 | application lifecycle/platform paths | R1.1 | Q02 |
| R1.3 | versioned model manager/manifest | R1.2 | Q03 |
| R1.4 | audio jobs/player/cache/batch adaptation | R1.3 | Q04,Q05 |
| R1.5 | SQLite migrations/reconciliation/backup | R1.2 (integrate R1.3–4 before gate; minimal persistence introduced as needed) | Q06 |
| R1.6 | shared UI foundation, RU/EN | R1.4–5 | Q02,Q05 |
| R1.7 | native CI/build/real devices/performance | R1.1–6 | Q01–06,Q18 |
| R2.1 | schema, importer, segmentation, immutable revision | R1.7 | Q07 |
| R2.2 | library and 18 lessons | R2.1 | Q07 |
| R2.3 | sentence controls/shared playback | R2.2 | Q08 |
| R2.4 | session FSM/repeats/shadowing/resume | R2.3 | Q08–09 |
| R3.A | recording service, permissions, durable files | R2.4 | Q11 |
| R3.B | A/B, retelling/free speaking recording/history | R3.A | Q11 |
| MVP v0.5 | native internal release, clean install/offline/backup | R3.B | Q01–09,Q11,Q16,Q18 + license/signing policy as applicable |
| R2.5 | dictation/comprehension/grammar notes | R2.4 | Q10 |
| R3.C | ASR optional group, local model, recognition metrics | R3.B | Q12 |
| R4 | vocabulary/IPA/translation/repetition | R2.1; source rights decision | Q13 |
| R5 | professional scenario bank | R2.5,R3.C,R4 | Q14 |
| R6 | plan and metrics | R4,R5 | Q15 |
| R7 | full release | all required prior gates | Q16–18, full exact SHA |
| R3.D research | phoneme validation separate, no release dependency | separate approval | independently defined |
## R4 concrete rules
Manual entry always works offline; curated/bundled dictionary adapter selected before R4 based on license, en-US/en-GB IPA coverage and RU translation sample review; no fabricated automatic translation. Sense and phrase identity separate, source labels and G2P estimate labels. Include collocations, phrasal verbs, examples, tags, search and archive, CSV/JSON round trip. Initial deterministic SRS v1 (not FSRS claim): Again=1 day, Hard=max(1,ceil(prior*1.2)), Good=max(3,ceil(prior*2)), Easy=max(7,ceil(prior*3)); prior default 1; cap 365 days; due=local review date + interval. One event per unique attempt ID, transaction event+state. Due cards ordered due date then stable ID. Review modes recognition/recall/listening, explicit self rating. Known words metric count distinct senses with at least one Good/Easy recall, not fluency.
## R5 rules
20 scenarios minimum (5 per IT/HR/Technical/Business); include STAR, Java/Spring/SQL, system design, meetings, standup, code review, negotiation. Reuse versioned lesson/exercise, prompt, optional preparation and response timers (default 30/120s editable), sample answer hidden until first attempt or explicit reveal. Rubric clarity/structure/completeness/vocabulary 1–5 self rating or N/A; no automatic correctness of free answer. Record/transcribe local, compare attempts, import custom questions, export transcript/audio by user choice.
## R6 rules
Profile self-assessed CEFR and goal, 10–120 min daily budget default 30. Planner v1 deterministic: reserve up to 30% for due reviews, then allocate remaining by weights listening .25, pronunciation .25, speaking .30, reading/comprehension .20; professional goal replaces up to 30% remaining with professional scenarios; only use available qualified activities, redistribute unavailable weights, floor minutes and distribute remainder stable order. Minimum item 5 min except reviews; never exceed budget, may underfill with reason. Weakness adjustment only after >=5 comparable attempts in last 30 days with available score; if mean <.6 increase relevant weight x1.5 then renormalize; self ratings separate and not treated as objective score. No automatic CEFR promotion. Stable tie-break due date, least recently completed, level match, ID; input hash + algorithm version ensures reproducibility. User edits create plan revision, completed items preserved, no silent rewrite. Metrics: active time union per day, completed exercise attempts unique IDs, studied senses and recall-known senses separate, recall rate successful Good/Easy recall / recall reviews, WER aggregate sum errors/sum reference words for matching normalization/task group, zero denominator N/A. No-data count zero only when known complete observation; charts 7/30/90 calendar days in profile timezone, timezone changes reaggregate from UTC events with stated policy. Weekly summary local. Explain recommendations.
## Audit trace
AUD-01 index and documents; AUD-02 R0; AUD-03/14 dependency and Q01; AUD-04/05 CORE/AUDIO; AUD-06 MODEL; AUD-07 PERSISTENCE; AUD-08/09 CONTENT+schema; AUD-10 AUDIO/Q11; AUD-11/12 R4/R6 gate and rules; AUD-13 dependency license gate; AUD-15 acceptance matrix. REV-01–15 addressed by R0 regression and R1/R2 requirements, actual defects remain open until code/tests. DEP-01–04 addressed by dependency qualification; no version qualified yet.
