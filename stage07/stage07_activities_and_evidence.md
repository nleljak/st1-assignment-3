# Stage 7 Testing and Verification Record

Group/tutorial: Online Group 2, Tuesday 17:30 Members/cohorts: Nikola, Kynan UG
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | Register a patient with a valid and unused ID. | Unsuccessful registration of a patient via a patient ID | Positive: The registered patient can be retrieved from the data store and the stored patient has the expected ID and details. Negative: A ValueError is raised and the original patient record remains unchanged. |
| FR-05 Prevent practitioner conflict | Book appointments for two different practitioners at the same time and day. | Unsuccessful booking of two different practitioners at the time and date. | Positive: Both appointments are accepted and associated with their respective practitioners. Negative: A ValueError is raised, and the rejected appointment is not added to the data store. |
| FR-06 Cancel appointment | Appointment was successfully removed from the appointment schedule | Appointment was unsuccessfully removed from the appointment schedule | Positive: The appointment's status changes to CANCELLED. Negative: A ValueError is raised, and the appointment remains CANCELLED. |
| FR-07 Retain cancelled history | Cancel an appointment, then retrieve it by its ID or list the appointments. | Attempt to retrieve a genuinely unknown appointment ID. | Positive: The cancelled appointment remains retrievable, with its status still CANCELLED. Negative: The service lookup raises a LookupError for an unknown appointment ID. |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: Weak  Why: This always passes, regardless of whether the software behaves correctly. It does not verify any requirement or expected outcome.

`assert appointment is not None`
Judgement: Weak Why: This only checks that an appointment object exists. It does not establish that it belongs to the correct patient or practitioner, has the correct date and time, or has the expected status.

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: Strong  Why: This checks the specific observable outcome of cancellation: the appointment status is Cancelled. It does not, by itself, prove that the appointment remains retrievable from the data store.

`assert len(results) > 0`
Judgement: Weak  Why: This only checks that a collection contains at least one result. It does not prove that the correct appointment is present or that cancelled appointments are retained.

