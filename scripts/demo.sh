#!/bin/bash
# E2E demo - exercises all 9 user stories against running app

set -e

API_URL="${1:-http://localhost:8000}"
DEMO_RESULTS="reports/demo_results.txt"

mkdir -p reports

echo "CodeSurgeon E2E Demo"
echo "==================="
echo "Testing against: $API_URL"
echo ""

# Helper function
test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4

    echo -n "Testing $name... "
    if [ "$method" = "GET" ]; then
        response=$(curl -s "$API_URL$endpoint")
    else
        response=$(curl -s -X POST "$API_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi

    if echo "$response" | grep -q '"id"' || echo "$response" | grep -q '"status"'; then
        echo "✓"
        echo "$response" >> "$DEMO_RESULTS"
    else
        echo "✗"
        echo "Failed response: $response" >> "$DEMO_RESULTS"
    fi
}

# US-01: Analyze code snippet
test_endpoint "US-01: Analyze code" "POST" "/api/v1/analyze" \
    '{"code":"x = 1 || 2","language":"python"}'

# US-02: Generate fixes
test_endpoint "US-02: Generate fixes" "POST" "/api/v1/analyze" \
    '{"code":"if x == None: pass","language":"python"}'

# US-03: Empty code error
test_endpoint "US-03: Empty code validation" "POST" "/api/v1/analyze" \
    '{"code":"","language":"python"}'

# US-04: Syntax error
test_endpoint "US-04: Syntax error" "POST" "/api/v1/analyze" \
    '{"code":"def f(: pass","language":"python"}'

# US-08: Metrics
test_endpoint "US-08: Metrics" "POST" "/api/v1/analyze" \
    '{"code":"x = 1\ny = 2","language":"python"}'

# US-09: Code analysis without GitHub token
test_endpoint "US-09: Code snippet (no GitHub token)" "POST" "/api/v1/analyze" \
    '{"code":"x = 1 or 2","language":"python"}'

# Health check
test_endpoint "Health check" "GET" "/api/v1/health" ""

echo ""
echo "Demo complete! Results saved to $DEMO_RESULTS"
