# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Online group 2, Tuesday 17:30
Members and UG/PG applicability: Kynan and Nikola, UG


## A Release scope and starting SHA

Release label/version and requirements baseline: The release will be labelled SmartCare v1.0. The requirements baseline is Assignment 3 Overview/Revision 2, covering FR-01–FR-09, QRY-01–04, FP-01–03 and the applicable UI requirements. FR-10 is retired. The release includes current-session data storage without persistent database functionality.
Common starting SHA / branch / applicable members: Main, Kynan and Nikola
PG starting SHA / branch / applicable members or not applicable: N/A
Working-state review and approved integration: The working state was reviewed using git status --short, git diff, git diff --cached and git rev-parse HEAD. Tracked and untracked changes were inspected before integration to identify unfinished work and ensure that only approved changes were included in the final release candidate.
Protected common candidate and PG differences: N/A
Feature freeze / owner / verifier: Feature development will be frozen before final release verification. The team will focus on correcting genuine release blockers, completing regression testing, reviewing code quality and confirming that the submitted version matches the tested Git commit. Owner: Nikola, Verifier: Kynan


## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: [response]

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | Unit tests demonstrate that a scheduled appointment can be cancelled, its status changes to cancelled and the appointment remains retrievable using its original ID. | project/tests/ – cancellation and appointment history tests. | Kynan | Yes, if all assertions pass. | Confirm repeated cancellation and invalid cancellation are rejected. |
| Architecture responsibilities are appropriate | Code inspection demonstrates that domain classes manage their own data, SmartCareDataStore manages current-session collections, services coordinate application operations and pure query functions handle appointment selection and sorting. | project/ – domain models, datastore, services and query modules. | [response] | Pending independent inspection. | Confirm responsibilities are separated and unnecessary duplication, globals and responsibility leakage are avoided. |
| Rescheduling is safe — PG only | N/A | N/A | N/A | N/A | N/A |
| AI use is responsible — common recheck / PG assurance | N/A | N/A | N/A | N/A | N/A |
| System is maintainable | Source code inspection evaluates naming conventions, type hints, docstrings, indentation, focused methods, code duplication and separation of responsibilities. | project/ source files and Section E. | [response] | Pending final review. | Address genuine code-quality issues and document any justified decision not to make changes. |
| FR-01–03 register/find and validation | Unit tests verify patient and practitioner registration, successful lookup, input validation and handling of unknown records. | project/tests/ – patient and practitioner tests. | [response] | Pending full-suite verification. | Confirm invalid input is rejected and the application can continue operating afterwards. |
| FR-04–05 booking/conflict rules | Unit tests demonstrate successful appointment booking, rejection of appointments with the same practitioner at the same time and acceptance of appointments with different practitioners at the same time. | project/tests/ – appointment booking and conflict tests. | [response] | Pending full-suite verification. | Verify failed bookings do not create partially registered appointments. |
| FR-06–08 cancellation/history/find | Unit tests demonstrate cancellation, retained appointment history, appointment retrieval and rejection of invalid or repeated cancellation attempts. | project/tests/ – cancellation and appointment lookup tests. | [response] | Pending full-suite verification. | Verify cancelled appointments retain their original identity and remain accessible. |
| FR-09 and QRY/FP listing/filter/order/purity | Query and service tests verify appointment listing, default inclusion of all statuses, explicit status filtering, deterministic ascending date/time and ID ordering, and pure query behaviour. | project/tests/ – appointment query and practitioner listing tests. | [response] | Pending full-suite verification. | Confirm equal-time sorting, empty results versus unknown practitioners and explicit function inputs. |
| UI full console sequence and error recovery | Console demonstration verifies registration, patient and practitioner lookup, appointment booking, cancellation, appointment listing, invalid input handling and normal exit. | Section D – demonstration evidence; project/main.py. | [response] | Pending demonstration. | Run the full sequence from a new process and demonstrate recovery after invalid inputs. |
| Session-only scope / FR-10 retired | Code inspection confirms that SmartCareDataStore holds current-session records and that the application does not require persistent storage between executions. | SmartCareDataStore implementation, README and Section D. | [response] | Pending final inspection | Clearly document that records are lost when the application closes and exclude retired FR-10. |
| PG RES and assurance integration | N/A | N/A | N/A | N/A | N/A |


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | Python 3.x (teaching-team confirmed version); pinned pytest dependency | project/ – python -m pytest -q | [response] | Full common test suite executed. | [response] |
| Complete PG if applicable | N/A | N/A | N/A | N/A | N/A |
| Affected focused checks after correction | Python 3.x; pinned pytest dependency | project/ – python -m pytest -q | [response] | Relevant tests rerun following any corrective changes. Record actual result. | [response] |
| Full integrated recheck | Python 3.x; pinned pytest dependency | project/ – python -m pytest -q | [response] | Complete integrated test suite rerun following corrections. | [response] |
Prior assertions preserved / reviewed test diff: Existing test assertions were retained throughout the integration and regression process to ensure that previously verified functionality continued to meet the original requirements. The test changes were reviewed to identify any removed, modified or weakened assertions that could affect the reliability of the test suite.
Remaining failure / limitation: SmartCare currently operates using session-only data storage, meaning patient, practitioner and appointment records are not retained after the application is closed. This is a deliberate limitation of the current assignment scope rather than a failure to meet the release requirements.


## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | SmartCare is a clinic appointment management application using synthetic patient and practitioner records. | Demonstrate how the application supports clinic staff in registering patients, managing practitioners and booking appointments. | The application provides a console-based system for managing patient and practitioner records and their appointments. | project/README.md – application overview. |
| Register and find Patient and two Practitioners | Register patient P001 (Alex Smith), practitioner PR001 (Dr Taylor) and practitioner PR002 (Dr Brown). Search for P001 afterwards. | The application must allow patients and practitioners to be registered and existing patient records to be retrieved. | The patient and both practitioners were registered successfully. Searching for P001 returned the correct patient record. | Registration and patient search tests. |
| Valid booking | Book patient P001 with PR001 for 10/11/2026 at 10:00 am. | A valid appointment must be created when the patient, practitioner, date and time are valid. | Appointment A001 was successfully created and displayed with the correct patient, practitioner, date, time and scheduled status. | Appointment booking test. |
| Same practitioner exact-time conflict rejected | [response] | [response] | [response] | [response] |
| Different practitioner same time allowed | [response] | [response] | [response] | [response] |
| Cancel SCHEDULED and retain/find CANCELLED object | [response] | [response] | [response] | [response] |
| Invalid/repeated cancellation rejected | [response] | [response] | [response] | [response] |
| Default all-status listing | [response] | [response] | [response] | [response] |
| Explicit filtering / empty vs unknown / deterministic order | [response] | [response] | [response] | [response] |
| Invalid date/status/menu/lookup recovery and continued operation | [response] | [response] | [response] | [response] |
| Session-only limitation and normal exit | [response] | [response] | [response] | [response] |
| One meaningful requirement-linked pytest test explained | [response] | [response] | [response] | [response] |
| Architecture and one actual AI decision / known limitation | [response] | [response] | [response] | [response] |
| PG reschedule identity/participants/time and no-op | N/A | N/A | N/A | N/A |
| PG conflict/invalid status/failure non-mutation | N/A | N/A | N/A | N/A |
| PG old slot / current lookup/list ordering / assurance risks | N/A | N/A | N/A | N/A |
Stable demo owner / fresh process / command: [response]
PG demonstrations through service/tests or not applicable: [response]


## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | [response] | [response] | [response] |
| PascalCase and snake_case naming | [response] | [response] | [response] |
| Useful type hints and meaningful docstrings | [response] | [response] | [response] |
| Four-space indentation and imports/layout | [response] | [response] | [response] |
| Focused methods / duplication / dead or commented code | [response] | [response] | [response] |
| Globals / leakage / unnecessary inheritance or frameworks | [response] | [response] | [response] |
| No SQLite/persistence/repository ABCs/speculative features | [response] | [response] | [response] |
| Synthetic data / secrets / dependencies / provenance | [response] | [response] | [response] |
| Significant common Copilot contributions and human verification | [response] | [response] | [response] |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | [response] | [response] | [response] |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] |
Access route or approved equivalent / limitations: [response]
Available AI evidence and missing evidence honestly disclosed: [response]


## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | [response] | [response] | [response] |
| Out-of-scope capabilities and known limitations | [response] | [response] | [response] |
| Confirmed teaching Python version and dependency installation | [response] | [response] | [response] |
| Working directory / demo / interactive / test commands | [response] | [response] | [response] |
| Repository structure and architecture responsibilities | [response] | [response] | [response] |
| Responsible AI summary / synthetic-data rule | [response] | [response] | [response] |
| Release label/version and SHA links | [response] | [response] | [response] |
Root README index and project/README verified: [response]
Fresh clone or extracted ZIP / candidate identity: [response]
Verifier and clean environment / actual version: [response]
Setup/run/test commands and observed results: [response]
Missing local file or setup gap / remedy and recheck: [response]


## G Known limitations debt and release notes

Delivered features: [response]
Important fixes: [response]
Architecture/quality improvements: [response]
Known limitations: [response]
AI-assisted development note: [response]

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] |
Session-only synthetic data and minute-precision local time: [response]
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: [response]
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: [response]
Difference between accepted scope limit and unresolved required behaviour: [response]
PG assurance residual risks / owner / status or not applicable: [response]


## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] | [response] | [response] |
Justified no-change conclusion if no defect found: [response]
Release blockers still open / status: [response]


## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: [response]
Independent reviewer / feedback / response: [response]
Integration commit / full recheck: [response]
Tracked and untracked file inspection / cleanliness: [response]
Secrets/staff material/caches/tool-metadata exclusion check: [response]
Candidate recovery plan / known-good SHA: [response]
Named substantive contributions: [response]


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: [response]
Approver / date / rationale and evidence: [response]
What risks remain / conditions / owners: [response]
Can the team explain the system: [response]
Can a change be recovered: [response]
Common decision / PG decision where different: [response]


## K Final tested release SHA

Exact common tested SHA: [response]
Exact PG tested SHA or not applicable: [response]
Final submitted SHA / repository URL: [response]
Evidence-only later commit and difference explanation: [response]
Executable changes after testing and re-verification: [response]
Source ZIP name / SHA correspondence / extracted comparison: [response]


## L Submission package verification

- [ ] Feature freeze and scoped requirements traced.
- [ ] Applicable full regressions, integrated demo and invalid paths verified.
- [ ] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [ ] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [ ] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [ ] project/ source and all accumulated applicable tests included.
- [ ] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [ ] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ ] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [ ] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: [response]
Deadline/timezone: [response]
Repository access arrangement: [response]
Mixed-candidate upload arrangement: [response]
Oral/video recording/accessibility arrangements: [response]
Remaining administration or release dependency: [response]


## M Formative questions

1. What is a release candidate? [response]

2. What is feature freeze and why is it used? [response]

3. What is regression testing in a release context? [response]

4. What is a known limitation? [response]

5. What is technical debt? [response]

6. What are release notes? [response]

7. What is software maintenance? [response]

8. What is the purpose of the individual demonstration/viva? [response]

9. What should the final responsible-AI check establish before release? [response]

10. What is the main course conclusion about AI and the role of the software engineer? [response]


## N Reflection viva and handover

Strongest evidence SmartCare is ready: [response]
Weakest area: [response]
How AI use changed from Stage 1 to Stage 12: [response]
Start doing — engineering and AI use: [response]
Stop doing — engineering and AI use: [response]
Continue doing — engineering and AI use: [response]
What worked / caused rework / future delivery improvement: [response]
One paragraph — If AI can write code why do we still need software engineers: [response]

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | [response] |
| Two requirements and acceptance criteria | [response] |
| Domain model and architecture | [response] |
| Design trade-off | [response] |
| Meaningful test and its limits / 100 percent coverage | [response] |
| Diagnosed defect and verification | [response] |
| Shared store and session-state/query responsibilities | [response] |
| What would break if session-state lookup/query responsibilities changed? | [response] |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | [response] |
| FR-07 retained history test | [response] |
| Actual AI change rejected/modified or honestly accepted with verification | [response] |
| Unresolved limitation / future production work | [response] |
| Personal implementation contribution | [response] |
| Personal test/review/design/integration contribution | [response] |
| PG agentic change and rescheduling verification | [response] |
| PG responsible-AI risk/remediation or supported no finding | [response] |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: [response or not undertaken]
Separate reflection / peer / common team viva evidence links and routing: [response]
No further coding stage. Later corrections use the published assessment process.
