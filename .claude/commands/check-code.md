---
allowed-tools: all
description: Verify code quality and fix all issues
---

# Code Quality Check (FastAPI + Flutter)

Fix all issues found during quality verification. Do not just report problems.

## Workflow

1. **Identify** - Run all validation commands
2. **Fix** - Address every issue found
3. **Verify** - Re-run until all checks pass

---

## Validation Commands

### 🔹 Python (FastAPI)
- **Lint & Format**:  
  - `ruff check .`  
  - `ruff format .`  

### 🔹 Flutter (Dart)
- **Lint**:  
  - `dart analyze`  
- **Format**:  
  - `dart format .`  

## Parallel Fixing Strategy

When multiple issues exist, spawn agents to fix in parallel:

