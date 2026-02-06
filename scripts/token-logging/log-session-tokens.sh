#!/bin/bash
# Helper script for agents to log session token usage to the shared register
# Usage: ./log-session-tokens.sh <session_key> <agent_id> <model> <tokens_input> <tokens_output> <cost>

set -e

SESSION_KEY="${1:-unknown}"
AGENT_ID="${2:-main}"
MODEL="${3:-unknown}"
TOKENS_INPUT="${4:-0}"
TOKENS_OUTPUT="${5:-0}"
COST="${6:-0.0}"

REGISTER="/home/ubuntu/clawd/data/token-usage-register.jsonl"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Ensure register exists
touch "$REGISTER"

# Check if session already logged (avoid duplicates)
if grep -q "\"session_key\":\"$SESSION_KEY\"" "$REGISTER" 2>/dev/null; then
    echo "⚠️  Session $SESSION_KEY already logged, skipping"
    exit 0
fi

# Append entry atomically
echo "{\"timestamp\":\"$TIMESTAMP\",\"session_key\":\"$SESSION_KEY\",\"agent_id\":\"$AGENT_ID\",\"model\":\"$MODEL\",\"tokens_input\":$TOKENS_INPUT,\"tokens_output\":$TOKENS_OUTPUT,\"cost\":$COST}" >> "$REGISTER"

echo "✅ Logged session $SESSION_KEY to token register"
echo "   Model: $MODEL | Tokens: $TOKENS_INPUT in, $TOKENS_OUTPUT out | Cost: \$$COST"
