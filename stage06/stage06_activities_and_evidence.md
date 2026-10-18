# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Tuesday 17:30
- Members, GitHub usernames and cohorts: Kynan and Nikola, kcsch and nleljak
- Repository URL: https://github.com/nleljak/st1-assignment-3.git 
- Starting SHA: [response]

## A Requirement to issue activities

### FR-02 Patient Search

- Title: [response]
- Context: [response]
- Requirement: [response]
- Acceptance criteria: [response]
- Scope: [response]
- Definition of Done: [response]
- Owner: [response]
- Actual issue link: [response]

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: [response]
- Context: [response]
- Requirement: [response]
- Acceptance criteria: [response]
- Scope: [response]
- Definition of Done: [response]
- Owner: [response]
- Actual issue link: [response]

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | [select] | [response] |
| final version | [select] | [response] |
| Add patient search by ID | [select] | [response] |
| fix stuff | [select] | [response] |
| Prevent cancellation of completed appointments | [select] | [response] |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: [response]
- Responsibility and architecture concerns: [response]
- Testing and review concerns: [response]
- Changes to remove or separate, with reasons: [response]

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: [response]
- Follow-up review question 1: [response]
- Follow-up review question 2: [response]
- Follow-up review question 3: [response]
- Follow-up review question 4: [response]
- Follow-up review question 5: [response]
- Additional questions if useful: [response]

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | [response] |
| Commit message convention | [response] |
| PR size | [response] |
| Another-member review requirement | [response] |
| Merge rule | [response] |
| Significant Copilot disclosure rule | [response] |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| [issue 1] | [response] | [response] | [response] | [response] |
| [issue 2] | [response] | [response] | [response] | [response] |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: [response]
- Linked issue and requirement: [response]
- Feature branch: [response]
- Changed behaviour: [response]
- Meaningful commits: [links]
- Test command, directory and observed result: [response]
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

- Member and task: [response]
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

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

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
