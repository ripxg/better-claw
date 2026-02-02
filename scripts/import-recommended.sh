#!/bin/bash
# Import recommended starter jobs from Better Claw library
# These are disabled by default - you can enable them after reviewing

set -e

echo "🦉 Better Claw - Import Recommended Jobs"
echo ""

# Check if openclaw CLI exists
if ! command -v openclaw &> /dev/null; then
    echo "❌ Error: openclaw CLI not found"
    echo "Please install OpenClaw first: https://github.com/openclaw/openclaw"
    exit 1
fi

# Recommended starter jobs (safe for all users)
JOBS=(
  "jobs/feedback/daily-workflow-feedback.json"
  "jobs/feedback/weekly-reflection.json"
  "jobs/feedback/learning-preference-calibration.json"
  "jobs/discovery/tool-discovery.json"
)

echo "This will import ${#JOBS[@]} recommended starter jobs:"
for job in "${JOBS[@]}"; do
  echo "  - $(basename "$job" .json)"
done
echo ""
echo "All jobs will be DISABLED by default."
echo "You can review and enable them after import."
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""
IMPORTED=0
FAILED=0

for job in "${JOBS[@]}"; do
  if [ ! -f "$job" ]; then
    echo "⚠️  Skipping $job (file not found)"
    ((FAILED++))
    continue
  fi
  
  echo -n "Importing $(basename "$job" .json)... "
  
  if openclaw cron add --file "$job" 2>/dev/null; then
    echo "✅"
    ((IMPORTED++))
  else
    echo "❌ (failed)"
    ((FAILED++))
  fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Imported: $IMPORTED jobs"
[ $FAILED -gt 0 ] && echo "Failed: $FAILED jobs"
echo ""
echo "Next steps:"
echo "1. Review jobs: openclaw cron list --include-disabled"
echo "2. Customize schedules/timezones as needed"
echo "3. Enable jobs: openclaw cron update --job-id <id> --patch '{\"enabled\": true}'"
echo ""
echo "See EXAMPLES.md for detailed usage guide."
echo "🦉 Make your agent better every day!"
