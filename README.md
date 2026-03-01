# AI Coding Agent Guardrails

A reference structure for deploying GitHub Copilot (and similar AI coding assistants)
in engineering teams while maintaining code quality, security, and developer accountability.

## Structure

```
.
├── AGENTS.md                          # Primary AI policy (Copilot reads this)
├── .github/
│   ├── CODEOWNERS                     # Protected file ownership
│   ├── pull_request_template.md       # PR template with AI disclosure checklist
│   └── workflows/
│       └── ai-guardrails-ci.yml      # CI enforcement pipeline
└── docs/
    ├── ai-onboarding.md              # Developer onboarding guide
    ├── code-review-guidelines.md     # How to review AI-assisted PRs
    └── testing-standards.md         # Test requirements for AI-generated code
```

## Guardrail Layers

| Layer | File | Purpose |
|---|---|---|
| **Policy** | `AGENTS.md` | What AI may/may not do; developer obligations |
| **PR Gate** | `pull_request_template.md` | Forces AI disclosure and security checklist |
| **Review** | `docs/code-review-guidelines.md` | Trains reviewers to catch AI-specific issues |
| **Testing** | `docs/testing-standards.md` | Mandates edge case and security test coverage |
| **CI/CD** | `.github/workflows/ai-guardrails-ci.yml` | Automated secret scanning, SAST, coverage gates |
| **Ownership** | `.github/CODEOWNERS` | Protects policy files from unauthorized changes |
| **Onboarding** | `docs/ai-onboarding.md` | Teaches developers to use Copilot responsibly |

## Adapting to Your Stack

1. Update the CI workflow's language-specific steps for your tech stack
2. Set coverage thresholds in `testing-standards.md` to match your team's targets
3. Update `CODEOWNERS` with your actual GitHub team handles
4. Add your internal wiki links in `ai-onboarding.md`
5. Customize the prohibited patterns in `AGENTS.md` for your security requirements
