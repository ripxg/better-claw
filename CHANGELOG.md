# Changelog

All notable changes to Better Claw will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- **Token Logging System v2** (2026-02-06)
  - Session-end logging protocol for accurate cross-agent token tracking
  - `daily-token-report-v2.py` script with register + active session merging
  - `log-session-tokens.sh` helper script for easy session logging
  - `token-usage-register.jsonl` persistent JSONL register
  - Comprehensive documentation in `scripts/token-logging/README.md`
  - AGENTS.md patch for session-end logging integration
  - Agent breakdown (coordinator vs subagents) in daily reports
  - Automatic deduplication by session_key
  - Monthly rotation of old register entries
  - Fixes: Daily token reports now capture completed sessions and subagent usage

### Changed
- Updated `token-usage-daily.json` job definition to v2
- Updated README to reflect v2 features

## [1.0.0] - 2026-02-02

### Added
- Initial release of Better Claw cron job library
- 18+ curated cron jobs across 7 categories:
  - Feedback & Learning
  - Usage & Analytics
  - Project Health
  - Memory & Context
  - Security & Maintenance
  - Discovery & Exploration
  - Calendar & Scheduling
- Zero-backend landing page for browsing jobs
- GitHub Pages deployment guide
- Installation and configuration documentation
- Examples and best practices
- Contributing guidelines

### Categories

#### Feedback & Learning
- `daily-workflow-feedback` - Daily reflection on communication patterns
- `weekly-reflection` - Weekly accomplishments and lessons learned
- `learning-preference-calibration` - Monthly style adaptation check-in
- `communication-audit` - Weekly message clarity review

#### Usage & Analytics
- `token-usage-daily` - Daily token usage report (v1)
- `session-summary` - Weekly session activity summary
- `tool-usage-report` - Monthly tool usage analysis

#### Project Health
- `project-owner` - Template for monitoring project status
- `stalled-work-detector` - Detect inactive projects
- `dependency-update-check` - Check for outdated dependencies
- `test-coverage-monitor` - Track test coverage trends

#### Memory & Context
- `memory-health-check` - Detect stale/contradictory memories
- `memory-consolidation` - Merge daily notes into MEMORY.md
- `context-pruning` - Archive outdated context

#### Security & Maintenance
- `security-audit` - Weekly security posture check
- `secret-leak-detector` - Scan for exposed credentials
- `backup-health` - Verify backup integrity

#### Discovery & Exploration
- `tool-discovery` - Weekly exploration of new OpenClaw features
- `skill-discovery` - Monthly skill library updates
- `model-benchmarking` - Monthly model performance comparison

#### Calendar & Scheduling
- `daily-agenda` - Morning agenda with upcoming events
- `event-reminder` - Pre-event notifications
- `weekly-planning` - Sunday evening week prep

## Links

- [GitHub Repository](https://github.com/ripxg/better-claw)
- [Landing Page](https://ripxg.github.io/better-claw/)
- [Installation Guide](INSTALLATION.md)
- [Contributing](CONTRIBUTING.md)
