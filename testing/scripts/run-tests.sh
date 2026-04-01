#!/bin/bash
# Run local tests

set -e

TEST_TYPE=${1:-all}
VERBOSE=${2:--v}

echo "Running $TEST_TYPE tests..."

case $TEST_TYPE in
    unit)
        pytest tests/unit/ $VERBOSE
        ;;
    integration)
        pytest tests/integration/ $VERBOSE
        ;;
    smoke)
        pytest tests/smoke/ $VERBOSE
        ;;
    all)
        pytest tests/ $VERBOSE --cov=app/src --cov-report=html
        echo "✓ Coverage report generated in htmlcov/index.html"
        ;;
    *)
        echo "Usage: $0 {unit|integration|smoke|all} [-v|-vv]"
        exit 1
        ;;
esac
