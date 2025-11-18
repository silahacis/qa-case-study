#!/usr/bin/env bash

# Always run from repo root
cd "$(dirname "$0")/.." || exit

###############################################
# Local Test Runner for QA Case Study
# Runs:
#  - K6 REST Tests
#  - K6 GraphQL Tests
#  - Playwright Python E2E Tests
###############################################

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo ""
echo "==========================================="
echo "🚀 QA Case Study — Local Test Runner"
echo "==========================================="
echo ""

###############################################
# K6 REST COUNTRIES TEST
###############################################
echo "-------------------------------------------"
echo "🌍 Running K6 REST Countries Tests..."
echo "-------------------------------------------"

REST_FILE="k6/rest/restcountries-smoke.js"

if [ -f "$REST_FILE" ]; then
    k6 run "$REST_FILE" --out json=rest_output.json
    echo -e "${GREEN}✔ REST Countries tests completed${NC}"
else
    echo -e "${RED}❌ File not found: $REST_FILE${NC}"
    exit 1
fi

###############################################
# K6 RICK & MORTY GRAPHQL TEST
###############################################
echo ""
echo "-------------------------------------------"
echo "🧬 Running K6 Rick & Morty GraphQL Tests..."
echo "-------------------------------------------"

GQL_FILE="k6/graphql/rickmorty-characters.js"

if [ -f "$GQL_FILE" ]; then
    k6 run "$GQL_FILE" --out json=graphql_output.json
    echo -e "${GREEN}✔ GraphQL tests completed${NC}"
else
    echo -e "${RED}❌ File not found: $GQL_FILE${NC}"
    exit 1
fi

###############################################
# PLAYWRIGHT TESTS
###############################################
echo ""
echo "-------------------------------------------"
echo "🎭 Running Playwright Python E2E Tests..."
echo "-------------------------------------------"

if [ -d "playwright-python" ]; then
    cd playwright-python || exit
    pytest --disable-warnings --maxfail=1
    echo -e "${GREEN}✔ Playwright tests completed${NC}"
    cd ..
else
    echo -e "${RED}❌ Directory not found: playwright-python${NC}"
    exit 1
fi

###############################################
# FINAL
###############################################
echo ""
echo "==========================================="
echo -e "🎉 ${GREEN}All tests completed successfully!${NC}"
echo "==========================================="
echo ""