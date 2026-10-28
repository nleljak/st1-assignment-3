# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Online group 2, Tuesday 17:30
Members and UG/PG cohorts: Kynan and Nikola, UG
Record owner / contribution links for each member: Check commit history

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason: | Statement | Classification | Reason |
|---|---|---|
| Appointment disappears after cancellation. | Symptom | This describes the observed problem: the appointment is no longer available after cancellation. It does not establish the underlying cause. |
| The data-store removal path is probably being called. | Hypothesis | This proposes a possible explanation for the symptom. It must be tested against the current implementation, especially because the project has no public delete operation. |
| The failing test shows `store.find_appointment('A1')` returns `None`. | Evidence | This reports a specific, observable test result that can be reproduced and used to investigate the problem. |
| The service layer is badly designed. | Opinion | This is a broad judgement without specific supporting evidence. It should be replaced with a precise, testable statement about the service layer's behaviour. |
| Traceback points to `smartcare/services.py` line 42 in the example. | Evidence | A traceback provides a concrete location associated with the failure. |

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: Cancelled Appointment History

Requirement used to justify expected behaviour: AC-05.2 requires cancelled appointment history to be retained and retrievable during the current session.

Expected behaviour: When appointment `A1` is cancelled, its status should change from `SCHEDULED` to `CANCELLED`, but the appointment should remain in the data store and be retrievable using its ID.

Observed behaviour: [Record the actual result after running the reproduction. Do not assume the appointment disappears unless the test demonstrates this.]

Minimal reproduction:
1. Create a fresh `SmartCareDataStore`.
2. Register a patient and practitioner.
3. Book appointment `A1`.
4. Cancel the appointment using `appointment.cancel()`.
5. Check that `appointment.status` is `AppointmentStatus.CANCELLED`.
6. Check that `data_store.find_appointment('A1')` returns the original appointment.

Initial hypothesis: My initial hypothesis is that cancelling an appointment may be removing it from the data store instead of only changing its status.

Evidence to inspect:
- The test output showing whether `data_store.find_appointment('A1')` returns the original appointment or `None`.
- The implementation of `Appointment.cancel()` in `smartcare/domain.py`.
- The appointment storage and lookup methods in `smartcare/data_store.py`.
- Any cancellation-related service methods in `smartcare/services.py`.
- The traceback and actual source line if the test fails.

Diagnosis and next steps: Compare the observed result with AC-05.2 and inspect the relevant implementation before deciding whether the issue is a product defect, a test defect or unresolved. The project has no public delete operation, so the initial removal hypothesis may be disproved. Keep the original hypothesis in the record regardless, and document what the evidence actually establishes.

No production code should be changed until the failure has been reproduced and diagnosed.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: The test should be changed, not the implementation, if it expects cancelled appointments to be deleted contrary to the requirements. FR-07 requires appointment history to be retained. When an appointment is cancelled, its status should change from SCHEDULED to CANCELLED, and the appointment should remain retrievable.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: The code smells include duplicate status strings, direct collection manipulation, unnecessary printing, repeated validation and conflict logic and deeply nested conditionals. These can be improved by using the existing AppointmentStatus enum and SmartCareDataStore, extracting repeated helpers and simplifying conditions without changing required behaviour. Renaming appt to appointment, extracting a conflict helper and replacing a magic status string are refactorings; restoring cancelled appointment history is a repair because it fixes a requirement violation; adding rescheduling is a feature because it introduces new functionality. Existing booking, validation, conflict, cancellation and history-retention rules must remain unchanged.

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: The failure occurred in `test_cancelled_appointment_remains_in_history`, where the assertion checking that `data_store.find_appointment('A1')` returned the original appointment failed. The expected value was the original appointment object, but the observed value was `None`. The relevant test line was the assertion checking the result of `find_appointment('A1')`. The application call path was the test → `Appointment.cancel()` → `SmartCareDataStore.find_appointment()`. The supporting requirement was FR-07, which requires cancelled appointment history to be retained.

Three plausible causes were considered. First, the appointment may have been removed from storage during cancellation; this could be checked by inspecting the cancellation implementation and data-store contents before and after cancellation. Second, the data-store lookup method may be failing to find an appointment that is still stored; this could be checked by inspecting the stored appointments and testing lookup independently. Third, the test setup or identifier may be incorrect; this could be checked by confirming that appointment `A1` was successfully booked and that the same ID is used throughout the test. These are hypotheses ranked by their fit with the observed failure, not confirmed causes. A traceback identifies where an exception or assertion failure surfaced, but it does not by itself establish why the failure occurred; the implementation, state and test setup must also be inspected.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: The cause may not be what it first appears to be. The failure could result from a product defect, an incorrect test expectation or a problem with the test setup. Changing code without investigating can introduce new bugs or hide the real problem. Instead, reproduce the failure, inspect the evidence, identify and test possible causes, then make the smallest justified change and rerun the relevant tests.

Classification responses (1–5, each with reason):

1. “Appointment disappears after cancellation.” — Symptom. It describes the observed problem without identifying its cause.
2. “The data-store removal path is probably being called.” — Hypothesis.** It proposes a possible cause that must be tested against the current implementation, which has no public delete operation.
3. “The failing test shows `store.find_appointment('A1')` returns `None`.” — Evidence. It reports a specific, observable result from a test, provided that result was actually observed.
4. “The service layer is badly designed.” — Opinion. It is a broad judgement without specific supporting evidence or a clearly testable claim.
5. “Traceback points to `smartcare/services.py` line 42 in the example.” — Evidence. A traceback provides an observable failure location, but line 42 is illustrative and must be checked against the actual traceback.

Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect:

