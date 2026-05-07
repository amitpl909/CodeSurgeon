#!/bin/bash
# Preflight checks - local TA dry-run validation

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Running TA Preflight Checks...${NC}\n"

# 1. Check directory structure
echo "Checking directory structure..."
required_dirs=(
    "src/myproject"
    "tests/unit"
    "tests/integration"
    "tests/user_stories"
    "tests/edge"
    "tests/load"
    "docs"
    "grading"
    "reports"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "  ${GREEN}✓${NC} $dir"
    else
        echo -e "  ${RED}✗${NC} $dir (MISSING)"
        exit 1
    fi
done

# 2. Check required files
echo -e "\nChecking required files..."
required_files=(
    "pyproject.toml"
    "Makefile"
    "Dockerfile"
    "docker-compose.yml"
    ".env.example"
    ".gitignore"
    "docs/SPEC.md"
    "docs/STORIES.md"
    "docs/README.md"
    "grading/manifest.yaml"
    "grading/traceability.yaml"
    "grading/grade.py"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
    else
        echo -e "  ${YELLOW}⚠${NC}  $file (WARNING: may be missing)"
    fi
done

# 3. Run linting
echo -e "\nRunning linting..."
if command -v ruff &> /dev/null; then
    if ruff check src/myproject tests --select E,W,F > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} Code lint passed"
    else
        echo -e "  ${YELLOW}⚠${NC}  Lint warnings found (non-blocking)"
    fi
else
    echo -e "  ${YELLOW}⚠${NC}  ruff not installed (skip)"
fi

# 4. Test imports
echo -e "\nTesting imports..."
if python -c "from src.myproject import api" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Module imports work"
else
    echo -e "  ${RED}✗${NC} Module imports failed"
    exit 1
fi

# 5. Summary
echo -e "\n${GREEN}✓ Preflight checks passed!${NC}"
echo -e "  Ready for: docker compose up && make test"
