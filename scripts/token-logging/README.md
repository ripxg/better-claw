# Token Logging System (v2)

**Complete token usage tracking with session-end logging and register-based reporting.**

## Problem

The default OpenClaw token usage reporting only captures **active sessions** at the time of polling. This misses:
- ✗ Completed sessions that have already ended
- ✗ Subagent sessions that finish before the report runs
- ✗ Short-lived sessions (< 1 hour)
- ✗ Accurate agent-by-agent breakdown

**Result:** Your daily token reports underreport actual usage, sometimes significantly.

## Solution

This system implements **session-end logging** where every agent (coordinator + subagents) logs their token usage to a shared register before exiting. The daily report then merges:
1. **Register entries** (completed sessions)
2. **Active sessions** (currently running)

Deduplication by `session_key` prevents double-counting.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Session-End Hook (in AGENTS.md)                        │
│ ↓                                                       │
│ session_status → extract tokens → log-session-tokens.sh │
│ ↓                                                       │
│ token-usage-register.jsonl (append-only)               │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│ Daily Cron Job (20:00 UTC)                             │
│ ↓                                                       │
│ daily-token-report-v2.py                               │
│ ├─ Read register entries (last 24h)                    │
│ ├─ Fetch active sessions (OpenClaw API)                │
│ ├─ Merge & deduplicate by session_key                  │
│ └─ Generate report → Send to Telegram/Discord/Slack    │
└─────────────────────────────────────────────────────────┘
```

## Files

```
scripts/token-logging/
├── daily-token-report-v2.py       # Main report generator
├── log-session-tokens.sh          # Helper script for agents to log tokens
├── token-usage-register.example.jsonl  # Example register format
├── README.md                      # This file
└── AGENTS.md.patch                # Session-end logging protocol (see below)
```

## Installation

### 1. Copy Scripts

```bash
# From better-claw root
cp scripts/token-logging/*.py ~/clawd/tools/
cp scripts/token-logging/*.sh ~/clawd/tools/
chmod +x ~/clawd/tools/*.py ~/clawd/tools/*.sh
```

### 2. Create Register File

```bash
touch ~/clawd/data/token-usage-register.jsonl
echo '# Token Usage Register (JSONL)' > ~/clawd/data/token-usage-register.jsonl
```

### 3. Update AGENTS.md

Add the **Session-End Token Logging** section to your `AGENTS.md`:

```markdown
## 📊 Session-End Token Logging (CRITICAL)

**Every session MUST log token usage before exit** to the shared register for accurate daily reporting.

### When to Log
- When you receive a final message indicating session end
- When your task is complete and you're awaiting cleanup
- Before a long idle period (>1 hour)
- **Automatically on graceful session termination**

### How to Log

\`\`\`bash
# Get session stats from session_status tool
# Extract: model, tokens_input, tokens_output, cost
# Then append to register (atomic write):

cat >> /home/ubuntu/clawd/data/token-usage-register.jsonl <<EOF
{"timestamp":"$(date -u +%Y-%m-%dT%H:%M:%SZ)","session_key":"YOUR_SESSION_KEY","agent_id":"YOUR_AGENT_ID","model":"MODEL_NAME","tokens_input":INPUT_COUNT,"tokens_output":OUTPUT_COUNT,"cost":COST_VALUE}
EOF
\`\`\`

### Example Entry
\`\`\`json
{"timestamp":"2026-02-05T20:00:00Z","session_key":"abc123","agent_id":"backend-engineer","model":"anthropic/claude-sonnet-4-5","tokens_input":15000,"tokens_output":3000,"cost":0.045}
\`\`\`

### Register Location
- **Main workspace**: `/home/ubuntu/clawd/data/token-usage-register.jsonl`
- **Subagent sandbox**: Same path (accessible from all agents)

### Important Notes
- **Append-only** — never truncate or overwrite
- **Atomic writes** — use `>>` or atomic file operations
- **No duplicates** — check if session_key already logged (optional, but preferred)
- **JSON Lines format** — one complete JSON object per line
- **Graceful failure** — if write fails, continue without blocking session end

### Verification
After logging, you can verify:
\`\`\`bash
tail -1 /home/ubuntu/clawd/data/token-usage-register.jsonl | jq .
\`\`\`

### Monthly Cleanup
The daily report script handles rotation:
- Archive entries older than 30 days to `token-usage-register-YYYY-MM.jsonl.gz`
- Keep current month + last month in active register
```

**Place this section BEFORE the "Development Rules" section in AGENTS.md.**

### 4. Sync Agent Context

If you use subagents, sync their context files:

```bash
cd ~/clawd
./scripts/sync-agent-context.sh
```

### 5. Import Cron Job

```bash
openclaw cron add --job "$(cat ~/better-claw/jobs/analytics/token-usage-daily.json)"
```

Update the `to` field with your Telegram ID:

```bash
openclaw cron update --job-id <JOB_ID> --patch '{"payload": {"to": "YOUR_TELEGRAM_ID"}}'
```

### 6. Enable the Job

```bash
openclaw cron update --job-id <JOB_ID> --patch '{"enabled": true}'
```

## Usage

### Manual Test

Log a test session:

```bash
cd ~/clawd
./tools/log-session-tokens.sh "test-001" "main" "anthropic/claude-sonnet-4-5" 1000 500 0.0075
```

Verify:

```bash
tail -1 ~/clawd/data/token-usage-register.jsonl
```

### Generate Report Manually

```bash
cd ~/clawd
python3 tools/daily-token-report-v2.py
```

Send to Telegram:

```bash
python3 tools/daily-token-report-v2.py --send-telegram
```

With rotation:

```bash
python3 tools/daily-token-report-v2.py --send-telegram --rotate
```

## Report Format

```
📊 DAILY TOKEN USAGE REPORT
📅 2026-02-06

Summary
┌ Total Tokens: 52,695
├ Input: 20,000 (38.0%)
├ Output: 32,695 (62.0%)
├ Cost: $0.1425
└ Sessions: 12

By Model
• claude-sonnet-4-5: 40,000 tokens (8 sessions)
• claude-opus-4-5: 10,000 tokens (2 sessions)
• glm-4.7: 2,695 tokens (2 sessions)

By Agent
• main: 35,000 tokens (8 sessions)
• backend-engineer: 12,000 tokens (3 sessions)
• frontend-engineer: 5,695 tokens (1 sessions)

Hourly Breakdown (Last 24 Hours)
20:00: 15,000 tokens (3 sessions) | $0.0450
19:00: 8,000 tokens (2 sessions) | $0.0240
...

📁 Dataset: /home/ubuntu/clawd/data/token-usage-daily.json
Generated at 20:00 UTC
```

## Pricing

Update pricing in `daily-token-report-v2.py`:

```python
PRICING = {
    "claude-sonnet-4-5": {"input": 3.00, "output": 15.00},
    "claude-opus-4-5": {"input": 15.00, "output": 75.00},
    "claude-haiku-4-5": {"input": 0.25, "output": 1.25},
    "glm-4.7": {"input": 0.10, "output": 0.10},
}
```

Prices are per 1M tokens in USD.

## Register Format

**JSON Lines (JSONL)** — one JSON object per line:

```json
{"timestamp":"2026-02-05T20:00:00Z","session_key":"abc123","agent_id":"main","model":"anthropic/claude-sonnet-4-5","tokens_input":15000,"tokens_output":3000,"cost":0.045}
{"timestamp":"2026-02-05T21:30:00Z","session_key":"def456","agent_id":"backend-engineer","model":"glm-4.7","tokens_input":5000,"tokens_output":2000,"cost":0.007}
```

### Schema

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | ISO8601 UTC | When the session ended |
| `session_key` | string | Unique session identifier |
| `agent_id` | string | Agent that ran the session (main, backend-engineer, etc.) |
| `model` | string | Model used (with provider prefix) |
| `tokens_input` | int | Input tokens consumed |
| `tokens_output` | int | Output tokens generated |
| `cost` | float | Estimated cost in USD |

## Rotation

The daily report automatically rotates entries older than 2 months when run with `--rotate`:

```bash
python3 tools/daily-token-report-v2.py --rotate
```

Archived entries are removed from the active register. To keep historical data, manually archive before rotation:

```bash
cp ~/clawd/data/token-usage-register.jsonl ~/clawd/data/archive/token-usage-register-$(date +%Y-%m).jsonl
```

## Troubleshooting

### Report shows 0 sessions

**Cause:** No sessions logged to register yet, and no active sessions.

**Fix:** Wait for sessions to complete and log, or manually test with `log-session-tokens.sh`.

### Duplicate entries

**Cause:** Session logged multiple times.

**Fix:** `log-session-tokens.sh` checks for duplicates, but if you manually append, ensure session_key is unique.

### Register file not found

**Cause:** Register file doesn't exist.

**Fix:**
```bash
touch ~/clawd/data/token-usage-register.jsonl
```

### Timezone mismatch in timestamps

**Cause:** Script uses UTC for all timestamps.

**Fix:** This is intentional. Display timezone can be customized in report formatting if needed.

### Agent not logging sessions

**Cause:** AGENTS.md not updated or agent context not synced.

**Fix:**
1. Update AGENTS.md with session-end logging protocol
2. Run `./scripts/sync-agent-context.sh`
3. Verify agents have the updated AGENTS.md in their workspace

## Integration with Existing Reports

If you already have `daily-token-report.py` (v1), you can:

1. **Run both** during transition period (v1 for historical comparison, v2 for accuracy)
2. **Migrate** by disabling v1 cron job and enabling v2
3. **Compare** reports to verify v2 is capturing all sessions

The v2 report includes a source field in the dataset to distinguish register vs active sessions.

## Contributing

Found a bug or have a feature request? Open an issue on the [Better Claw GitHub](https://github.com/ripxg/better-claw).

## License

MIT License - see LICENSE file in the repository root.

## Credits

Developed by [@ripxg](https://github.com/ripxg) as part of the Better Claw project.
