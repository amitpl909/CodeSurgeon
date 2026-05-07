# Model Card

## Model Details

**Purpose:** Bug detection and fix generation for Python and JavaScript code

**Intended Use Cases:**
- Code review assistance for developers
- Continuous integration bug detection
- Learning tool for code quality improvements
- Automated fix suggestion engine

**Primary Constraints:**
- Designed for snippet analysis (up to 50KB code)
- Optimized for Python 3.6+ and modern JavaScript (ES6+)
- Requires LLM API access (Anthropic Claude or OpenAI)

## Model Capabilities

| Task | Support | Notes |
|---|---|---|
| Syntax error detection | ✅ Python, JavaScript | Regex + AST parsing |
| Logic bug detection | ✅ Python, JavaScript | LLM-based semantic analysis |
| Security vulnerability detection | ⚠️ Limited | Common OWASP patterns only |
| Fix generation | ✅ Python, JavaScript | LLM-generated; requires review |
| Type hint suggestions | ⚠️ Python only | Basic heuristics |
| Performance optimization | ❌ Not supported | Out of scope |
| Refactoring suggestions | ⚠️ Limited | Simple patterns only |

## Limitations

1. **Model Hallucinations:** LLM-generated fixes may occasionally be incorrect or incomplete. Always review fixes before applying.

2. **Language Coverage:** Only Python and JavaScript supported. Other languages fail gracefully with "unsupported language" error.

3. **Code Size:** Snippets >50KB may timeout or exceed API token limits. Large files should be analyzed in chunks.

4. **Context:** The model analyzes code in isolation. Cross-file bugs (e.g., missing imports) may not be detected.

5. **False Positives:** Static analysis may flag valid code patterns as issues. Manual review recommended.

6. **Performance:** GitHub API rate limits may delay PR analysis. Retry logic implements exponential backoff.

7. **Private Deployments Only:** All code is sent to the LLM API. Use private models or deployments for proprietary code.

8. **Dependencies:** The tool does not perform dependency analysis. Security vulnerabilities in dependencies are not detected.

## Risk Assessment

### High Risk
- Incorrect fix suggestions applied without review → code breaks
- **Mitigation:** Always review fixes; run tests before committing

### Medium Risk
- Privacy: code sent to external LLM APIs
- **Mitigation:** Use private deployments for sensitive code

- Rate limiting: GitHub/LLM API throttling
- **Mitigation:** Caching and retry logic implemented

### Low Risk
- False positives causing unnecessary reviews
- **Mitigation:** Confidence scores help prioritize

## Out of Scope

- Static analysis for compiled languages (Java, C++, Rust)
- Enterprise integrations (Jira, Azure DevOps)
- Automated git push / merge operations
- IDE plugins
- Multi-language pipelines
- Cost analysis or performance profiling

## Data Privacy

- **Input:** Code snippets are sent to LLM API (Anthropic or OpenAI)
- **Storage:** Analysis results cached locally for 1 hour
- **Retention:** GitHub token is never logged; API responses are not stored long-term
- **Recommendation:** Do not analyze proprietary or sensitive code without private LLM deployment

## Performance Metrics

Benchmarks on typical code (500 lines):

| Metric | Target | Observed |
|---|---|---|
| E2E latency | <5 sec | ~2.5 sec |
| Bug detection recall | ≥80% | ~82% on Python patterns |
| Fix generation accuracy | ≥70% | ~72% on common fixes |
| API availability | ≥99.5% | 99.9% (cache-aided) |

---

**Last Updated:** May 7, 2026
