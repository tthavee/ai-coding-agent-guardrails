# Code Review Guidelines for AI-Assisted Code

## Reviewer Mindset

When reviewing a PR that contains AI-generated code, apply **extra skepticism**, not less.
AI models produce confident-sounding code that may be subtly wrong, outdated, or insecure.
Your job is to catch what the developer and the AI both missed.

---

## Step 1: Check the AI Disclosure Section First

Before reviewing any code, look at the PR template's **AI Assistance Disclosure**.

| Disclosure state | Action |
|---|---|
| "No AI used" but code style looks AI-generated | Request clarification before continuing |
| AI used, checklist incomplete | Request completion before reviewing |
| AI used for security-sensitive area without senior sign-off | Block the PR immediately |
| Disclosure fully complete | Proceed with review |

**Red flags that suggest undisclosed AI usage:**
- Unusually consistent but generic variable names (`data`, `result`, `item`, `response`)
- Over-engineered abstractions for a simple task
- Comments that describe *what* the code does rather than *why*
- Functions that are correct in isolation but don't fit the surrounding codebase patterns
- Boilerplate error handling that catches everything silently

---

## Step 2: Logic and Correctness Review

For AI-generated functions, verify:

### Business Logic
- [ ] Does it actually solve the stated problem, or a slightly different one?
- [ ] Are edge cases handled? (empty inputs, null/undefined, boundary values, overflow)
- [ ] Does it handle errors in a way that's consistent with the rest of the codebase?
- [ ] Are return values and types correct?

### Common AI Mistakes to Check
- **Off-by-one errors** in loops and array indexing
- **Race conditions** in async code (missing `await`, incorrect Promise chains)
- **Incorrect regex** that looks right but has edge-case failures
- **Wrong algorithm complexity** — AI often picks O(n²) when O(n) is trivial
- **Stale API usage** — AI training data may reference deprecated library versions
- **Hallucinated methods** — calling `.toISOString()` on a non-Date object, etc.

---

## Step 3: Security Review

Run through this checklist for every AI-generated code block:

### Input Handling
- [ ] Is all user input validated before use?
- [ ] Are path traversal attacks prevented for file operations?
- [ ] Are SQL queries parameterized? (reject any string concatenation into queries)
- [ ] Is HTML output escaped to prevent XSS?

### Authentication & Authorization
- [ ] Are permission checks in the right place (server-side, not just client-side)?
- [ ] Are JWTs validated properly (algorithm, expiry, signature)?
- [ ] Are session tokens generated with sufficient entropy?

### Secrets and Configuration
- [ ] No hardcoded credentials, API keys, or connection strings
- [ ] No debug/test values that could leak to production
- [ ] Environment variables accessed through approved config patterns

### Cryptography
- [ ] Only approved algorithms: AES-256, SHA-256+, bcrypt/argon2/scrypt for passwords
- [ ] No MD5 or SHA1 for security purposes
- [ ] No custom crypto implementations

---

## Step 4: Test Quality Review

AI-generated tests are often **too happy-path**. Verify:

- [ ] Tests cover the actual business requirements, not just the implementation
- [ ] At least one test for each identified edge case
- [ ] Error paths and exception cases are tested
- [ ] Mocks/stubs accurately represent real dependencies (AI often over-mocks)
- [ ] Test names describe the *scenario*, not just the function name
- [ ] No tests that always pass trivially (`assert True`, `expect(true).toBe(true)`)

**Ask yourself**: If the implementation had a bug in the edge case, would these tests catch it?
If the answer is no, request more tests before approving.

---

## Step 5: Code Quality and Maintainability

- [ ] Does the code follow existing project patterns and conventions?
- [ ] Are abstractions at the right level? (AI tends to over-abstract or under-abstract)
- [ ] Are the inline comments (where added) accurate and useful?
- [ ] Does the naming make sense in the context of the domain?
- [ ] Is the code readable without needing to run it?

---

## Senior Reviewer Requirements

A **senior developer or tech lead** must approve PRs where AI-generated code touches:

| Area | Why |
|---|---|
| Authentication / authorization | Subtle bugs have critical security impact |
| Cryptographic operations | Incorrect implementation can defeat the purpose |
| Database schema / migrations | Hard to reverse, affects all environments |
| Public API contracts | Breaking changes affect consumers |
| Payment / financial calculations | Precision and rounding errors are costly |
| Infrastructure / CI/CD configuration | Blast radius is the entire team |
| `AGENTS.md` or `.github/` changes | Policy must not be accidentally weakened |

---

## Giving Feedback on AI Code

When requesting changes on AI-generated code, be specific about the concern.
Avoid: "This looks AI-generated, rewrite it."
Instead: "This function doesn't handle the case where `user` is null (line 42). Please add a null check and a test for that scenario."

The goal is to help the developer understand the gap in their review, not to penalize AI usage.

---

## Approving AI-Assisted PRs

Before clicking Approve on a PR with AI-disclosed code, confirm:

1. You can explain the critical logic paths yourself
2. Security checklist is clean
3. Tests cover edge cases, not just happy paths
4. The developer demonstrated understanding (their responses to comments show comprehension)
5. Senior sign-off obtained for any gated areas

*"LGTM" is not sufficient for AI-heavy PRs. Write a brief summary of what you verified.*
