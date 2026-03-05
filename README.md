# AI Coding Agent Guardrails

A structured set of controls for governing GitHub Copilot (and similar AI coding assistants)
across engineering teams — ensuring code quality, security, and developer accountability.

**Primary language: Java (Maven/Gradle).** All rules, examples, and CI checks also cover Python, Go, TypeScript, and JavaScript.

> For a full breakdown of how these files relate, see [docs/guardrails-overview.md](docs/guardrails-overview.md).

## Structure

```
.
├── AGENTS.md                             # Master AI policy (read by Copilot agents + Claude Code)
├── .github/
│   ├── copilot-instructions.md           # Per-suggestion rules (read by Copilot in IDE)
│   ├── CODEOWNERS                        # Protects policy files from unauthorized changes
│   ├── pull_request_template.md          # AI disclosure + language-specific security checklist
│   └── workflows/
│       └── ai-guardrails-ci.yml          # CI: secret scan, coverage gate, PR policy, protected files
├── .githooks/
│   └── pre-commit                        # Local: warns on unfilled AI tag <author> placeholder
└── docs/
    ├── guardrails-overview.md            # Full control map + file relationship diagram
    ├── ai-onboarding.md                  # Developer guide: how to use Copilot responsibly
    ├── code-review-guidelines.md         # How to review AI-assisted PRs
    └── testing-standards.md             # Test categories, naming conventions, mutation testing
```

## Guardrail Layers

| Layer | What enforces it | Purpose |
|---|---|---|
| **AI Behavior** | `AGENTS.md`, `copilot-instructions.md` | Shapes what Copilot generates before a developer sees it |
| **Local** | `.githooks/pre-commit`, `pom.xml`/`pyproject.toml` | Catches issues at commit time; enforces coverage thresholds |
| **PR Gate** | `pull_request_template.md` | Forces AI disclosure + Java/Python security checklist on every PR |
| **CI** | `ai-guardrails-ci.yml` (4 jobs) | Blocks merge on: secret leak, coverage drop, missing AI tags, protected file changes |
| **Human** | `docs/` | Trains developers and reviewers on AI-specific risks and standards |

## CI Jobs (all block merge on failure)

| Job | What it checks |
|---|---|
| Secret Scanning | Gitleaks + detect-secrets — credentials, tokens, API keys |
| Tests & Coverage Gate | Java (JaCoCo) + Python (pytest-cov) — 80% line coverage minimum |
| PR Policy Compliance | AI disclosure present, security checklist checked, AI tagging enforced |
| Protected File Guard | Blocks changes to `AGENTS.md`, workflows, `CODEOWNERS` without escalation |

## One-Time Setup

```bash
# Activate the local pre-commit hook (once per developer machine)
git config core.hooksPath .githooks
```

For Java projects, add the JaCoCo plugin to `pom.xml` or `build.gradle` to enable the coverage gate in CI.
See [docs/guardrails-overview.md](docs/guardrails-overview.md) for configuration details.
