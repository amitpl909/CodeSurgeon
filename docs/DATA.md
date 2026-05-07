# Data

## Overview

CodeSurgeon does not require external datasets for core operation. The system works with user-provided code snippets and GitHub repositories. However, optional test datasets are provided for validation.

## Datasets

### Test Dataset: code_snippets.json

**Location:** `data/test_snippets.json` (included in repo)

**Description:** 50 Python and JavaScript code snippets with known bugs for validation

**Format:**
```json
{
  "snippets": [
    {
      "id": "py-001",
      "language": "python",
      "code": "x = 1 || 2",
      "expected_bugs": [
        {"type": "SYNTAX_ERROR", "severity": "CRITICAL", "keywords": ["||", "or"]}
      ]
    }
  ]
}
```

**Size:** ~5 KB

**Provenance:** Internally generated from common anti-patterns

**License:** MIT

### Optional: GitHub PR Test Cases

For testing GitHub integration, use publicly accessible PRs:
- Example: `https://github.com/python/cpython/pull/1234`
- Must be public or user must have access token

## Data Processing

The system processes code data through the following pipeline:

1. **Input:** Code snippet (string) or GitHub PR diff (git format)
2. **Parsing:** Language detection and AST parsing (Python) or regex (JavaScript)
3. **Analysis:** Static + LLM analysis (no external model files)
4. **Output:** Bug report (JSON) and suggested fixes

**Data retention:** Analysis results cached for 1 hour; GitHub diffs never persisted.

## Data Privacy

- **PII:** Code may contain author names, emails. No PII extraction.
- **Sensitive:** Code is sent to LLM API (Anthropic/OpenAI). Use private deployments for proprietary code.
- **Storage:** Local cache only; no remote storage.

## How to Add Custom Test Data

1. Create `data/custom_snippets.json` with your test cases
2. Run: `pytest tests/unit/test_code_analyzer.py --custom-data data/custom_snippets.json`
3. Results saved to `reports/custom_validation.json`

---

**Last updated:** May 7, 2026
