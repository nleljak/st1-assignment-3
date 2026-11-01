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
| QRY-01 | smartcare/queries.py | Practitioner isolation: appointments belonging to the requested practitioner are returned, while appointments belonging to other practitioners are excluded. | | |
| QRY-02 | smartcare/queries.py | Status filtering: each AppointmentStatus value returns only appointments with the matching status. A None status returns appointments of all statuses. | | |
| QRY-03 | smartcare/queries.py | Equal-time sorting: appointments with identical date/time values are ordered by appointment ID. | | |
| FP-01 | smartcare/queries.py | Repeated calls using the same input produce consistent results without changing the supplied appointments. | | |
| FP-02 | smartcare/queries.py  | Empty and already-sorted lists are handled correctly. The returned list is a new list and the original source order and appointment fields remain unchanged. | | |
| FP-03 | smartcare/queries.py  | The named appointment_sort_key() function is reused for sorting, keeping the sorting logic consistent and avoiding duplicated logic. | | |
| QRY-01 | smartcare/queries.py  | A known practitioner with no appointments returns an empty list. An unknown practitioner and an invalid status are rejected appropriately. | | |
| HIST-01 | tests/test_workflows.py  | A cancelled appointment remains retrievable and appears in an unfiltered practitioner listing, but is excluded from a scheduled-only listing. | | |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: The query functions are designed to be pure because they operate only on the appointment data supplied through their arguments. They do not access global or hidden state, read user input, print output, access files or modify the original appointment collection.

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | Register P1, D1 and D2; book A1 and A2; attempt a practitioner conflict; cancel and retrieve A1; list appointments; book into the freed slot; exit. | Successful registration and booking, rejection of the practitioner conflict, successful cancellation, retained appointment history, correct filtered listings and successful reuse of the freed slot. | | |
| UI-02 invalid-input recovery | Duplicate and unknown IDs, blank IDs, malformed and impossible dates, invalid status, unknown menu choice and repeated cancellation. | Invalid operations are rejected with appropriate messages. The application remains usable and invalid operations do not corrupt existing records. | | |
| Automated service workflow | Automated tests in tests/test_workflows.py. | Registration, booking, conflict checking, cancellation, retrieval and practitioner listing work together correctly. | | |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: The initial design separated appointment filtering and sorting from service coordination and console interaction.

The query functions were designed to operate on supplied appointment collections without modifying the source data. The service layer was responsible for validating the practitioner and optional appointment status, retrieving the current appointments from the shared data store and delegating filtering and sorting to the query functions.

The console remained responsible for reading user input, displaying appointment information and handling expected errors. This approach maintained the existing application architecture and avoided introducing unnecessary complexity.
Actual prompt/context supplied: Act as a senior Python software engineer reviewing my Stage 9 SmartCare appointment management application.
I want you to critically review my implementation of appointment querying, practitioner appointment listing and the integrated console workflow.
The application uses an in-memory data store and follows a layered architecture consisting of:
Domain objects, which enforce business rules and invariants.
Data store, which manages shared patient, practitioner and appointment collections.
Services, which coordinate operations and validate inputs.
Query functions, which filter and sort appointment collections.
Console, which handles user input and presentation.
Stage 9 requirements:
appointment_sort_key(appointment) must return a tuple containing the appointment date/time and appointment ID.
Select_appointments(appointments, practitioner_id, status=None) must filter by practitioner and optional appointment status.
A None status must include appointments of all statuses.
Results must be sorted in ascending order using the named appointment_sort_key function.
The query must return a new list and must not modify the original list or appointment objects.
list_practitioner_appointments() must validate that the practitioner exists and that a supplied status is a valid AppointmentStatus.
The service must retrieve a fresh appointment list from the data store and delegate filtering and sorting to the query function.
Cancelled appointments must remain retrievable and appear in unfiltered listings.
The console must support practitioner appointment listing with optional status filtering.
Existing functionality and accumulated tests must continue to work.
Please review the code I provide and:
Identify genuine implementation defects or potential edge cases.
Identify missing or weak automated tests.
Check whether responsibilities are correctly separated.
Check for unnecessary duplication or over-engineering.
Examine whether query functions are genuinely pure.
Check whether cancellation retains appointment history.
Identify any changes that could break existing functionality.
For every finding, provide:
The specific issue.
Its location in the code.
Its severity (High, Medium or Low).
Whether it should be fixed.
A suggested correction.
Actual response: The implementation should retain its existing layered architecture. Filtering and sorting should remain in the query module, practitioner validation and data retrieval should remain in the service layer, and user interaction should remain in the console.
I would not recommend introducing database persistence, additional repository layers or unnecessary abstractions because these are not required by the Stage 9 specification.
Before merging, run the complete accumulated test suite and ensure that the new query and workflow tests pass alongside the existing tests.

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|

