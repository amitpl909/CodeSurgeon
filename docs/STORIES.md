# User Stories

Every story below has a stable ID, a Given/When/Then statement, and numbered manual steps the TA can follow against the live `docker compose up` system. The TA scores Application Functionality (20 points) by walking these stories against the live UI.

Format conventions:
- Story IDs are US-NN (US-01, US-02, ...)
- Every story has a corresponding test in `tests/user_stories/test_us_NN.py`
- Stories that exercise error paths are marked with [ERROR PATH]
- At least 2 stories must be error path stories

---

## US-01: User submits code snippet and receives bug analysis

**As a** software developer
**I want** to paste code into the UI and get immediate bug detection
**So that** I can identify issues before committing.

**Acceptance criteria (Given / When / Then):**

> Given the application is running,
> When the user enters Python code "x = 1 || 2" and clicks "Analyze",
> Then the response shows 1 detected bug (severity CRITICAL) within 5 seconds,
> with description containing "||" and "or operator".

**Manual walkthrough steps:**

1. Open http://localhost:8000 in browser.
2. Verify the page shows a CodeSurgeon header and "Analyze Code" input form.
3. Select language: Python.
4. Paste code: `def calc(a):\n    x = 1 || 2\n    return x`
5. Click "Analyze Code" button.
6. Within 5 seconds, observe:
   - Analysis Summary showing "1 Total", "1 Critical"
   - Bug list showing one CRITICAL bug with description mentioning "||"
7. Click "View" on the detected bug.
8. Observe bug details panel showing:
   - Type: SYNTAX_ERROR
   - Severity: CRITICAL
   - File: main.py
   - Line: 2
   - Description: "Using || instead of 'or' operator in Python"

**Expected output:** Analysis result JSON with 1 bug of type SYNTAX_ERROR, severity CRITICAL.

---

## US-02: User views bug details and generates fixes

**As a** developer
**I want** to click on a detected bug and see detailed fixes
**So that** I can understand the issue and apply the correction.

**Acceptance criteria (Given / When / Then):**

> Given a bug is detected and displayed in the list,
> When the user clicks "View" on the bug,
> Then the bug detail panel appears with a "🤖 Generate Fix" button,
> and clicking the button returns a primary fix with code and explanation.

**Manual walkthrough steps:**

1. Complete US-01 (have a bug detected and listed).
2. In the bug list, locate the CRITICAL bug row.
3. Click the "View" button on the right.
4. Observe the "Bug Details" panel appears with:
   - Type: SYNTAX_ERROR
   - Severity: CRITICAL
   - File: main.py
   - Line: 2
   - Description: "Using || instead of 'or' operator in Python"
   - Confidence bar (should show ~0.95)
5. Click the "🤖 Generate Fix" button.
6. Wait <3 seconds.
7. Observe the "Primary Fix" section appears with:
   - Code block showing corrected code: `x = 1 or 2`
   - Explanation: "Changed || operator to 'or'..."
8. Verify "Alternative Solutions" section shows at least 1 option.
9. Click "Copy" button next to primary fix; verify clipboard notification.

**Expected output:** Fix object with primary fix code and explanation text.

---

## US-03 [ERROR PATH]: User enters empty code and sees validation error

**As a** user
**I want** to receive clear feedback when I submit empty input
**So that** I know what to fix before retrying.

**Acceptance criteria (Given / When / Then):**

> Given the application is running,
> When the user clicks "Analyze Code" without entering any code,
> Then an inline error message appears stating "Please enter some code",
> and no API call is made.

**Manual walkthrough steps:**

1. Open http://localhost:8000 in browser.
2. Leave the "Code Snippet" textarea empty.
3. Click "Analyze Code" button.
4. Observe an error message appears inline, saying "Please enter some code" or similar.
5. Verify no spinner or loading state appears.
6. Open browser dev tools (F12), Network tab.
7. Confirm no request was sent to `/api/v1/analyze`.
8. Try again with actual code; verify the error clears and analysis proceeds.

**Expected output:** Client-side validation; 400 Bad Request if sent to API.

---

## US-04 [ERROR PATH]: User submits code with syntax error and sees appropriate message

**As a** developer
**I want** to know when my code cannot be analyzed due to syntax errors
**So that** I can fix the syntax before analysis.

**Acceptance criteria (Given / When / Then):**

> Given the application is running,
> When the user enters invalid Python syntax "def f(: pass",
> Then an error message appears stating the code has syntax errors,
> and analysis does not proceed.

**Manual walkthrough steps:**

1. Open http://localhost:8000 in browser.
2. Select language: Python.
3. Paste invalid code: `def f(: pass`
4. Click "Analyze Code".
5. Observe within 2 seconds:
   - Error message appears (inline or toast)
   - Message contains text about "syntax" or "invalid" or "parse error"
   - No analysis results are shown
6. Fix the code to `def f(): pass`
7. Click "Analyze Code" again.
8. Verify analysis proceeds normally (no SYNTAX_ERROR for the code structure itself; only logical bugs are detected).

**Expected output:** 400 Bad Request with error message about invalid syntax.

---

## US-05: User submits GitHub PR URL for analysis

**As a** DevOps engineer
**I want** to analyze an entire GitHub pull request
**So that** I can review all changes in one shot.

**Acceptance criteria (Given / When / Then):**