`assert data_store.find_appointment('A1') is appointment`
Judgement: Strong  Why: This checks that looking up appointment A1 returns the exact expected appointment object. It supports the requirement that the appointment remains retrievable, but does not by itself prove that its status is Cancel.

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract: [response]

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | Checks appointment is not None | Only proves an object exists; it does not prove the appointment was booked correctly. | Book an appointment with registered participants and assert that it has the expected ID, patient, practitioner and SCHEDULED status, and is stored in the data store.
| 2 | Checks another object is not None | Does not establish that the correct patient or practitioner was returned. | Register a patient, look them up using their ID, and assert that the returned object is the same patient that was registered.
| 3 | Uses assert True | Always passes, even if the required behaviour is broken. | Attempt to cancel a scheduled appointment and assert that its status changes to CANCELLED.
| 4 | Assumes an SMS notification is sent after booking | SMS notifications are not part of the stated requirements, so this test invents functionality. | After booking, assert that the appointment is stored and has the correct details and status.
| 5 | Assumes an SMS notification is sent after cancellation | SMS notifications are not part of the stated requirements, so this test does not verify the required cancellation behaviour. | Cancel a scheduled appointment and assert that it becomes CANCELLED and remains retrievable in the data store.

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
Code coverage measures which lines or branches of code are executed and not whether the tests correctly verify the needed behaviour. A test might execute a cancellation function but only use assert True. The code is covered, but the test does not prove that the appointment was actually cancelled.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| FR-01 Register patient | AC-01.1 | Test-01 | Positive — service | Patient registration test — tests/test_services.py | Valid patient details and a unique ID result in a patient being stored. | Not yet verified | Student Authorised |
| FR-05 Prevent practitioner conflict | AC-04.1 | Test-02| Negative — service | test_conflict_rule_and_different_practitioner — tests/test_services.py | Rejects a second scheduled appointment for the same practitioner at the exact same time. | Verified | Supplied from stage 6 |
| FR-06 Cancel appointment | AC-05.1 | Test-03 | Positive — domain | test_domain_cancellation_and_guard — existing Stage 6 test file | Cancelling a scheduled appointment changes its status to CANCELLED. | Verified | Supplied from stage 6 |
| FR-07 Retain cancelled history | AC-05.2 | Test-04 | Positive — service | Cancellation/history test — tests/test_services.py | A cancelled appointment remains retrievable during the current session. | Verified | Supplied from stage 6 |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| Test-C01 | Patient construction | Supporting domain contract | positive | test_patient_construction() | Valid patient ID and name are stored correctly. | Verifies stored field values, not just successful construction. |
| Test-C02 | Patient validation | Blank-ID validation contract | Negative | test_patient_blank_id_rejected() | Blank patient ID raises ValueError. | Preserves the required reference-test intention; adds a descriptive test name. |
| Test-C03 | Patient validation | Required-name validation contract | Boundary | test_patient_blank_name_rejected() | Whitespace-only patient name raises ValueError. | Adds explicit coverage of whitespace-only names. |
| Test-C04 | Practitioner construction | Supporting domain contract | Positive | test_practitioner_construction() | Practitioner ID, name and specialty are stored correctly. | Verifies all required practitioner fields. |
| Test-C05 | Practitioner validation | Blank-ID validation contract | Negative | test_practitioner_blank_id_rejected() | Blank practitioner ID raises ValueError. | Adds explicit practitioner ID validation coverage. |
| Test-C06 | Practitioner validation | Required-name validation contract | Boundary | test_practitioner_blank_name_rejected() | Whitespace-only practitioner name raises ValueError. | Adds explicit whitespace-only name validation coverage. |
| Test-C07 | Practitioner validation | Required-specialty validation contract | Boundary | test_practitioner_blank_specialty_rejected() | Whitespace-only specialty raises ValueError. | Adds explicit specialty validation coverage. |
| Test-C08 | Appointment construction | Supporting domain contract | Positive | test_appointment_construction() | Appointment ID, patient, practitioner and date/time match the supplied values.] | Verifies appointment fields and that the actual participant objects are retained. |
| Test-C09 | Appointment status | AC-05.1 is not applicable to initial status; supporting domain contract | Positive | test_new_appointment_starts_scheduled() | A new appointment has status AppointmentStatus.SCHEDULED. | Preserves the required reference-test intention. |
| Test-C10 | Appointment cancellation | AC-05.1 | Positive | test_cancellation_changes_status() | Cancelling a scheduled appointment changes its status to CANCELLED. | Preserves the cancellation reference-test intention with an explicit status assertion. |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| Test-D01 | Create a fresh data store and PatientService. | Register patient "P1" with name "Alex Example". | Assert the patient can be retrieved and is the same object returned by registration. | Proves successful patient registration stores the correct patient. |
| Test-D03 | Register patient "P1" and create a PatientService. | Look up "P1", then look up "UNKNOWN". | Assert the first lookup returns the registered patient and the second raises LookupError. | Proves both successful and unsuccessful patient lookups behave correctly. |
| Test-D04 | Create a fresh data store and PractitionerService. | Register practitioner "D1", then attempt to register another practitioner with ID "D1". | Assert the original practitioner is retrievable; use pytest.raises(ValueError) for the duplicate and verify the original details remain unchanged. | Proves practitioner registration works and duplicate IDs are rejected safely. |
| Test-D07 | Register a patient and two practitioners. Book "A1" with practitioner "D1" at a specific time. | Attempt another booking with "D1" at that time, then book with "D2" at the same time. | Assert the conflicting booking raises ValueError, the original remains unchanged, and the different-practitioner booking succeeds. | Proves the conflict rule rejects same-practitioner clashes without blocking valid bookings with another practitioner. |
| Test-D09 | Book appointment "A1" and retain its ID. | Cancel it, retrieve it again, and attempt to cancel it a second time. | Assert its status becomes CANCELLED, it remains retrievable, and repeated cancellation raises ValueError without changing its status. | Proves cancellation, appointment history retention and rejection of repeated cancellation. |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| Test-C01 | test_domain.py / test_patient_construction | [complete] | [complete] |
| Test-C02 | test_domain.py / test_patient_blank_id_rejected | [complete] | [complete] |
| Test-D01 | test_services.py / patient registration test | [complete] | [complete] |
| Test-D05 | test_services.py / appointment booking test | [complete] | [complete] |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| Test-F01 | Register a patient and verify the patient is stored. | AC-01.1 — valid patient data with an unused ID is stored. | test_services.py / patient registration test — confirm function name | [complete] |
| Test-F02 | Reject duplicate patient registration and preserve the original patient. | AC-01.2 — duplicate patient ID rejected. | test_services.py / test_duplicate_patient_preserves_original() if present | [complete] |
| Test-F03 | Find a registered patient. | AC-02.1 — registered patient lookup succeeds. | test_domain.py or test_services.py / test_find_patient() | [complete] |
| Test-F04 | Reject lookup of an unknown patient. | AC-02.2 — unknown patient lookup is rejected. | test_domain.py or test_services.py / test_find_unknown_patient() | [complete] |
| Test-F05 | Register a practitioner and verify the practitioner is stored. | Practitioner registration requirement — confirm the exact criterion in your handout. | test_services.py / practitioner registration test — confirm function name | [complete] |
| Test-F06 | Reject duplicate practitioner registration and preserve the original. | Practitioner duplicate-ID requirement — confirm the exact criterion in your handout. | test_services.py / test_duplicate_practitioner_preserves_original() if present | [complete] |
| Test-F07 | Book an appointment with registered participants and verify its scheduled status. | AC-03.1 — appointment is stored with scheduled status. | test_services.py / test_registration_and_booking() if present | [complete] |
| Test-F08 | Reject booking with an unknown participant without storing an appointment. | AC-03.2 — unknown participant rejected. | test_services.py / test_unregistered_participants_rejected() if present | [complete] |
| Test-F09 | Reject a conflicting booking but allow another practitioner at the same time. | AC-04.1 / AC-04.2 — same-practitioner conflict rejected; different practitioner allowed. | test_services.py / test_conflict_rule_and_different_practitioner() if present | [complete] |
| Test-F10 | Cancel an appointment and verify its cancelled status and retained history; reject repeated cancellation. | AC-05.1 / AC-05.2 / AC-05.3 — cancellation, history retention and repeated-cancellation rejection. | test_services.py / cancellation test — confirm function name | [complete] |
| Test-F11 | Retrieve an appointment by ID. | AC-06.1 — known appointment lookup succeeds. | test_services.py / appointment lookup test — confirm function name | [complete] |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| Reject blank patient ID/Name | Patient ID/Name is " " | ValueError is raised; no patient is registered. | Test-C02 |
| Reject blank practitioner specialty | Specialty is "   " | ValueError is raised | Test-C07 |
| Reject duplicate patient registration | Register "P1", then register another patient with ID "P1" | ValueError is raised; original patient remains stored with the original details. | Test-D02 |
| Reject unknown patient lookup | Search for patient ID "UNKNOWN" | LookupError is raised. | Test-D03 |
| Reject booking with an unknown participant | Attempt to book using an unregistered patient ID | LookupError is raised; no appointment is stored. | Test-D06 |
| Reject conflicting appointment | Book two appointments with the same practitioner at the exact same time | ValueError is raised; original appointment remains unchanged. | test-D07 |
| Reject repeated cancellation | Cancel an appointment, then cancel it again | ValueError is raised; status remains CANCELLED. | test-D09 |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: Appointment booking must prevent conflicting appointments for the same practitioner.
Acceptance criterion: AC-04.1 — A booking for the same practitioner at the exact time as an existing scheduled appointment is rejected.
Behaviour to test: The service must reject a second appointment with the same practitioner at the same date and time, while preserving the original appointment.
Human-first test idea/categories: Book an appointment with a registered patient and practitioner at an available time. Check that the appointment is stored and has AppointmentStatus.SCHEDULED.
Prompt and purpose: (https://github.com/nleljak/st1-assignment-3/blob/main/project/tests/test_starter.py)

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: Create an appointment, then attempt a second booking with the same practitioner at the same time. Expect ValueError.
- What it claims to verify: Conflicting appointments for the same practitioner are rejected.
- Requirement trace: AC-04.1 — same-practitioner, same-time booking is rejected.
- Assertion quality: Checking pytest.raises(ValueError) verifies rejection, but by itself does not prove that the original appointment remains unchanged.
- Human critique: The candidate is relevant, but it needs an additional assertion to verify that the original booking is still stored and its details have not changed.
- Decision: Accept
- Reason: The test should verifies the existing state.
- Final test reference if accepted/modified: project/tests/test_services.py / test_conflict_rule_and_different_practitioner() (if this existing test covers the behaviour).
- Actual verification result: Not run as part of this illustrative example.

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? The test that attempted to book a second appointment with the same practitioner at the same time and checked that ValueError was raised.
Why was it weak? The test checked that the conflicting booking was rejected, but it did not verify that the original appointment remained stored and unchanged. Therefore, it did not provide sufficient evidence that the rejected operation preserved the existing data.
How did you strengthen it? I strengthened the test by checking that ValueError was raised when the conflicting booking was attempted, then asserting that the original appointment remained retrievable and that its date, time and status were unchanged. These assertions verify both the rejection and the preservation of the original appointment.
Accepted / modified / rejected test decisions and evidence: I strengthened the test by checking that ValueError was raised when the conflicting booking was attempted, then asserting that the original appointment remained retrievable and that its date, time and status were unchanged. These assertions verify both the rejection and the preservation of the original appointment.

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

Individual test runs and changed-order independence evidence: [commands, results, links]
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? [response]
Coverage if used: [result or not used]
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? [response]
Optional fixtures/parametrisation used and why, if any: [response or not used]

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| Kynan | Part A-O | Commit history |

## N Formative Questions

1. What question does verification answer?
Verification checks whether the software meets its specified requirements and technical specifications.

2. What question does validation answer?
Validation checks whether the software meets user needs and is fit for its intended purpose.

3. What is a unit test?
A unit test checks a small, individual part of a program, such as a function or method, to confirm that it behaves as expected

4. What is a pytest fixture?
A pytest fixture provides reusable setup or resources for tests, such as creating a fresh data store and registering a patient and practitioner before each test.

5. What is parametrisation in pytest?
Parametrisation allows the same test to run with multiple inputs and expected outcomes, reducing repeated code and helping test different cases consistently.

6. What is regression testing?
Parametrisation allows the same test to run with multiple inputs and expected outcomes, reducing repeated code and helping test different cases consistently.

7. What does code coverage tell us, and what does it not prove?
Code coverage indicates how much of the code was executed during testing. It does not prove that the code is correct or that the tests adequately check the expected behaviour.

8. What makes an assertion weak?
An assertion is weak when it does not adequately verify the required outcome. For example, checking only that an exception is raised does not confirm that the original data remains unchanged after the operation fails.

10. What is the appropriate role of GitHub Copilot as a test assistant?
GitHub Copilot can suggest test cases, edge cases and assertions, but its suggestions must be reviewed and tested by a person. The developer remains responsible for checking that tests match the requirements and genuinely detect incorrect behaviour.

11. What is the Stage 7 engineering rule?
GitHub Copilot can suggest test cases, edge cases and assertions, but its suggestions must be reviewed and tested by a person. The developer remains responsible for checking that tests match the requirements and genuinely detect incorrect behaviour.

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
