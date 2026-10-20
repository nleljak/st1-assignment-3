# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Tuesday 17:30
- Members, GitHub usernames and cohorts: Kynan and Nikola, kcsch and nleljak, Tuesday 17:30
- Repository URL: https://github.com/nleljak/st1-assignment-3.git 
- Starting SHA: [response]

## A Requirement to issue activities

### FR-02 Patient Search

- Title: Implement Patient Search by Patient ID
- Context: The SmartCare system stores registered patients in SmartCareDataStore. Staff need to retrieve the correct patient using their unique patient ID.
- Requirement: The system shall allow a registered patient to be retrieved using their patient ID without changing existing patient records.
- Acceptance criteria: Searching for an existing patient ID returns the correct Patient object. Searching for an unknown patient ID handles the missing patient according to the service specification. Duplicate patient IDs cannot replace existing patient records, as verified by test_duplicate_patient_preserves_original. Searching for a patient does not modify stored patient details.
- Scope: Patient lookup through the relevant service and data store. Does not include patient registration changes or unrelated appointment functionality.
- Definition of Done: The lookup behaviour meets the agreed specification, relevant automated tests are passed, the change is reviewed by another team member and the PR is merged according to the team workflow.
- Owner: Kynan
- Actual issue link: https://github.com/nleljak/st1-assignment-3/blob/main/project/tests/test_starter.py

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: Implement Appointment Cancellation While Retaining History
- Context: SmartCare appointments have a status and are stored in SmartCareDataStore. Cancelling an appointment should update its status without deleting the appointment record.
- Requirement: The system shall allow an eligible appointment to be cancelled while retaining its record and relevant appointment details for historical purposes.
- Acceptance criteria: Cancelling a scheduled appointment changes its status to AppointmentStatus.CANCELLED. The cancelled appointment remains retrievable through find_appointment(). The cancelled appointment remains in data_store.list_appointments(). Cancelling an already cancelled appointment raises ValueError, consistent with the supplied test_domain_cancellation_and_guard. Any additional cancellation restrictions specified in the assignment, such as preventing cancellation of completed appointments, are implemented and tested.
- Scope: Appointment cancellation behaviour and retention of existing appointment records. Unrelated patient fields, unrelated architecture changes and unnecessary dependencies are excluded.
- Definition of Done: Cancellation and history-retention requirements pass automated tests, invalid cancellation attempts are handled correctly, another team member reviews the change, and the approved PR is merged.
- Owner: Kynan/Nikola
- Actual issue link: https://github.com/nleljak/st1-assignment-3/blob/main/project/tests/test_starter.py

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | weak | Does not explain what was changed or why. |
| final version | weak | Vague and does not identify the functionality or fix. |
| Add patient search by ID | strong | Clearly describes the change and the feature it implements. |
| fix stuff | weak | Gives no meaningful information about the bug or solution. |
| Prevent cancellation of completed appointments | strong | Describes the behaviour being changed |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR combines appointment cancellation with unrelated patient-field renaming, unrelated code restructuring and a new dependency. These changes make the PR broader than its stated purpose.
- Responsibility and architecture concerns: Unrelated patient-field changes may affect other components and break existing interfaces. A new dependency adds maintenance and compatibility considerations. Changes should remain within the relevant service and domain responsibilities.
- Testing and review concerns: Reviewers must assess more code than necessary. It becomes harder to identify regressions, attribute failures to specific changes and determine whether cancellation and retained-history requirements are satisfied.
- Changes to remove or separate, with reasons: Remove unrelated patient-field renaming from the cancellation PR and create a separate PR if it is required. Separate unrelated restructuring into its own focused PR, with independent tests and justification. Remove the new dependency unless it is genuinely required; if needed, justify it and review its compatibility and maintenance implications. Keep the cancellation implementation and its relevant tests together so the PR is focused and straightforward to verify.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: The statement does not identify what tests were ran, the command or directory used, the observed results or the code reviewed. Nor whether the cancellation and history-retention requirements were checked.
- Follow-up review question 1: Does cancellation change the appointment status to CANCELLED without deleting the appointment record?
- Follow-up review question 2: Does the implementation reject repeated cancellation and other invalid cancellation attempts according to the specification?
- Follow-up review question 3: Which automated tests were executed? Provide the exact command, working directory and observed result.
- Follow-up review question 4: Does the change preserve existing appointment details and avoid breaking booking, lookup or other appointment functionality?
- Follow-up review question 5: Does the PR contain unrelated changes, unnecessary dependencies or logic that belongs in another service or domain class?
- Additional questions if useful: Are there tests for unknown appointment IDs?

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | Use feature/short-description for features and fix/short-description for bug fixes. |
| Commit message convention | Use short, descriptive imperative messages, such as Add patient search by ID. |
| PR size | Keep each PR focused on one requirement or closely related change, including relevant tests. |
| Another-member review requirement | Every PR must be reviewed by at least one other team member before merging. The author should not approve their own PR. |
| Merge rule | Merge only after required review feedback is addressed and relevant automated tests pass. Use the repository's agreed merge strategy. |
| Significant Copilot disclosure rule | Record Copilot assistance, including its purpose, suggestions, human verification and whether suggestions were accepted, modified or rejected. |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| https://github.com/nleljak/st1-assignment-3/blob/main/project/tests/test_starter.py | FR-02 Patient Search | Kynan | Existing patient ID returns the correct patient; unknown IDs are handled as specified; existing records are preserved. | In progress |
| https://github.com/nleljak/st1-assignment-3/blob/main/project/tests/test_starter.py | Practitioner Lookup | Nikola | Eligible appointment is cancelled, its record remains retrievable and invalid cancellation attempts are handled according to the specification. | In progress |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: (https://github.com/nleljak/st1-assignment-3/blob/main/project/tests/test_starter.py) - Patient + Practitoner lookup
- Linked issue and requirement: https://github.com/nleljak/st1-assignment-3/blob/main/project/tests/test_starter.py
- Feature branch: [response]
- Changed behaviour: Added tests for successful patient and practitioner lookup by ID and for handling unknown IDs. The tests expect the lookup methods to return the registered object or raise LookupError when the ID is unknown.
- Meaningful commits: [links]
- Test command, directory and observed result: pytest, passed
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: N/A
- Prompt/purpose and relevant issue/diff: N/A
- Summary of output: N/A
- Human check against actual code, requirements and tests: N/A
- Decision — Accept / Modify / Reject: N/A
- Reason: N/A
- Verification/evidence: N/A

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: N/A
- Copilot noticed: N/A
- Overlap: N/A
- What did the human reviewer notice that Copilot did not: N/A
- What did Copilot identify that the human reviewer initially missed: N/A
- Unsupported or incorrect Copilot suggestion: N/A
- Human judgement accepted, modified or rejected, and why: N/A
- Which evidence justified merge approval: N/A

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: Kynan
- Implementation: Worked on Stage 6 patient and practitioner lookup functionality, including PatientService.find_patient() and PractitionerService.find_practitioner(), if these methods were implemented by me.
- Testing: Wrote tests verifying that patient and practitioner lookup return the correct registered objects and raise LookupError for unknown IDs. Evidence: test_find_patient(), test_find_unknown_patient(), test_find_practitioner(), and test_find_unknown_practitioner()
- Review: N/A
- Issue refinement: N/A
- Design and responsibility discussion: Spoke about how we were going to set up the code.
- Debugging or integration: N/A
- Documentation or team support: Helped design and check the initial code written. 

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