| Avoid in-place sorting of the original appointment list. | `smartcare/queries.py`; FP-02 | Medium | Accept. Modifying the original list would violate the query purity requirement. | Used `sorted()` to return a new list without changing the original collection. | FP-02 confirmed the returned list was separate and the original order remained unchanged. |
| Include appointment ID as a secondary sorting key when appointment times are equal.| `smartcare/queries.py`; QRY-03 | Medium | Accept. This ensures deterministic ordering when appointments share the same date and time. | Updated `appointment_sort_key()` to return date/time and appointment ID. | QRY-03 verified the expected ordering. |
| Validate practitioner existence and appointment status in the service layer. | `smartcare/services.py`; QRY-04 | Medium | Accept. This separates invalid requests from valid practitioners who simply have no matching appointments. | Added or retained practitioner and status validation before querying appointments. | QRY-04 tested known-empty, unknown-practitioner and invalid-status cases. |
| Retain cancelled appointments rather than deleting them. | `smartcare/services.py`; `tests/test_workflows.py`; HIST-01 | Medium | Accept. Appointment history must remain available throughout the session. | Cancellation updates the appointment status rather than removing the record. | HIST-01 checked retrieval and filtered/unfiltered listings after cancellation. |
| Add database persistence to retain records after application exit. | Stage 9 in-memory storage requirement | High | Reject. Database persistence is outside the specified scope and would introduce unnecessary complexity. | No change. The application continues to use in-memory storage. | Checked the implementation against the Stage 9 requirements. |
| Add tests for empty, already-sorted and repeated query calls. | `tests/test_queries.py`; FP-01 and FP-02 | Low | Accept if these cases were not already covered. They provide additional evidence of consistent query behaviour. | Added focused tests where coverage was missing. | Re-ran the relevant query tests. |


Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: The application separates responsibilities across five components. Domain objects enforce business rules and invariants, such as valid appointment details and permitted status transitions. The shared data store manages the in-memory collections of patients, practitioners and appointments, providing a consistent source of data for the services. Services coordinate application operations by validating inputs, retrieving records and calling the appropriate domain or query functions. Pure query functions are responsible only for filtering and sorting the appointments supplied to them; they do not modify the original collections or perform input/output operations. Finally, the console layer handles user interaction, including displaying menus, collecting input and presenting results or error messages. This separation keeps business rules, data management, application coordination, querying and user interaction independent and easier to test.

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? The main architectural concern was ensuring that the service layer correctly integrated the shared data store with the pure query functions. The service needed to validate that the practitioner existed and that any supplied status was valid before retrieving the current appointment collection and passing it to the query function. This was important because filtering and sorting alone could not distinguish an unknown practitioner from a valid practitioner who simply had no appointments. Keeping this coordination in the service layer preserved the separation of responsibilities.
2. Which Copilot suggestion did you reject as over-engineering, and why? We rejected the suggestion to introduce database persistence. Although persistence could allow appointment records to remain available after the application closes, it was outside the Stage 9 requirements, which specified an in-memory application. Adding a database would introduce unnecessary complexity and additional responsibilities without improving the required functionality. We therefore retained the existing in-memory data store.
3. How did you prove cancelled appointments remain retrievable and listable in the same session? We verified this through the cancellation workflow. After cancelling an appointment, we retrieved it again using its appointment ID and checked that the record still existed with a CANCELLED status. We then listed the practitioner's appointments without a status filter and confirmed that the cancelled appointment remained visible. Finally, we used the scheduled-only filter and checked that the cancelled appointment was excluded. This demonstrated that cancellation changes the appointment's status rather than deleting the record.

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