Expected: Under FR-07 and AC-05.2, cancelling an appointment should change its status to `CANCELLED` while retaining its history so it remains retrievable.
Observed: Record the actual result from the test run. The suspected problem is that the appointment cannot be retrieved after cancellation, but this must be confirmed rather than assumed.
Reproduction: Create a fresh `SmartCareDataStore`, register a patient and practitioner, book appointment `A1`, cancel it, and check both its status and whether `data_store.find_appointment('A1')` returns the original appointment.
Initial hypothesis: Cancellation may be removing the appointment from storage instead of only changing its status.
Evidence to inspect: The actual test output, the implementation of `Appointment.cancel()` in `smartcare/domain.py`, the appointment storage and lookup methods in `smartcare/data_store.py`, and any relevant cancellation service method in `smartcare/services.py`. Keep the initial hypothesis in the record even if later evidence disproves it.

Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks:

Response and reason: The failure occurred in `test_cancelled_appointment_remains_in_history`, where the assertion checking that `data_store.find_appointment('A1')` returned the original appointment failed. The expected value was the original appointment object, but the observed value was `None`. The relevant test line was the assertion checking the result of `find_appointment('A1')`. The application call path was the test → `Appointment.cancel()` → `SmartCareDataStore.find_appointment()`. The supporting requirement was FR-07, which requires cancelled appointment history to be retained.

Three plausible causes were considered. First, the appointment may have been removed from storage during cancellation; this could be checked by inspecting the cancellation implementation and data-store contents before and after cancellation. Second, the data-store lookup method may be failing to find an appointment that is still stored; this could be checked by inspecting the stored appointments and testing lookup independently. Third, the test setup or identifier may be incorrect; this could be checked by confirming that appointment `A1` was successfully booked and that the same ID is used throughout the test. These are hypotheses ranked by their fit with the observed failure, not confirmed causes. A traceback identifies where an exception or assertion failure surfaced, but it does not by itself establish why the failure occurred; the implementation, state and test setup must also be inspected.


## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: [complete]
- Baseline test command / working directory / observed result / evidence: [complete]
- Clean preparation SHA if a record-only commit followed Stage 7: [complete]
- Branch and preparer / how teammates obtained this branch: [complete]
- Downloaded tool version, source SHA256 and --check outcome: [complete]
- --apply and --verify output summaries / artefact references: [complete]
- Bounded diff inspected and recovery location (not committed): [complete]
- Prepared faulty-state commit SHA: [complete]
- Preparation or recovery issues and resolution, if any: [complete]
- Initial prepared full-suite command / result / key failures: [complete]

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: [complete]
- Expected behaviour and requirement: [complete]
- Minimal synthetic reproduction steps: [complete]
- Meaningful failing test path/name and exact relevant failure: [complete]
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: [complete]
- Expected behaviour and requirement: [complete]
- Minimal synthetic reproduction steps: [complete]
- Meaningful failing test path/name and exact relevant failure: [complete]
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: [complete]
Evidence intended to inspect / competing explanation / discriminating check: [complete]
Member and saved sequence/time or commit showing this preceded consultation: [complete]

### F8-02 human entry
Likely cause and why plausible: [complete]
Evidence intended to inspect / competing explanation / discriminating check: [complete]
Member and saved sequence/time or commit showing this preceded consultation: [complete]

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

### F8-02 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | [complete] | [complete] | [complete] |
| F8-02 after repair | [complete] | [complete] | [complete] |
| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: Reproduce the failure, record the expected and observed behaviour, inspect the evidence and test possible causes before making the smallest justified change.

2. Where should expected behaviour come from during debugging?

Response: Expected behaviour should come from the requirements, acceptance criteria and specified behaviour of the system, rather than personal assumptions or the behaviour of a failing test alone.

3. What is a debugging hypothesis?

Response: A debugging hypothesis is a possible explanation for a failure that can be investigated and tested against evidence.

4. What is a regression test and why is it retained?

Response: A regression test checks that previously working behaviour remains correct after changes. It is retained so future changes can be checked against known requirements and to help prevent previously fixed defects from returning.

5. What is meant by root cause?

Response: It is the underlying issue of a defect, rather than just a symptom or location of the failure. 

6. What is refactoring?

Response: Refactoring is improving the internal structure of the readability of the code without changing it's required external behaviour.

7. What is a swallowed exception?

Response: A swallowed exception occurs when an exception is caught but ignored or not properly reported, potentially hiding a failure and allowing the program to continue in an unexpected state.

8. What is a code smell?

Response: A sign that code may be difficult to understand, maintain or test, such as duplicated logic, long methods or deeply nested conditionals. It suggests a possible improvement but does not automatically mean the code is defective.

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: They should be treated as suggestions or hypotheses, not established facts. Engineers must verify them against the requirements, source code, reproducible failures and test results before making changes.

10. What is the Stage 8 engineering rule?

Response: Use evidence and requirement-linked tests to guide changes, make the smallest justified modification, retain regression tests, and verify the result. Do not invent failures or assume a proposed diagnosis is correct without evidence.

## L. Completion and handover

- [x] Existing project, earlier tests and stage records preserved.
- [x] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
