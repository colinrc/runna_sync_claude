#!/bin/bash
# run.sh - Run the converter locally

set -e

echo "==================================="
echo "Runna to Intervals.icu Converter"
echo "Local Execution"
echo "==================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Starting conversion..."
echo ""

# Run with command line arguments or environment variables
if [ -n "$ICS_URL" ]; then
    # Use environment variable
    python3 runna_to_intervals.py \
        --url "$ICS_URL" \
        --output "${OUTPUT_PATH:-intervals_icu_workouts.json}" \
        --log-level "${LOG_LEVEL:-INFO}" \
        ${LOG_JSON:+--log-json}
elif [ $# -gt 0 ]; then
    # Use command line arguments
    python3 runna_to_intervals.py "$@"
else
    # Interactive mode
    python3 runna_to_intervals.py --interactive
fi

echo ""
echo "==================================="
echo "Conversion complete!"
echo "==================================="