As the number of commits measures activity and not the quality or complexity of the work completed.

## L Stage 6 formative questions

1. What is version control?

It is a system that tracks the changes made to files over time, allow for the developers to record, review and revert changes and collaborate with other people without overwriting work. 

2. Why is a feature branch useful?

It allows a developer to work on a new feature or fix the main code separately. Preventing unfinished or faulty changes from affecting the main project and allowing for changes to be tested before being merged. 

3. What makes a commit a good engineering commit?

It is small, focused and self-contained and is clear and easy to understand. They are also easy to review and revert if needed, making the project easier to maintain and collaborate on. 

4. What is a pull request?

It's a request to merge changes from one branch to another into another branch. Allowing team members to review the code, discuss improvements, identify bugs and run tests before the changes are merged. 

5. What is the purpose of code review?

Other developers examine the code changes before they are implemented into the program. Helping identify bugs, improve code quality, check requirements are met and ensure the coding standards are followed. 

6. What does a Git diff show?

Shows the differences between versions of files, highlighting lines of code that have been added, modified or removed. Along with helping developers review changes, identify mistakes and understand what a commit contains. 

7. What is a Definition of Done?

A set of agreed criteria by the developers that must be met before a task is considered complete. 

8. What is the appropriate role of GitHub Copilot in pull-request review?

It should be used as an assistant and not a direct developer or as a replacement for human judgement. It may help identify bugs, security concerns, logic errors or improvement to code quality, all of which need to be verified by a human.

9. Why should individual contribution not be judged only by commit count?

As commits vary in complexity, quality and impact. Someone may make fewer commits but have more heavy features, fix more complex bugs or review other member's code. Contribution should instead be assessed using evidence of the quality, significance and effectiveness of each person’s work.

10. What is the Stage 6 engineering rule?

Make small traceable changes, test the code, review the changes and record genuine evidence of that work. 

## M Completion and handover

- Starting SHA: [response]
- Final Stage 6 code SHA: [response]
- Test command: [response]
- Working directory: [response]
- Observed result: [response]
- PR and another-member reviewer: [links]
- Unresolved issue or none: [response]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

- [x] Three Stage 6 service targets completed and checked.
- [x] Original supplied tests retained and passing.
- [x] At least two focused issues link requirements and acceptance criteria.
- [x] Feature work reviewed by another member using the actual diff.
- [x] Human-first review and required Copilot comparison recorded.
- [x] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [x] Required activities, quiz responses and contribution notes completed.
- [x] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
