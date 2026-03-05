# Pull Request

## Testing
- [ ] Unit tests pass locally (`npm test` / `pytest` / `go test ./...` / `mvn test` / `./gradlew test`)
- [ ] New tests added for new logic
- [ ] Edge cases covered (empty/null inputs, boundary values, error paths)

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
# src/OrderProcessor.java — calculateTotal() method
# tests/OrderProcessorTest.java — scaffold generated, edge cases added manually
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
- [ ] No `eval()`, `exec()`, `Runtime.exec()`, or dynamic code execution with user input
- [ ] SQL uses parameterized queries / `PreparedStatement` (no string concatenation)
- [ ] External inputs are validated and sanitized
- [ ] No `console.log`/`print`/logger output of PII or sensitive data
