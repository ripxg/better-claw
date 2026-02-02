# Installation Guide

**Step-by-step instructions for adding Better Claw jobs to your OpenClaw instance.**

---

## Prerequisites

Before you start, make sure you have:

- ✅ **OpenClaw installed** — See [OpenClaw docs](https://docs.openclaw.ai) if you haven't set it up yet
- ✅ **`openclaw` CLI available** — Test by running `openclaw --version`
- ✅ **Git installed** — For cloning the repository
- ✅ **Terminal access** — Basic command-line familiarity

---

## Step 1: Clone the Repository

Clone Better Claw to a location on your machine:

```bash
# Clone to your home directory or preferred location
cd ~
git clone https://github.com/ripxg/better-claw.git
cd better-claw
```

Or via HTTPS if you don't have SSH keys set up:

```bash
git clone https://github.com/ripxg/better-claw.git
cd better-claw
```

---

## Step 2: Explore Available Jobs

Browse the job categories to see what's available:

```bash
# View all categories
ls jobs/

# Output:
# analytics/  calendar/  discovery/  feedback/  memory/  projects/  security/

# List jobs in a specific category
ls jobs/feedback/

# Output:
# daily-workflow-feedback.json
# weekly-reflection.json
# learning-preference-calibration.json
# communication-audit.json
```

Check the [manifest.json](manifest.json) for a complete overview of all jobs with descriptions:

```bash
cat manifest.json | jq '.jobs[] | {name: .name, category: .category, description: .description}'
```

Or read the [README.md](README.md) for the full catalog.

---

## Step 3: Import Jobs

### Option A: Import Recommended Starter Jobs (Easiest)

Use the provided script to import a curated set of starter jobs:

```bash
# Make sure you're in the better-claw directory
cd ~/better-claw

# Run the import script
./scripts/import-recommended.sh
```

This imports:
- `daily-workflow-feedback` — Daily reflection on what worked/didn't
- `weekly-reflection` — Weekly summary of accomplishments and learnings
- `learning-preference-calibration` — Monthly check-in on your preferences
- `tool-discovery` — Weekly introduction to new OpenClaw capabilities

**All jobs are imported as DISABLED** so you can review them first.

### Option B: Import Specific Jobs (More Control)

Add individual jobs using the `openclaw cron add` command:

```bash
# Example: Add the daily workflow feedback job
openclaw cron add --file jobs/feedback/daily-workflow-feedback.json

# Example: Add the token usage analytics job
openclaw cron add --file jobs/analytics/token-usage-daily.json

# Example: Add the memory health check
openclaw cron add --file jobs/memory/memory-health-check.json
```

### Option C: Import All Jobs in a Category

Import every job from a specific category:

```bash
# Import all feedback jobs
for job in jobs/feedback/*.json; do
  echo "Importing $(basename "$job")..."
  openclaw cron add --file "$job"
done

# Import all analytics jobs
for job in jobs/analytics/*.json; do
  openclaw cron add --file "$job"
done
```

---

## Step 4: Review Imported Jobs

List all jobs (including disabled ones):

```bash
openclaw cron list --include-disabled
```

You'll see output like:

```
Jobs:
  ID: abc123
  Name: Daily Workflow Feedback Loop
  Schedule: 0 15 * * * (UTC)
  Enabled: false
  Next Run: (disabled)
  
  ID: def456
  Name: Weekly Reflection Summary
  Schedule: 0 18 * * 0 (UTC)
  Enabled: false
  Next Run: (disabled)
  
...
```

**Note the job IDs** — you'll need them for enabling and customizing jobs.

---

## Step 5: Customize Jobs (Optional)

Before enabling, customize schedules and timezones to fit your preferences.

### Example: Change Timezone

```bash
# Update the daily-workflow-feedback job to your timezone
openclaw cron update --job-id abc123 --patch '{"schedule": {"kind": "cron", "expr": "0 15 * * *", "tz": "America/New_York"}}'
```

Replace `"America/New_York"` with your timezone (e.g., `"Europe/London"`, `"Asia/Singapore"`, `"Australia/Sydney"`).

### Example: Change Schedule Time

```bash
# Change daily feedback to 6pm instead of 3pm
openclaw cron update --job-id abc123 --patch '{"schedule": {"kind": "cron", "expr": "0 18 * * *", "tz": "America/New_York"}}'
```

Cron expression format: `"minute hour day month weekday"`
- `0 9 * * *` = 9:00 AM every day
- `0 18 * * 5` = 6:00 PM every Friday
- `0 12 * * 1` = 12:00 PM every Monday

### Example: Customize Prompt

Edit the job file directly, then re-import:

```bash
# Edit the job file
nano jobs/feedback/daily-workflow-feedback.json

# Change the "text" field under "payload" to your preferred prompt
# Save and exit (Ctrl+X, then Y, then Enter)

# Re-import (will update existing job if name matches)
openclaw cron add --file jobs/feedback/daily-workflow-feedback.json
```

---

## Step 6: Enable Jobs

Once you've reviewed and customized, enable the jobs you want to run:

```bash
# Enable a specific job
openclaw cron update --job-id abc123 --patch '{"enabled": true}'

# Enable multiple jobs
openclaw cron update --job-id abc123 --patch '{"enabled": true}'
openclaw cron update --job-id def456 --patch '{"enabled": true}'
```

### Start Small!

**Recommended first jobs to enable:**
1. **daily-workflow-feedback** — Learn what communication patterns work
2. **tool-discovery** — Gradually discover OpenClaw features
3. **token-usage-daily** (if you track costs) — Monitor API usage

Enable 1-3 jobs initially, see how they fit your workflow, then add more.

---

## Step 7: Monitor and Adjust

### Check Job Status

```bash
# View all active jobs
openclaw cron list

# View job run history
openclaw cron runs --job-id abc123
```

### Disable a Job

If a job isn't useful or creates too much noise:

```bash
openclaw cron disable --job-id abc123
```

Or:

```bash
openclaw cron update --job-id abc123 --patch '{"enabled": false}'
```

### Remove a Job

Delete a job entirely:

```bash
openclaw cron remove --job-id abc123
```

---

## Step 8: Stay Updated

Better Claw is a community library that grows over time. Pull updates regularly:

```bash
cd ~/better-claw
git pull origin main
```

After pulling, check for new jobs:

```bash
cat manifest.json | jq '.jobs[] | {name: .name, category: .category}'
```

Import new jobs using the steps above.

---

## Troubleshooting

### "openclaw: command not found"

OpenClaw CLI isn't in your PATH. Check installation:

```bash
which openclaw
```

If not installed, see [OpenClaw installation docs](https://docs.openclaw.ai/getting-started/installation).

### "Error: Invalid job format"

The job file might be corrupted or incompatible. Validate JSON:

```bash
cat jobs/feedback/daily-workflow-feedback.json | jq .
```

If that fails, re-clone the repository.

### Jobs Not Running

Check:
1. **Is the job enabled?** `openclaw cron list --include-disabled`
2. **Is the schedule correct?** Review the cron expression
3. **Is the gateway running?** `openclaw status`

### Wrong Timezone

Update the job's timezone:

```bash
openclaw cron update --job-id abc123 --patch '{"schedule": {"tz": "Your/Timezone"}}'
```

List of valid timezones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

### Job Creates Too Much Noise

Options:
- **Adjust frequency** — Change the schedule to run less often
- **Refine prompt** — Edit the job file to make it more focused
- **Disable temporarily** — `openclaw cron disable --job-id abc123`
- **Remove** — `openclaw cron remove --job-id abc123`

---

## Next Steps

- **Read [EXAMPLES.md](EXAMPLES.md)** — See real-world usage patterns and customizations
- **Read [CONTRIBUTING.md](CONTRIBUTING.md)** — Share your own jobs with the community
- **Join the community** — [OpenClaw Discord](https://discord.com/invite/clawd)

---

## Quick Reference

| Action | Command |
|--------|---------|
| Clone repository | `git clone https://github.com/ripxg/better-claw.git` |
| Import recommended jobs | `./scripts/import-recommended.sh` |
| Import single job | `openclaw cron add --file jobs/category/job-name.json` |
| List all jobs | `openclaw cron list --include-disabled` |
| Enable job | `openclaw cron update --job-id <id> --patch '{"enabled": true}'` |
| Disable job | `openclaw cron update --job-id <id> --patch '{"enabled": false}'` |
| Remove job | `openclaw cron remove --job-id <id>` |
| View job runs | `openclaw cron runs --job-id <id>` |
| Update timezone | `openclaw cron update --job-id <id> --patch '{"schedule": {"tz": "Your/Timezone"}}'` |

---

🦉 **Make your agent better every day!**
