# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: Online group 2
Members and responsibilities: Kynan and Nikola, both have the same responsibilities
Stage 8 integrated SHA, command, working directory and actual result: <!-- complete -->

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity | Required session/domain state | The system must retain registered patient details so patients can be identified and linked to appointments. |
| Appointment history | Required session/domain state | Appointment records must remain available during the session, including cancelled appointments. |
| Temporary menu choice | Transient state | The menu choice is only needed to determine which action the user wants to perform. |
| Practitioner specialty | Required session/domain state | Practitioner specialty is part of the practitioner's registered information. |
| Debug print output | Transient state | Debug messages are not required application data and do not need to be retained. |
| Appointment status | Required session/domain state | The system must track whether an appointment is scheduled, cancelled or completed. |

What is intentionally lost on exit? All session data, including patient and practitioner records, appointment details and appointment history, is intentionally lost when the application exits. The application uses in-memory storage only, and permanent data persistence is outside the scope of Stage 9.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | appointment: Appointment | Tuple: (datetime, str) | Returns the appointment's date/time and appointment ID to provide deterministic sorting. No additional validation required because it receives a valid Appointment object. | Uses Appointment.date_time and Appointment.appointment_id. |
| select_appointments | appointments: list[Appointment], practitioner_id: str, status: AppointmentStatus \| None = None | New list[Appointment], sorted in ascending order | Filters appointments by practitioner ID and optional status. Returns all statuses if status is None. Must not modify the original list or appointment objects. | Uses Appointment.practitioner.practitioner_id, Appointment.status and AppointmentStatus. |
| Service listing | practitioner_id: str, status: AppointmentStatus \| None = None | list[Appointment] | Checks that the practitioner exists and that the supplied status is valid. Retrieves appointments from the data store and passes them to select_appointments(). | Uses SmartCareDataStore and existing practitioner lookup and status constraints. |
| Console | User-entered menu choice and relevant text inputs (str) | Displays information and messages; invokes service operations | Handles user input, converts date/time and status values, calls services, displays results and recovers from expected errors such as ValueError and LookupError. | Uses existing services, parse_date_time() and format_appointment(). |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: The existing domain classes enforce local validation rules when objects are created. The data store enforces uniqueness and checks that appointment participants are the actual registered objects. Appointment cancellation is controlled by the domain object, which only allows appointments with scheduled status to be cancelled. These existing contracts should be reused rather than duplicated in the console or query functions.

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | Domain logic is incorrectly handling user interaction. | The console should collect user input. Appointment.cancel() should only enforce the domain rule that an appointment can be cancelled if its status is SCHEDULED. |
| Service prints/reads the menu | The service is handling presentation and user interaction instead of coordinating application operations. | The console should display menus and collect input. The service should coordinate domain objects and data-store operations. |
| Query sorts its source in place | The query is modifying the supplied collection, creating an unwanted side effect and violating its pure-function responsibility. | The query should return a new sorted list without modifying the original collection or appointment objects. |
| Store prints Appointment saved | The data store is handling user-facing output instead of managing in-memory records. | The console should display confirmation messages. The data store should only manage storage, retrieval and relevant data integrity constraints. |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: appointments.sort(key=appointment_sort_key) sorts the original list in place, meaning the source order changes. It returns None, so it does not create a separate list.
result = sorted(appointments, key=appointment_sort_key) creates and returns a new sorted list. The original list remains in its original order. The returned list is a different list object, although it contains references to the same Appointment objects.
A meaningful mutation check is to save a copy of the original list before sorting, then compare the original list with that copy afterwards. For sorted(), also check that result is not appointments and that the objects inside the result are the same objects as those in the source list.