> Given the application is running and a valid GitHub token is configured,
> When the user clicks the "GitHub PR" tab, enters a PR URL "https://github.com/owner/repo/pull/123",
> Then the application fetches the PR, analyzes all changed files, and returns aggregated bugs
> within 10 seconds.

**Manual walkthrough steps:**

1. Open http://localhost:8000 in browser.
2. Look for input form; select "GitHub PR" mode (radio button or tab).
3. Enter a valid GitHub PR URL (e.g., a public repo PR, or your own test PR).
4. Click "Analyze" button.
5. Wait 5-10 seconds for GitHub API call and analysis.
6. Observe:
   - Summary shows total bugs across all changed files
   - Bug list shows bugs from multiple files with file paths
   - Each bug shows the file name, line number, and description
7. Click on one bug; verify the bug detail panel shows the correct file context.

**Expected output:** Aggregated analysis result from multiple files in the PR.

---

## US-06: User copies fix code to clipboard

**As a** developer
**I want** to copy the suggested fix code directly to my clipboard
**So that** I can paste it into my editor or commit.

**Acceptance criteria (Given / When / Then):**

> Given a fix is displayed in the UI,
> When the user clicks the "Copy" button next to the fix code,
> Then the fix code is copied to the system clipboard,
> and a confirmation message appears (e.g., "✓ Copied!").

**Manual walkthrough steps:**

1. Complete US-02 (have a fix displayed).
2. In the "Primary Fix" section, locate the "Copy" button.
3. Click "Copy".
4. Observe a confirmation message appears briefly (e.g., "✓ Copied!", tooltip).
5. Open a text editor (e.g., Notepad, VS Code).
6. Paste (Ctrl+V or Cmd+V).
7. Verify the fixed code appears: `x = 1 or 2`.

**Expected output:** Clipboard contains the fix code; UI shows confirmation.

---

## US-07 [ERROR PATH]: API returns timeout error for slow LLM

**As a** user
**I want** to see a timeout error if the LLM is slow
**So that** I know to retry or contact support.

**Acceptance criteria (Given / When / Then):**

> Given the LLM API is slow or unreachable (timeout >30 seconds),
> When the user analyzes code,
> Then an error message appears stating "LLM service unavailable; try again"
> and the UI remains responsive (no hang).

**Manual walkthrough steps:**

1. (Optional: simulate by stopping LLM service or deleting API key.)
2. Open http://localhost:8000 in browser.
3. Paste code: `x = 1 || 2`
4. Click "Analyze Code".
5. Wait up to 30 seconds.
6. Observe error message appears: "LLM service unavailable" or similar.
7. Verify the UI is still responsive (no spinning spinner, no browser hang).
8. Try again with a different code snippet; verify retry succeeds (if LLM is back).

**Expected output:** 503 Service Unavailable with error message.

---

## US-08: User views analysis metrics (time, bug counts by severity)

**As a** user
**I want** to see summary statistics about the analysis
**So that** I can understand the scope of issues at a glance.

**Acceptance criteria (Given / When / Then):**

> Given an analysis is complete,
> When the user views the results,
> Then the Summary panel shows:
> - Total bug count
> - Counts by severity (Critical, High, Medium, Low)
> - Analysis time in milliseconds.

**Manual walkthrough steps:**

1. Complete US-01 (have an analysis result).
2. Observe the "Analysis Summary" panel below the input form.
3. Verify it shows:
   - "1 Total" (or actual count)
   - "1 Critical" (or actual count)
   - "0 High", "0 Medium", "0 Low" (or actual counts)
   - "Analysis Time: 250 ms" (or actual ms)
4. Analyze multiple code snippets; verify counts update correctly.

**Expected output:** Summary statistics displayed in a grid/card layout.

---

## US-09: User analyzes code without GitHub token (missing optional credential)

**As a** a developer using code snippets
**I want** to analyze code even without a GitHub token
**So that** I can use the tool for snippet analysis.

**Acceptance criteria (Given / When / Then):**

> Given the application is running (even with GITHUB_TOKEN missing from .env),
> When the user chooses "Code Snippet" mode and analyzes code,
> Then the analysis succeeds and returns bugs.
> (GitHub PR mode fails gracefully if token is missing.)

**Manual walkthrough steps:**

1. Verify `.env` does not have GITHUB_TOKEN set (or is empty).
2. Open http://localhost:8000 in browser.
3. Select "Code Snippet" mode (default).
4. Paste code: `x = 1 || 2`
5. Click "Analyze Code".
6. Verify analysis succeeds within 5 seconds.
7. Observe bugs detected and fixes generated normally.
8. (Optional: try GitHub PR mode; should fail with message "GitHub token not configured".)

**Expected output:** Code snippet analysis works; GitHub mode gracefully fails if token is missing.

---

## Appendix: Manual Testing Checklist

Before submission, manually verify:

- [ ] All 9 user stories pass on the live app (docker compose up)
- [ ] All error messages are clear and actionable
- [ ] No unhandled exceptions or 500 errors
- [ ] API responds in <5 seconds for typical code (500 lines)
- [ ] Load test `make loadtest` passes (>50 concurrent users)
- [ ] Unit tests pass: `pytest tests/unit`
- [ ] Integration tests pass: `pytest tests/integration`
- [ ] All user story tests pass: `pytest tests/user_stories`
