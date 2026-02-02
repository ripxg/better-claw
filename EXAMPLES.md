# Examples: How to Use Better Claw Jobs

This guide shows practical examples of importing, customizing, and using Better Claw jobs.

## Quick Start: Your First Job

Let's start with the simplest and most useful job: **Daily Workflow Feedback**.

### 1. View the Job

```bash
# Clone the repo
git clone https://github.com/ripxg/better-claw.git
cd better-claw

# Read the job file
cat jobs/feedback/daily-workflow-feedback.json
```

### 2. Import the Job

There are two ways to import:

**Method A: Using OpenClaw CLI** (if available)
```bash
openclaw cron add --file jobs/feedback/daily-workflow-feedback.json
```

**Method B: Using the cron tool in a session**

In your OpenClaw chat:
```
Add this cron job: [paste the JSON from the file]
```

Or ask your agent:
```
Import the daily-workflow-feedback job from better-claw/jobs/feedback/
```

### 3. Customize Before Enabling

Before enabling, adjust to your preferences:

```bash
# List all jobs (including disabled)
openclaw cron list --include-disabled

# Update the schedule to your timezone
openclaw cron update --job-id <id> --patch '{
  "schedule": {
    "kind": "cron",
    "expr": "0 17 * * *",
    "tz": "America/New_York"
  }
}'

# Enable the job
openclaw cron update --job-id <id> --patch '{"enabled": true}'
```

## Example Workflows

### Workflow 1: Solo Developer Productivity

**Goal**: Track projects, optimize costs, improve communication

**Jobs to enable:**
1. `daily-workflow-feedback` - Daily reflection
2. `weekly-reflection` - Weekly summary
3. `token-usage-daily` - Cost tracking
4. `project-owner` - For each active project
5. `security-audit` - Security monitoring

**Setup:**
```bash
# Import all jobs
for job in jobs/feedback/daily-workflow-feedback.json \
           jobs/feedback/weekly-reflection.json \
           jobs/analytics/token-usage-daily.json \
           jobs/security/security-audit.json; do
  openclaw cron add --file $job
done

# Customize project-owner for your main project
# (Edit the JSON first to replace PROJECT_NAME, etc.)
openclaw cron add --file jobs/projects/project-owner-custom.json
```

### Workflow 2: Team Collaboration

**Goal**: Maintain memory, coordinate work, track trends

**Jobs to enable:**
1. `learning-preference-calibration` - Monthly alignment
2. `memory-consolidation` - Keep memory current
3. `communication-audit` - Improve clarity
4. `session-summary` - Track usage patterns

### Workflow 3: New User Onboarding

**Goal**: Learn OpenClaw capabilities gradually

**Jobs to enable:**
1. `tool-discovery` - Weekly intro to new tools
2. `skill-learning-prompt` - Bi-weekly deep dive
3. `daily-workflow-feedback` - Build good habits

**Timeline:**
- Week 1-2: Just `daily-workflow-feedback`
- Week 3+: Add `tool-discovery`
- Month 2+: Add `skill-learning-prompt`

## Customization Examples

### Example 1: Adjust Schedule

Original schedule (3pm UTC daily):
```json
{
  "schedule": {
    "kind": "cron",
    "expr": "0 15 * * *",
    "tz": "UTC"
  }
}
```

Change to 5pm in your timezone:
```bash
openclaw cron update --job-id <id> --patch '{
  "schedule": {
    "kind": "cron",
    "expr": "0 17 * * *",
    "tz": "America/New_York"
  }
}'
```

### Example 2: Change Delivery Method

Original (system event to main session):
```json
{
  "sessionTarget": "main",
  "payload": {
    "kind": "systemEvent",
    "text": "..."
  }
}
```

Change to Telegram notification:
```bash
openclaw cron update --job-id <id> --patch '{
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "...",
    "deliver": true,
    "channel": "telegram"
  }
}'
```

### Example 3: Clone Project Owner for Multiple Projects

Create custom job files for each project:

**my-frontend.json:**
```json
{
  "name": "My Frontend Project Owner",
  "enabled": false,
  "schedule": {
    "kind": "every",
    "everyMs": 21600000
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Review my-frontend (GitHub: myorg/frontend, Vercel deployment).\n\nCheck:\n1. Deployment status\n2. Open PRs & recent commits\n3. Issues/blockers\n\nReply with:\n- 🟢/🟡/🔴 Status\n- 2-3 bullet points max\n- Under 500 chars",
    "deliver": true,
    "channel": "telegram",
    "to": "2128930209"
  }
}
```

Then import:
```bash
openclaw cron add --file my-frontend.json
openclaw cron add --file my-backend.json
openclaw cron add --file my-mobile-app.json
```

## Testing Jobs

Before enabling, test manually:

```bash
# Trigger a job immediately (doesn't change schedule)
openclaw cron run --job-id <id>

# Watch the output
openclaw cron runs --job-id <id>
```

## Common Patterns

### Pattern 1: Progressive Enablement

Don't enable all jobs at once. Start with 1-2, see how they work, then add more.

```
Week 1: daily-workflow-feedback
Week 2: Add weekly-reflection
Week 3: Add tool-discovery
Month 2: Add memory-consolidation
```

### Pattern 2: Timezone Consistency

Set all jobs to the same timezone:

```bash
# Update all jobs to your timezone
for id in $(openclaw cron list --json | jq -r '.[].id'); do
  openclaw cron update --job-id $id --patch '{
    "schedule": {
      "tz": "America/Los_Angeles"
    }
  }'
done
```

### Pattern 3: Quiet Hours

Disable jobs during sleep hours:

```json
{
  "payload": {
    "message": "Check current hour. If between 11pm-7am local time, skip and reschedule for 8am. Otherwise, [normal job logic]"
  }
}
```

## Troubleshooting

### Job not firing

```bash
# Check next run time
openclaw cron list --json | jq '.[] | select(.name == "My Job")'

# Verify job is enabled
openclaw cron list  # Should show in active list

# Check for errors
openclaw cron runs --job-id <id> | tail -20
```

### Job failing

```bash
# View recent runs and errors
openclaw cron runs --job-id <id>

# Check timeout setting
# Increase if job is complex:
openclaw cron update --job-id <id> --patch '{
  "payload": {
    "timeoutSeconds": 600
  }
}'
```

### Too many notifications

```bash
# Change from deliver:true to isolated session summary
openclaw cron update --job-id <id> --patch '{
  "payload": {
    "deliver": false
  },
  "isolation": {
    "postToMainPrefix": "Cron",
    "postToMainMode": "summary"
  }
}'
```

## Advanced: Batch Import Script

Create a script to import multiple jobs at once:

```bash
#!/bin/bash
# import-jobs.sh

JOBS=(
  "jobs/feedback/daily-workflow-feedback.json"
  "jobs/feedback/weekly-reflection.json"
  "jobs/analytics/token-usage-daily.json"
  "jobs/security/security-audit.json"
)

for job in "${JOBS[@]}"; do
  echo "Importing $job..."
  openclaw cron add --file "$job"
done

echo "Done! Remember to customize and enable jobs."
```

## Need Help?

- Check the main [README.md](README.md) for job descriptions
- Read [CONTRIBUTING.md](CONTRIBUTING.md) for job structure
- Browse [manifest.json](manifest.json) for the full catalog
- Ask in [OpenClaw Discord](https://discord.com/invite/clawd)

Happy optimizing! 🦉
