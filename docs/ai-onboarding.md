# AI Tooling Onboarding — GitHub Copilot

Welcome to the team. Before using GitHub Copilot on production code, read this guide in full.
It takes about 20 minutes and will save you from common mistakes that have caused real incidents.

---

## Why We Have These Rules

AI code assistants are powerful, but they have consistent failure modes:

1. **They optimize for plausibility, not correctness.** Code looks right but has subtle bugs.
2. **Their training data is frozen.** They suggest deprecated APIs, outdated patterns, insecure practices.
3. **They can't read your context.** They don't know your business rules, data contracts, or threat model.
4. **They're convincing.** A confident-sounding wrong answer is more dangerous than an obvious error.

Junior developers are particularly at risk because they may not yet have the experience to spot these issues.
These guardrails exist to protect you, your teammates, and your customers.

---

## Your Mental Model: The Three-Pass Rule

When working with Copilot suggestions, apply three passes before accepting:

### Pass 1: Does it compile / parse?
Run it. If it doesn't work at all, reject or fix.

### Pass 2: Do I understand every line?
Read each line. If you can't explain what it does and why, don't accept it.
It's fine to use Copilot Chat to ask "explain this code" — but you must understand the answer.

### Pass 3: Does it handle failure?
What happens if the input is null? If the network call fails? If the database returns an empty set?
AI-generated code frequently handles only the happy path.

---

## How to Use Copilot Effectively (Not Passively)

### Good usage patterns

**Use Copilot for repetition, not for thinking:**
```
# Good: Let Copilot generate the nth CRUD endpoint after you've done the first one
# Good: Let Copilot scaffold a test file structure
# Good: Ask Copilot Chat to explain an unfamiliar library

# Bad: Ask Copilot to design your data model
# Bad: Accept a Copilot-generated auth flow without reading it
# Bad: Use Copilot to write code you haven't yet designed in your head
```

**Write the test first, let Copilot fill in the implementation:**
This forces you to think about the contract before accepting suggestions.

**Use inline comments to constrain Copilot:**

Python:
```python
# Parse the ISO 8601 date string and return None if invalid (do not raise)
def parse_date(date_str: str) -> datetime | None:
    # Copilot suggestion will be constrained by your comment
```

Java:
```java
// Parse ISO 8601 date string; return Optional.empty() if invalid — do not throw
public Optional<LocalDate> parseDate(String dateStr) {
    // Copilot suggestion will be constrained by your comment
}
```

**Reject suggestions you can't explain in 30 seconds.** If a reviewer asks you why line 47 does what it does, you need an answer.

---

## What to Do When Copilot Suggests Something Suspicious

If a suggestion:
- Uses `eval()`, `exec()`, or `subprocess` with string concatenation → **always reject**
- Uses `Runtime.exec()` or `ProcessBuilder` with unsanitized input (Java) → **always reject**
- Uses `Statement` instead of `PreparedStatement` for SQL (Java) → **always reject**
- Imports a package you don't recognize → **look it up before accepting**
- Appears to disable a linter rule → **understand why before accepting**
- Hardcodes a value that looks like a credential → **reject and rotate the credential if it was real**
- Calls a method that looks wrong for the type → **verify against the docs**

When in doubt, ask in `#engineering` or pair with a senior developer.

---

## Disclosure Requirements

You MUST disclose AI assistance in every PR where it was used. This is not about policing you —
it helps reviewers know where to focus their attention. Undisclosed AI usage that causes a bug
is a trust issue, not just a technical issue.

See the PR template for the exact disclosure format.

---

## One-Time Local Setup

Run this once after cloning the repo to activate the pre-commit hook:

```bash
git config core.hooksPath .githooks
```

This enables a local warning if you commit code with an unfilled `<author>` placeholder
in an AI tag. It won't block your commit — it's a reminder.

---

## Practical Exercises Before Going Live

Complete these before using Copilot on your first production PR:

### Exercise 1: Find the Bug
Accept the following Copilot-style suggestion, then find the bug:

```python
def get_user_data(user_id: int) -> dict:
    conn = get_db_connection()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = conn.execute(query)
    return result.fetchone()
```

<details>
<summary>Answer</summary>
SQL injection vulnerability: user_id is interpolated directly into the query string.
If user_id = "1; DROP TABLE users;--", the database executes the DROP.
Fix: use parameterized queries: conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
</details>

### Exercise 2: Find the Missing Test
Given this AI-generated test, what critical case is missing?

```javascript
describe('calculateDiscount', () => {
  it('returns 10% for standard users', () => {
    expect(calculateDiscount(100, 'standard')).toBe(90);
  });
  it('returns 20% for premium users', () => {
    expect(calculateDiscount(100, 'premium')).toBe(80);
  });
});
```

<details>
<summary>Answer</summary>
Missing: negative price, zero price, unknown user type, non-numeric price input,
very large numbers (overflow), null/undefined arguments.
What does the function do when called with calculateDiscount(-50, 'premium') or
calculateDiscount(100, 'admin')?
</details>

### Exercise 3: Identify the Stale API
```javascript
const crypto = require('crypto');
const hash = crypto.createHash('md5').update(password).digest('hex');
```

<details>
<summary>Answer</summary>
MD5 is cryptographically broken and must never be used for password hashing.
Use bcrypt, argon2, or scrypt instead. This is in AGENTS.md under Prohibited Patterns.
</details>

---

## Quick Reference Card

| If you want to... | Do this |
|---|---|
| Get help with boilerplate | Accept Copilot suggestions freely after review |
| Design a new feature | Design it yourself first, then use Copilot to fill in |
| Understand unfamiliar code | Use Copilot Chat: "explain this function" |
| Write tests | Write the test names yourself, use Copilot for bodies, add edge cases manually |
| Handle auth/crypto | Read the company security patterns doc first, use Copilot for syntax only |
| Add a new dependency | Check the dependency approval process first |
| Be unsure about a suggestion | Ask a senior dev or post in `#engineering` |

---

## Contacts

- **AI tooling questions**: `#ai-tooling` Teams
- **Security concerns**: `#security` Teams or security@yourcompany.com
- **Policy questions**: Your team's Staff Engineer
- **Incident reporting**: Follow the standard incident response runbook

---

*Read AGENTS.md for the full policy. This document is the practical how-to; AGENTS.md is the authoritative policy.*
