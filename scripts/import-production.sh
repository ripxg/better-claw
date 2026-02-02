#!/bin/bash
# Import production-critical jobs (security, config monitoring, alerts)
# IMPORTANT: Review and customize BEFORE enabling these jobs!

set -e

echo "🔒 Better Claw - Import Production Jobs"
echo ""

# Check if openclaw CLI exists
if ! command -v openclaw &> /dev/null; then
    echo "❌ Error: openclaw CLI not found"
    echo "Please install OpenClaw first: https://github.com/openclaw/openclaw"
    exit 1
fi

# Production-critical jobs
JOBS=(
  "jobs/security/security-audit.json"
  "jobs/security/config-drift-detector.json"
)

echo "⚠️  WARNING: Production Jobs"
echo ""
echo "These jobs have elevated permissions and can:"
echo "  - Modify gateway configuration"
echo "  - Fix security issues automatically"
echo "  - Send alerts to your channels"
echo ""
echo "This will import ${#JOBS[@]} production jobs:"
for job in "${JOBS[@]}"; do
  echo "  - $(basename "$job" .json)"
done
echo ""
echo "IMPORTANT:"
echo "1. All jobs will be DISABLED by default"
echo "2. You MUST customize delivery channels before enabling"
echo "3. Review each job's permissions carefully"
echo "4. Test with 'openclaw cron run --job-id <id>' before enabling"
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
echo "⚠️  BEFORE ENABLING:"
echo ""
echo "1. Update delivery channels:"
echo "   openclaw cron update --job-id <id> --patch '{"
echo "     \"payload\": {"
echo "       \"channel\": \"telegram\","
echo "       \"to\": \"YOUR_TELEGRAM_ID\""
echo "     }"
echo "   }'"
echo ""
echo "2. Test each job:"
echo "   openclaw cron run --job-id <id>"
echo ""
echo "3. Review output:"
echo "   openclaw cron runs --job-id <id>"
echo ""
echo "4. Enable when ready:"
echo "   openclaw cron update --job-id <id> --patch '{\"enabled\": true}'"
echo ""
echo "See EXAMPLES.md for detailed configuration guide."
echo "🔒 Stay secure!"
