# Contributing to Better Claw

Thank you for your interest in improving the Better Claw job library! This document provides guidelines for contributing new jobs, improving existing ones, and sharing your customizations.

## Philosophy

Better Claw is about **continuous self-improvement** for AI agents. When proposing new jobs, ask:

1. **Does it create a feedback loop?** The best jobs learn and adapt over time.
2. **Is it actionable?** Reports should lead to specific actions, not just information.
3. **Does it respect the user's time?** Brief, high-signal outputs > verbose reports.
4. **Is it broadly useful?** Avoid hyper-specific workflows; focus on common patterns.

## Ways to Contribute

### 1. New Job Submissions

Have a great cron job pattern? Share it!

**Requirements:**
- JSON file following the job schema (see below)
- Clear description and use case
- Recommended schedule with rationale
- Configuration options documented
- Estimated duration and required capabilities
- Example output (optional but helpful)

**File structure:**
```
jobs/
  <category>/
    <job-name>.json
```

**Job schema:**
```json
{
  "name": "Job Display Name",
  "description": "One-sentence description of what this job does",
  "enabled": false,
  "schedule": {
    "kind": "cron|every",
    "expr": "0 9 * * *",  // for cron
    "everyMs": 86400000,   // for every
    "tz": "UTC",
    "rationale": "Why this schedule makes sense"
  },
  "sessionTarget": "main|isolated",
  "wakeMode": "next-heartbeat|now",
  "payload": {
    "kind": "systemEvent|agentTurn",
    "text": "Prompt for systemEvent",
    "message": "Prompt for agentTurn",
    // ... other payload fields
  },
  "configuration": {
    "schedule": "How to customize schedule",
    "delivery": "Delivery options",
    // ... other config notes
  },
  "category": "feedback|analytics|projects|memory|security|calendar|discovery",
  "requiredCapabilities": ["tool1", "tool2"],
  "estimatedDuration": "1-2 minutes",
  "recommendedFor": ["user type 1", "user type 2"],
  "tips": ["tip 1", "tip 2"]
}
```

**Categories:**
- `feedback`: Learning and communication improvement
- `analytics`: Usage tracking and insights
- `projects`: Codebase and deployment monitoring
- `memory`: Memory health and maintenance
- `security`: Security and config monitoring
- `calendar`: Time and deadline awareness
- `discovery`: Capability exploration

### 2. Improve Existing Jobs

Found a bug? Have a better prompt? Want to add configuration options?

**Process:**
1. Fork the repository
2. Make your changes to the job file
3. Update the job's version/notes if significant
4. Submit a PR with clear description of changes
5. Include before/after examples if applicable

### 3. Share Customizations

Have you customized a job for your workflow? Share your variant!

**Options:**
- Add to the `examples` array in the job file
- Create a variant job file (e.g., `project-owner-frontend.json`)
- Document in a blog post and link in discussions

### 4. Documentation Improvements

Help make Better Claw more accessible:

- Clarify unclear instructions
- Add missing examples
- Improve README explanations
- Fix typos and formatting

## Submission Guidelines

### Pull Request Process

1. **Fork & Branch**
   ```bash
   git clone https://github.com/YOUR_USERNAME/better-claw.git
   cd better-claw
   git checkout -b feature/your-job-name
   ```

2. **Create Job File**
   - Place in appropriate category directory
   - Follow naming convention: `lowercase-with-hyphens.json`
   - Validate JSON (use `jq` or online validator)

3. **Update Manifest**
   - Add your job to `manifest.json` in the appropriate category
   - Increment `totalJobs` count
   - Update `lastUpdated` date

4. **Test Locally**
   ```bash
   # Validate JSON
   jq . jobs/your-category/your-job.json
   
   # Test import (don't enable yet!)
   openclaw cron add --file jobs/your-category/your-job.json
   
   # Review and test
   openclaw cron list --include-disabled
   ```

5. **Document**
   - Clear commit messages: `feat: add memory-cleanup job`
   - PR description: What the job does, why it's useful, testing done

6. **Submit PR**
   - Push your branch
   - Open PR against `main`
   - Fill out PR template (coming soon)

### Job Quality Checklist

Before submitting, ensure your job has:

- [ ] **Clear name** - Descriptive and concise
- [ ] **Good description** - One sentence, clear value proposition
- [ ] **Disabled by default** - Users must opt-in
- [ ] **Sensible schedule** - With rationale
- [ ] **Proper session target** - Main vs isolated with justification
- [ ] **Actionable prompt** - Specific instructions, expected format
- [ ] **Configuration docs** - How to customize
- [ ] **Required capabilities** - What tools/access needed
- [ ] **Realistic duration** - Estimated execution time
- [ ] **Target audience** - Who benefits from this job
- [ ] **Usage tips** - How to get the most value
- [ ] **No hardcoded secrets** - Use placeholders like YOUR_API_KEY
- [ ] **Tested** - You've run it and verified it works

### Writing Good Prompts

Job prompts should be:

1. **Specific**: Clear instructions on what to check/do
2. **Structured**: Use sections, lists, formatting
3. **Concise**: Respect agent context limits
4. **Actionable**: Lead to clear next steps
5. **Consistent**: Follow similar jobs' format

**Example good prompt:**
```
Review project health.

Check:
1. Deployment status
2. Open PRs & commits
3. Issues/blockers

Report:
- 🟢/🟡/🔴 Status
- 2-3 bullet points max
- Under 500 chars
```

**Example bad prompt:**
```
Look at the project and tell me how it's doing
```

### Style Guide

**Job files:**
- Use 2-space indentation
- Include rationale for schedule
- Document all configuration options
- Provide realistic duration estimates

**Commit messages:**
```
feat: add weekly project health summary
fix: correct cron expression in daily-agenda
docs: clarify memory-consolidation requirements
refactor: simplify project-owner prompt
```

## Community

- **Discussions**: Share customizations, ask questions, propose ideas
- **Issues**: Report bugs, request features, suggest improvements
- **Discord**: [Join OpenClaw community](https://discord.com/invite/clawd)

## Code of Conduct

- Be respectful and constructive
- Focus on helping users improve their AI workflows
- Provide thoughtful feedback on contributions
- Assume good intent

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Open a discussion for general questions
- File an issue for bugs or feature requests
- Tag @ripxg in discussions for maintainer attention

Thank you for making Better Claw better! 🦉
