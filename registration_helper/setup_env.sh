#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PROJECT_ROOT="$SCRIPT_DIR"

export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

echo "PYTHONPATH set to: $PYTHONPATH"
