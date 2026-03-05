# Pull Request

## Summary
<!-- What does this PR do? Why is this change needed? -->


## Changes
<!-- Bullet list of key changes -->
-
-

## Testing
<!-- How was this tested? -->
- [ ] Unit tests pass locally (`npm test` / `pytest` / `go test ./...` / `mvn test` / `./gradlew test`)
- [ ] New tests added for new logic
- [ ] Manual testing performed (describe below)

**Manual test notes:**


---

## AI Assistance Disclosure

> **Required.** Omitting or falsifying this section is a policy violation.

- [ ] No AI assistance was used in this PR
- [ ] AI assistance was used — complete the section below

### If AI was used:

**Tool(s) used:** (e.g., GitHub Copilot, Copilot Chat, Copilot Agent)

**Scope of AI involvement:**
- [ ] Autocompletion suggestions only (minor)
- [ ] Copilot Chat for explanation / debugging help
- [ ] Copilot generated substantial function/class bodies
- [ ] Copilot Agent ran multi-step autonomous tasks

**AI-generated files or functions** (list them):
```
# Example:
# src/utils/parser.ts — parseQueryString() function
# tests/parser.test.ts — scaffold generated, edge cases added manually
```

**Developer verification checklist:**
- [ ] I read and understood every line of AI-generated code in this PR
- [ ] I can explain the logic to a reviewer without referring back to Copilot
- [ ] AI-generated logic has human-authored tests covering edge cases
- [ ] No hardcoded secrets, credentials, or environment-specific values
- [ ] All imports/packages were verified to exist and are approved
- [ ] Security-sensitive areas (auth, crypto, DB) have senior reviewer sign-off

---

## Security Checklist
- [ ] No secrets, tokens, or credentials committed
- [ ] No `eval()`, `exec()`, or dynamic code execution with user input
- [ ] SQL uses parameterized queries (no string concatenation)
- [ ] External inputs are validated and sanitized
- [ ] No `console.log`/`print` of PII or sensitive data

---

## Reviewer Notes
<!-- Anything specific you want reviewers to focus on? -->


---

## Related Issues / Tickets
<!-- Link to Jira/GitHub issues -->
Closes #