Score-example prediction and explanation of passing the named key: The expected score is that the appointments are ordered by date/time first and appointment ID second. Passing appointment_sort_key to either sorting function tells Python to use the returned (date_time, appointment_id) tuple as the sorting value. This provides consistent ordering when two appointments have the same date and time. Using the named key also avoids duplicating sorting logic throughout the application.

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and scheduled-only exclusion: Cancellation changes an appointment's status from scheduled to cancelled, while deletion removes the appointment record entirely. SmartCare uses cancellation rather than deletion so appointment history remains available.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: <!-- response -->

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| QRY-01 Practitioner filtering | Appointment list and practitioner ID | select_appointments() filters by practitioner ID. | Only appointments belonging to the specified practitioner are returned. | Test appointments belonging to multiple practitioners and check isolation. |
| QRY-02 Status filtering | Appointment list and optional AppointmentStatus | select_appointments() filters by status when supplied. | None returns all statuses; an explicit status returns only matching appointments. | Test scheduled, cancelled, completed and no-match results. |
| QRY-03 Deterministic sorting | Appointment list | appointment_sort_key() and select_appointments() sort by date/time and appointment ID. | New list returned in ascending order, including correct tie-breaking. | Test different dates and equal-time appointments with different IDs. |
| FP-01 Query purity | Same appointment list and filter arguments | select_appointments() uses explicit inputs without accessing global state or performing I/O. | Repeated calls with unchanged inputs produce equivalent results without side effects. | Repeat query and compare results and source data. |
| FP-02 Source preservation | Original appointment list | select_appointments() returns a new list without modifying source data. | Original list order and appointment objects remain unchanged. | Check list identity, source order and object fields before and after. |
| FP-03 Named sorting key | Appointment objects | appointment_sort_key() supplies the sorting tuple. | Sorting uses (date_time, appointment_id). | Test the key directly and verify query ordering. |
| QRY-04 Service validation | Practitioner ID, optional status and data-store appointments | AppointmentService.list_practitioner_appointments() validates inputs, retrieves records and calls the query function. | Unknown practitioner raises LookupError; invalid status raises ValueError; valid practitioner with no matches returns an empty list. | Service tests for valid, unknown and invalid inputs. |
| UI-01 Interactive workflow | Patient, practitioners, appointments and menu choices | Console calls the relevant services to register, book, cancel, find and list records. | Operations work correctly, including practitioner conflict rejection and cancellation history. | Console demonstration with the required booking and cancellation sequence. |
| UI-02 Invalid input recovery | Invalid menu choices, IDs, dates, statuses and duplicate registrations | Console handles expected errors and returns to the menu. | Useful error message appears, application continues and rejected operations do not partially change stored data. | Console test using invalid inputs followed by a successful operation. |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: Listed above

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| | | | | |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: <!-- response -->
What the tests do and do not establish: <!-- response -->

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | | | | |
| UI-02 invalid-input recovery | | | | |
| Automated service workflow | | | | |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: <!-- paste or accessible reference -->
Actual response: <!-- accessible reference -->

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| | | | | | |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: <!-- response -->

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- response -->
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? <!-- response -->
2. Which explicit inputs are needed, and why avoid a global store? <!-- response -->
3. How can a new list reuse Appointment objects safely? <!-- response -->
4. Why use a named key, and what breaks equal-time ties? <!-- response -->
5. How do default and explicit status filters differ? <!-- response -->
6. How do empty, unknown practitioner and invalid filter cases differ? <!-- response -->
7. Which console errors recover, and how is unchanged state checked? <!-- response -->
8. What is data integrity for registered participants, conflicts and history? <!-- response -->
9. What is Copilot's review role, and who verifies findings? <!-- response -->
10. How do pure functions and OOP responsibilities work together? <!-- response -->

## H. Review, completion and common handover

Issues and bounded branches: <!-- links -->
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: <!-- links -->
Integrated common Stage 9 SHA: <!-- complete -->
Full regression command, working directory, actual count/result and evidence: <!-- complete -->
README run instructions and scope/limitations: <!-- link -->
Unresolved issues and support/action: <!-- complete -->
UG common candidate / PG future branch plan: <!-- complete -->

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
