# AGENTS.md — GitHub Copilot Agent Guardrails

> **Purpose**: This file governs how GitHub Copilot (and any AI code assistant) may be used in this repository.
> Every contributor — human or AI — must follow these rules. Copilot agents read this file automatically.

---

## 1. Core Philosophy

AI assistants are **accelerators, not replacements**. Developers are accountable for every line of code
that enters this repository, regardless of how it was generated. "The AI wrote it" is not an acceptable
explanation for a bug, security vulnerability, or failing test.

**The AI writes a draft. The developer owns the result.**

---

## 2. What Copilot MAY Do

- Suggest autocompletions for boilerplate (imports, struct definitions, standard CRUD patterns)
- Generate unit test scaffolding that the developer then validates and extends
- Explain existing code or suggest refactor options for review
- Draft documentation comments that the developer reviews for accuracy
- Propose algorithm implementations that the developer must understand before accepting

---

## 3. What Copilot MUST NOT Do Without Human Review

- Generate authentication, authorization, or session management logic autonomously
- Write database migrations or schema changes
- Produce cryptographic operations (hashing, signing, encryption/decryption)
- Generate environment configuration or secrets handling code
- Write infrastructure-as-code (Terraform, Kubernetes manifests, Dockerfiles) without explicit review
- Produce any public-facing API contract changes

All of the above require a **senior developer sign-off** in the PR review (see `docs/code-review-guidelines.md`).

---

## 4. Mandatory Developer Obligations

Before committing any AI-generated or AI-assisted code, the developer MUST:

1. **Read and understand** every line — if you cannot explain it, do not commit it
2. **Run the full test suite locally** — `npm test` / `pytest` / `go test ./...` (see project README)
3. **Write or update unit tests** — AI-suggested logic must have human-authored tests covering edge cases
4. **Check for hardcoded values** — secrets, localhost URLs, test credentials must never be committed
5. **Verify imports and dependencies** — Copilot sometimes imports packages that don't exist or aren't approved
6. **Disclose AI usage in the PR** — use the PR template section "AI Assistance Disclosure"

---

## 5. Prohibited Patterns

Copilot agents must not generate, and developers must reject suggestions containing:

```
# Absolute prohibitions
- eval(), exec(), os.system() with user-controlled input
- Hardcoded credentials, API keys, or tokens of any kind
- console.log / print statements containing PII or sensitive data
- SQL string concatenation (use parameterized queries only)
- MD5 or SHA1 for password hashing (use bcrypt/argon2/scrypt)
- HTTP (non-TLS) connections to external services in non-test code
- Disabling security linters with inline suppression comments
```

---

## 6. Code Ownership Rules

| Scenario | Requirement |
|---|---|
| >50% of a function is AI-generated | Developer must add an inline comment explaining the logic |
| Entire file is AI-generated | Mandatory senior review + documentation of why |
| AI-generated test file | Developer must add at least 3 additional edge-case tests manually |
| AI-suggested dependency added | Must be approved via the dependency review process (`docs/dependency-policy.md`) |

---

## 7. Agent Behavioral Constraints

When operating in **agent mode** (multi-step autonomous tasks), Copilot MUST:

- Stop and request human confirmation before creating, renaming, or deleting files
- Stop and request human confirmation before modifying CI/CD configuration
- Never commit or push directly — all changes go through PRs
- Never modify `.github/`, `AGENTS.md`, or any security configuration file
- Annotate all generated code blocks with a trailing comment: `# generated: copilot — reviewed by: <author>`

---

## 8. Escalation and Override

If a developer believes a guardrail should be relaxed for a specific task:

1. Open a discussion in `#ai-tooling` Teams channel
2. Get approval from a Staff Engineer or Security team member
3. Document the exception in the PR description with justification
4. The exception applies **only to that PR**, not permanently

---

## 9. Enforcement

These rules are enforced by:

- **CI checks**: Automated linting and secret scanning on every PR (see `.github/workflows/`)
- **PR template**: AI disclosure checklist is required before merge
- **Code review**: Reviewers are instructed to flag undisclosed AI-generated code
- **Periodic audits**: Quarterly review of AI usage patterns by the platform team

Violations may result in PR rejection, and repeated violations will trigger a conversation with your manager.

---

## 10. Learning Resources

Before using Copilot on production code, complete:

- [ ] Internal AI tooling onboarding (link in company wiki)
- [ ] OWASP Top 10 awareness training
- [ ] This repo's `docs/ai-onboarding.md`

---

*Last updated: 2026-03-01 | Maintained by: Platform Engineering*
