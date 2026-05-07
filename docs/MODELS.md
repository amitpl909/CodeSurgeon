# Models

## Overview

CodeSurgeon does not use pre-trained ML models. Instead, it leverages LLM APIs (Anthropic Claude or OpenAI GPT) for intelligent bug detection and fix generation.

## LLM Configuration

### Supported Models

| Provider | Model | Version | Use Case |
|---|---|---|---|
| Anthropic | Claude 3 Opus | latest | Bug detection + fix generation (recommended) |
| Anthropic | Claude 3 Sonnet | latest | Alternative (faster, cheaper) |
| OpenAI | GPT-4 | latest | Bug detection + fix generation |
| OpenAI | GPT-3.5-turbo | latest | Alternative (faster, cheaper) |

### Configuration

Set in `.env` file:

```bash
ANTHROPIC_API_KEY=sk-ant-...  # If using Claude
OPENAI_API_KEY=sk-...          # If using GPT
LLM_PROVIDER=anthropic         # or "openai"
LLM_MODEL=claude-3-opus-20240229
```

### API Requirements

- **Anthropic:** API token from https://console.anthropic.com/
- **OpenAI:** API token from https://platform.openai.com/account/api-keys/

## Prompts and Templates

### Bug Detection Prompt

Stored in `src/myproject/prompts/detect_bugs.txt`:

```
You are a code review expert. Analyze the following code for bugs, vulnerabilities, and quality issues.

Code:
{code}

Language: {language}
Context: {context}

Respond in JSON format with an array of bugs. Each bug must have:
- type (e.g., SYNTAX_ERROR, LOGIC_BUG, BEST_PRACTICE)
- severity (CRITICAL, HIGH, MEDIUM, LOW)
- line_number
- description (1-2 sentences)
- confidence (0.0-1.0)

Response:
```

### Fix Generation Prompt

Stored in `src/myproject/prompts/generate_fix.txt`:

```
You are an expert Python/JavaScript developer. Generate a fix for the following bug.

Original code:
{code}

Bug:
- Type: {bug_type}
- Description: {description}
- Line: {line}

Provide:
1. Fixed code (between ```code blocks)
2. Explanation (why the fix works)
3. 2-3 alternative approaches (briefly)

Response:
```

## Model Checkpoints

**Note:** CodeSurgeon does not save model checkpoints. API calls are stateless.

To fine-tune the system:
1. Collect feedback on generated fixes (accuracy, usefulness)
2. Update prompts in `src/myproject/prompts/` directory
3. Re-run validation: `make test`

## Cost and Performance

### Latency
- Bug detection: ~1.5-2 sec per call (includes network)
- Fix generation: ~1-2 sec per fix

### Cost (estimated)
- $0.01-0.05 per analysis (varies by code size and model)
- Use Claude 3 Sonnet or GPT-3.5-turbo for cost optimization

### Optimization
- Enable caching: 24h TTL for GitHub PRs, 1h TTL for snippets
- Batch requests: Analyze multiple files per API call (not yet implemented)
- Use cheaper models for non-critical paths

---

**Last updated:** May 7, 2026
