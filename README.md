# Better Claw 🦞

**Make your AI agent better every day.**

A curated library of OpenClaw cron jobs that implement continuous self-improvement loops. These scheduled tasks help your agent learn from experience, gather feedback, maintain project health, and evolve based on your preferences.

## Philosophy

The best AI agents aren't static—they adapt and improve over time. Better Claw helps you build feedback loops that:

- **Learn from patterns** — Identify what works and what doesn't through daily reflection
- **Stay accountable** — Regular check-ins on projects, usage, and progress
- **Maintain health** — Catch stale memories, detect stalled work, monitor security
- **Discover capabilities** — Gradually explore and adopt new tools and workflows
- **Respect your time** — Brief, actionable reports that inform without overwhelming

## 🌐 Browse Jobs Online

**NEW:** Visit the [Better Claw Landing Page](https://ripxg.github.io/better-claw/) to browse all available jobs organized by category!

The landing page provides:
- ✨ Visual catalog of all jobs
- 📚 Categories and descriptions
- 🏷️ Difficulty levels and recommendations
- 🚀 Quick start guide
- 📦 Direct links to job files

## Quick Start

**New to Better Claw?** → Read **[INSTALLATION.md](INSTALLATION.md)** for step-by-step setup instructions.

**TL;DR:**
```bash
# 1. Clone the repository
git clone https://github.com/ripxg/better-claw.git
cd better-claw

# 2. Import recommended starter jobs (all disabled by default)
./scripts/import-recommended.sh

# 3. Review and enable jobs
openclaw cron list --include-disabled
openclaw cron update --job-id <id> --patch '{"enabled": true}'
```

That's it! See [INSTALLATION.md](INSTALLATION.md) for detailed instructions, customization options, and troubleshooting.

## Job Catalog

### 🔄 Feedback & Learning
Jobs that help your agent learn from experience and improve communication.

| Job | Description | Schedule | Requires |
|-----|-------------|----------|----------|
| [daily-workflow-feedback](jobs/feedback/daily-workflow-feedback.json) | Daily reflection on communication patterns and process improvements | Daily @ 3pm UTC | Main session |
| [weekly-reflection](jobs/feedback/weekly-reflection.json) | Weekly summary of accomplishments, lessons learned, and goals | Sunday @ 6pm | Main session, memory access |
| [learning-preference-calibration](jobs/feedback/learning-preference-calibration.json) | Monthly check-in on how the agent should adapt to your style | First of month | Main session |
| [communication-audit](jobs/feedback/communication-audit.json) | Weekly review of message clarity and response quality | Friday @ 5pm | Session logs |

### 📊 Usage & Analytics
Jobs that track resource usage and provide insights.

| Job | Description | Schedule | Requires |
|-----|-------------|----------|----------|
| [token-usage-daily](jobs/analytics/token-usage-daily.json) | Daily token usage report with hourly breakdown | Daily @ 8pm | Python script, Telegram |
| [session-summary](jobs/analytics/session-summary.json) | Weekly session activity summary (spawns, models used, costs) | Sunday @ 9pm | Session history |
| [tool-usage-report](jobs/analytics/tool-usage-report.json) | Monthly report on which tools are used most/least | 1st of month | Session logs |

### 🏗️ Project Health
Jobs that monitor codebases and deployments.

| Job | Description | Schedule | Requires |
|-----|-------------|----------|----------|
| [project-owner](jobs/projects/project-owner.json) | Template for owning a project: check deployment, PRs, issues | Every 12h | GitHub access |
| [stalled-work-detector](jobs/projects/stalled-work-detector.json) | Detect projects with no commits in 7+ days | Every 3 days | Git access |
| [dependency-update-check](jobs/projects/dependency-update-check.json) | Check for outdated dependencies and security updates | Weekly Monday | npm/yarn/bun |
| [test-coverage-monitor](jobs/projects/test-coverage-monitor.json) | Track test coverage trends over time | After each push | CI integration |

### 🧠 Memory & Context
Jobs that maintain memory health and context awareness.

| Job | Description | Schedule | Requires |
|-----|-------------|----------|----------|
| [memory-health-check](jobs/memory/memory-health-check.json) | Detect stale, contradictory, or duplicate memories | Weekly Saturday | memory_search, memory_get |
| [memory-consolidation](jobs/memory/memory-consolidation.json) | Suggest merging daily notes into MEMORY.md | Every 3 days | Memory files |
| [context-pruning](jobs/memory/context-pruning.json) | Identify outdated context that can be archived | Monthly | Memory files |

### 🔒 Security & Maintenance
Jobs that keep your setup secure and healthy.

| Job | Description | Schedule | Requires |
|-----|-------------|----------|----------|
| [security-audit](jobs/security/security-audit.json) | Run security audit and fix critical issues | Daily | openclaw security CLI |
| [config-drift-detector](jobs/security/config-drift-detector.json) | Detect unexpected config changes | Daily | Gateway config access |
| [secret-scanner](jobs/security/secret-scanner.json) | Scan workspace for accidentally committed secrets | Weekly | Workspace access |

### 📅 Calendar & Awareness
Jobs that help your agent stay aware of time and commitments.

| Job | Description | Schedule | Requires |
|-----|-------------|----------|----------|
| [daily-agenda](jobs/calendar/daily-agenda.json) | Morning summary of today's events and deadlines | Daily @ 8am | Calendar access |
| [deadline-reminder](jobs/calendar/deadline-reminder.json) | Alert on approaching deadlines (3 days, 1 day, today) | Every 6h | Project tracking |
| [time-zone-aware-standups](jobs/calendar/time-zone-aware-standups.json) | Daily standup adjusted for your current timezone | Daily @ 9am local | Timezone tracking |

### 🔍 Discovery & Growth
Jobs that help discover new capabilities and patterns.

| Job | Description | Schedule | Requires |
|-----|-------------|----------|----------|
| [tool-discovery](jobs/discovery/tool-discovery.json) | Introduce one new OpenClaw capability per week | Weekly Wednesday | Skills directory |
| [skill-learning-prompt](jobs/discovery/skill-learning-prompt.json) | Periodic review of available skills to learn new patterns | Bi-weekly | Skills access |

## How to Use

**See [INSTALLATION.md](INSTALLATION.md) for complete setup instructions.**

**Quick reference:**

```bash
# Import a single job
openclaw cron add --file jobs/feedback/daily-workflow-feedback.json

# Import recommended starter jobs
./scripts/import-recommended.sh

# List all jobs (including disabled)
openclaw cron list --include-disabled

# Enable a job
openclaw cron update --job-id <id> --patch '{"enabled": true}'

# Disable a job
openclaw cron update --job-id <id> --patch '{"enabled": false}'

# Customize timezone
openclaw cron update --job-id <id> --patch '{"schedule": {"tz": "Your/Timezone"}}'
```

For detailed examples, customization options, and troubleshooting, see:
- **[INSTALLATION.md](INSTALLATION.md)** — Step-by-step setup guide
- **[EXAMPLES.md](EXAMPLES.md)** — Real-world usage patterns

## Categories Explained

### Feedback & Learning
These jobs create feedback loops. They ask questions, gather reflections, and help your agent adapt to your communication style over time. Start with `daily-workflow-feedback` if you're new.

### Usage & Analytics
Track how your agent is being used. Useful for understanding costs, identifying patterns, and optimizing workflows. The `token-usage-daily` job is essential for cost-conscious users.

### Project Health
For developers and teams managing multiple codebases. These jobs act as "project owners" that monitor health, detect issues, and suggest next steps. Clone `project-owner` for each repo you care about.

### Memory & Context
Your agent's memory grows over time. These jobs help maintain quality by detecting duplicates, consolidating notes, and pruning outdated information.

### Security & Maintenance
Proactive security and config monitoring. The `security-audit` job should be enabled for all production deployments.

### Calendar & Awareness
Help your agent understand time-sensitive context: deadlines, meetings, time zones. Especially useful for frequent travelers or distributed teams.

### Discovery & Growth
These jobs gradually introduce new capabilities, ensuring you get value from OpenClaw's full feature set without overwhelming initial setup.

## Best Practices

1. **Start small** — Enable 2-3 jobs and see how they fit your workflow
2. **Adjust delivery** — Use Telegram/Discord for async updates, main session for interactive reflection
3. **Respect quiet hours** — Schedule intensive jobs during your working hours
4. **Iterate prompts** — Customize the prompt templates to match your preferences
5. **Monitor noise** — If a job isn't providing value, disable it
6. **Use isolated sessions** — Most jobs should use `sessionTarget: "isolated"` to avoid cluttering your main conversation
7. **Set timeouts** — Add reasonable `timeoutSeconds` to prevent runaway jobs

## Contributing

We welcome community contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Proposing new jobs
- Improving existing templates
- Sharing customizations
- Reporting issues

## Credits

Built on the [OpenClaw](https://github.com/openclaw/openclaw) agent framework.

Initial job library curated by [ripXG](https://github.com/ripxg).

## License

MIT — Use freely, improve openly.
