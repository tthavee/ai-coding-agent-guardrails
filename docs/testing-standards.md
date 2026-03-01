# Testing Standards for AI-Assisted Development

## The Core Rule

> **AI-generated logic requires human-authored tests.**

Copilot may generate test scaffolding, but the developer is responsible for:
1. Verifying that the tests actually validate the business requirement
2. Adding edge case tests that the AI did not generate
3. Ensuring tests fail when the implementation is wrong (mutation testing mindset)

---

## Minimum Coverage Requirements

| Code type | Minimum line coverage | Minimum branch coverage |
|---|---|---|
| Business logic / domain layer | 85% | 80% |
| API handlers / controllers | 80% | 75% |
| Utility functions | 90% | 85% |
| AI-generated functions | Same as above + edge case mandate |
| Security-related code | 95% | 90% |

Coverage alone is insufficient. Coverage checks run in CI but reviewers must also assess test *quality*.

---

## Mandatory Test Categories for AI-Generated Code

For every function or module where Copilot generated substantial code, tests MUST include:

### 1. Happy Path
```
# The expected, normal use case
def test_parse_user_input_valid():
    result = parse_user_input("john@example.com")
    assert result.email == "john@example.com"
```

### 2. Edge Cases (required — AI almost always misses these)
```
# Empty, null, boundary values
def test_parse_user_input_empty_string():
    with pytest.raises(ValueError, match="Input cannot be empty"):
        parse_user_input("")

def test_parse_user_input_none():
    with pytest.raises(TypeError):
        parse_user_input(None)

def test_parse_user_input_max_length():
    long_email = "a" * 255 + "@example.com"
    with pytest.raises(ValueError, match="exceeds maximum length"):
        parse_user_input(long_email)
```

### 3. Error Paths
```
# What happens when dependencies fail?
def test_parse_user_input_invalid_format():
    with pytest.raises(ValueError, match="Invalid email format"):
        parse_user_input("not-an-email")
```

### 4. Security Edge Cases (for any input-handling code)
```
# Injection, traversal, encoding attacks
def test_parse_user_input_sql_injection_attempt():
    result = parse_user_input("user@example.com'; DROP TABLE users;--")
    # Should either sanitize or reject — never pass raw to DB
    assert "DROP TABLE" not in result.email

def test_parse_user_input_xss_attempt():
    result = parse_user_input("<script>alert('xss')</script>@example.com")
    assert "<script>" not in result.email
```

---

## Test Naming Conventions

Use the **Given-When-Then** or **Scenario** pattern in test names:

```
# Good — describes the scenario and expected outcome
test_calculate_discount_when_user_is_premium_returns_20_percent()
test_create_order_when_stock_is_zero_raises_out_of_stock_error()
test_authenticate_when_token_is_expired_returns_401()

# Bad — only describes the function
test_calculate_discount()
test_create_order()
test_authenticate()
```

---

## AI Test Review Checklist

When reviewing AI-generated tests, verify:

- [ ] **Tests are independent** — no test depends on execution order or shared mutable state
- [ ] **Mocks are accurate** — verify AI-generated mocks match actual interface signatures
- [ ] **Assertions are specific** — `assert result == expected_object` not `assert result is not None`
- [ ] **Tests actually fail** — mentally or actually run a broken version; if tests still pass, they're useless
- [ ] **No magic numbers** — constants in tests should be named or commented to explain their significance
- [ ] **Async tests are properly awaited** — AI sometimes generates async tests without `await` or proper async setup

---

## Test Architecture Rules

### Do
- One logical assertion per test (multiple `assert` statements are fine if testing one concept)
- Use fixtures/factories for test data setup
- Group related tests in classes or `describe` blocks
- Test behavior, not implementation (don't test private methods directly)

### Do Not
- Do not `except: pass` in test helpers — let failures surface
- Do not mock out the unit under test
- Do not write tests that only test the mock itself
- Do not commit tests with `skip`, `xfail`, or `.only` without a tracked issue

---

## Mutation Testing (Recommended for AI-Heavy PRs)

For critical modules with high AI involvement, run mutation testing to verify test quality:

```bash
# Python
pip install mutmut
mutmut run --paths-to-mutate src/your_module.py
mutmut results

# JavaScript/TypeScript
npx stryker run

# Go
go install github.com/zimmski/go-mutesting/...@latest
go-mutesting ./pkg/yourpackage/...
```

A mutation score below **70%** on an AI-generated module is a signal that tests need significant manual improvement.

---

## QA Sign-off Requirements

| PR type | QA requirement |
|---|---|
| Bug fix in existing feature | Automated tests + regression test for the bug |
| New feature, limited AI usage | Automated unit + integration tests |
| New feature, heavy AI usage | Automated tests + QA exploratory test session |
| Security-related change | Automated tests + security-focused QA review |
| Major AI-generated module | Full QA test plan documented and executed |

---

## Continuous Integration Enforcement

The following CI checks are mandatory and block merge if they fail:

```yaml
# Enforced in .github/workflows/ci.yml
- Coverage threshold check
- Linting (no suppressed rules without justification)
- Secret scanning (detect-secrets / gitleaks)
- Dependency vulnerability scan (npm audit / safety / govulncheck)
- SAST scan (semgrep / CodeQL)
```

Tests that are skipped to make CI pass will be flagged in PR review.
