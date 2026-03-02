# GitHub Copilot Instructions

These instructions apply to every suggestion Copilot makes in this repository.
Read AGENTS.md for the full policy. The rules below are the behavioural subset
that Copilot must apply automatically.

## Tagging Requirement

Every function, method, or class body you generate must end with a trailing comment:

- Python / Go / Ruby:  `# generated: copilot — reviewed by: <author>`
- JavaScript / TypeScript / Java / C#:  `// generated: copilot — reviewed by: <author>`

The `<author>` placeholder must be left as-is. The developer replaces it with
their name before committing. Do not omit the tag even for small helpers.

Example (Python):
```python
def calculate_discount(price: float, tier: str) -> float:
    if tier == "premium":
        return price * 0.80
    return price * 0.90
    # generated: copilot — reviewed by: <author>
```

Example (TypeScript):
```typescript
function parseQueryString(raw: string): Record<string, string> {
    return Object.fromEntries(new URLSearchParams(raw));
    // generated: copilot — reviewed by: <author>
}
```

## Security Rules (always apply)

- Never use `eval()`, `exec()`, or `os.system()` with user-controlled input
- Always use parameterized queries — never concatenate user input into SQL strings
- Never hardcode credentials, tokens, or API keys
- Use `bcrypt`, `argon2`, or `scrypt` for password hashing — never MD5 or SHA1
- Always validate and sanitize inputs at function boundaries
- Escape all user-supplied strings before rendering in HTML contexts

## Code Style

- Follow existing patterns in the file being edited
- Prefer explicit error handling over silent failures
- Match the naming conventions already present in the codebase
