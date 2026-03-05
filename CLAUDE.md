# CLAUDE.md — Claude Code Mandatory Rules

These rules apply to **every code generation action** Claude Code takes in this repository.
They are enforced instructions, not suggestions. They extend the policy in `AGENTS.md`.

---

## Tagging Is Non-Negotiable

Every function, method, or class body you write or substantially modify **must** include an
attribution comment on the **first write**. Do not wait to be reminded.

**Python / Go / Ruby:**
```python
# generated: copilot — reviewed by: <author>
```

**Java / JavaScript / TypeScript / C#:**
```java
// generated: copilot — reviewed by: <author>
```

Place the tag immediately after the docstring (if present), before the first line of logic.
Close the generated block with:
- Python: `# end generated: copilot`
- Java/JS/TS: `// end generated: copilot`

---

## Logic Comment — Required for Any Function >50% AI-Generated

For any function where you write more than half the body, add a `# Logic:` comment above the tag,
written to explain what the code does and why. This is proof of comprehension for the reviewer.

**Python example:**
```python
def validate_password(password: str) -> str:
    # Logic: rejects None/non-string early; enforces MIN and MAX length bounds —
    #        MAX caps at 128 to prevent bcrypt DoS on inputs exceeding 72 bytes.
    # generated: copilot — reviewed by: <author>
    ...
    # end generated: copilot
```

**Java example:**
```java
public BigDecimal calculateTotal(Order order) {
    // Logic: streams items, multiplies qty × unitPrice, sums to BigDecimal,
    //        returns ZERO for empty orders to avoid null downstream.
    // generated: copilot — reviewed by: yourname
    return order.getItems().stream()
        .map(i -> i.getUnitPrice().multiply(BigDecimal.valueOf(i.getQuantity())))
        .reduce(BigDecimal.ZERO, BigDecimal::add);
    // end generated: copilot
}
```

---

## Human-Authored Functions Must Also Be Declared

Any function you did **not** generate must be explicitly marked so CI can distinguish it:

```python
# human-authored
```
```java
// human-authored
```

This is enforced by CI (`scripts/check_ai_tags.py`). Every new function in the diff must have
one of these two markers, or the PR will be blocked.

---

## Pre-Flight Checklist — Before Completing Any Code Task

Before finishing any code generation task, verify:

- [ ] Every new or substantially modified function has `# generated:` / `// generated:` or `# human-authored` / `// human-authored`
- [ ] Functions with >50% AI body have a `# Logic:` comment above the tag
- [ ] No hardcoded secrets, credentials, API keys, or tokens
- [ ] None of the prohibited patterns from `AGENTS.md §5` are present
- [ ] Auth, crypto, or DB migration code is flagged for senior review

---

## Prohibited Patterns (from AGENTS.md §5)

Never generate:
- `eval()`, `exec()`, `os.system()` with user-controlled input (Python)
- `Runtime.exec()` or `ProcessBuilder` with unsanitized input (Java)
- SQL built with string concatenation — use `PreparedStatement` (Java) or parameterized queries (Python)
- Hardcoded credentials or API keys
- MD5 or SHA1 for password hashing
- HTTP (non-TLS) connections to external services in non-test code

---

*This file is read by Claude Code on every session start. Violations of these rules are a policy breach.*
