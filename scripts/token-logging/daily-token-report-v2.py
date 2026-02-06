#!/usr/bin/env python3
"""
Daily Token Usage Report Generator v2

Reads from session-end token register + active sessions
for complete daily token usage reporting across all agents.
"""

import json
import subprocess
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta


# Pricing per 1M tokens (as of 2026)
PRICING = {
    "claude-sonnet-4-5": {"input": 3.00, "output": 15.00},
    "claude-opus-4-5": {"input": 15.00, "output": 75.00},
    "claude-haiku-4-5": {"input": 0.25, "output": 1.25},
    "glm-4.7": {"input": 0.10, "output": 0.10},
}

REGISTER_PATH = Path("/home/ubuntu/clawd/data/token-usage-register.jsonl")


def fetch_active_sessions():
    """Fetch active session data from OpenClaw"""
    cmd = ["openclaw", "sessions", "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error fetching sessions: {result.stderr}")
        return []
    data = json.loads(result.stdout)
    return data.get("sessions", [])


def read_register_entries(hours=24):
    """Read session-end entries from the token register"""
    if not REGISTER_PATH.exists():
        print(f"Register not found: {REGISTER_PATH}")
        return []
    
    entries = []
    cutoff_time = datetime.now() - timedelta(hours=hours)
    
    with open(REGISTER_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            try:
                entry = json.loads(line)
                entry_time = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00")).replace(tzinfo=None)
                
                if entry_time >= cutoff_time:
                    entries.append(entry)
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Warning: Skipping invalid register entry: {e}")
                continue
    
    return entries


def normalize_session_data(session, source="active"):
    """Normalize session data from different sources"""
    if source == "active":
        # From openclaw sessions --json
        return {
            "session_key": session.get("key", "unknown"),
            "agent_id": session.get("agentId", "main"),
            "model": session.get("model", "unknown"),
            "tokens_input": session.get("inputTokens", 0),
            "tokens_output": session.get("outputTokens", 0),
            "cost": calculate_cost(
                session.get("model", "unknown"),
                session.get("inputTokens", 0),
                session.get("outputTokens", 0)
            ),
            "timestamp": datetime.fromtimestamp(session.get("updatedAt", 0) / 1000) if session.get("updatedAt") else datetime.now(),
            "source": "active"
        }
    else:
        # From register
        return {
            "session_key": session.get("session_key", "unknown"),
            "agent_id": session.get("agent_id", "main"),
            "model": session.get("model", "unknown"),
            "tokens_input": session.get("tokens_input", 0),
            "tokens_output": session.get("tokens_output", 0),
            "cost": session.get("cost", 0.0),
            "timestamp": datetime.fromisoformat(session["timestamp"].replace("Z", "+00:00")).replace(tzinfo=None),
            "source": "register"
        }


def calculate_cost(model, input_tokens, output_tokens):
    """Calculate cost in USD"""
    model_key = model.replace("anthropic/", "").replace("zai/", "")
    pricing = PRICING.get(model_key, {"input": 0, "output": 0})
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    return input_cost + output_cost


def merge_sessions(active_sessions, register_entries):
    """Merge active sessions + register entries, deduplicating by session_key"""
    merged = {}
    
    # Add register entries first (completed sessions)
    for entry in register_entries:
        normalized = normalize_session_data(entry, source="register")
        merged[normalized["session_key"]] = normalized
    
    # Add active sessions (may override if session completed since last poll)
    for session in active_sessions:
        normalized = normalize_session_data(session, source="active")
        # Only add if not already in register (avoid double-counting)
        if normalized["session_key"] not in merged:
            merged[normalized["session_key"]] = normalized
    
    return list(merged.values())


def generate_hourly_report(sessions, hours=24):
    """Generate hourly breakdown for last N hours"""
    now = datetime.now()
    hourly_data = defaultdict(lambda: {
        "sessions": [],
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "cost": 0.0,
        "models": defaultdict(int),
        "agents": defaultdict(int)
    })

    cutoff_time = now - timedelta(hours=hours)
    
    for session in sessions:
        session_time = session["timestamp"]
        
        if session_time < cutoff_time:
            continue
        
        # Round down to hour
        hour_key = session_time.strftime("%Y-%m-%d %H:00")
        
        model = session["model"]
        agent_id = session["agent_id"]
        input_toks = session["tokens_input"]
        output_toks = session["tokens_output"]
        total_toks = input_toks + output_toks
        cost = session["cost"]
        
        hourly_data[hour_key]["sessions"].append(session["session_key"])
        hourly_data[hour_key]["input_tokens"] += input_toks
        hourly_data[hour_key]["output_tokens"] += output_toks
        hourly_data[hour_key]["total_tokens"] += total_toks
        hourly_data[hour_key]["cost"] += cost
        hourly_data[hour_key]["models"][model] += 1
        hourly_data[hour_key]["agents"][agent_id] += 1
    
    return hourly_data


def generate_daily_dataset(sessions):
    """Generate reusable daily dataset"""
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    daily_data = {
        "date": today,
        "generated_at": now.isoformat(),
        "by_hour": {},
        "summary": {
            "total_tokens": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "total_cost": 0.0,
            "total_sessions": 0,
            "by_model": defaultdict(lambda: {"tokens": 0, "sessions": 0}),
            "by_agent": defaultdict(lambda: {"tokens": 0, "sessions": 0})
        }
    }
    
    # Last 24 hours hourly breakdown
    hourly_data = generate_hourly_report(sessions, hours=24)
    
    for hour, data in sorted(hourly_data.items()):
        daily_data["by_hour"][hour] = {
            "sessions": len(data["sessions"]),
            "input_tokens": data["input_tokens"],
            "output_tokens": data["output_tokens"],
            "total_tokens": data["total_tokens"],
            "cost": round(data["cost"], 4),
            "models": dict(data["models"]),
            "agents": dict(data["agents"])
        }
        
        # Add to summary
        daily_data["summary"]["total_tokens"] += data["total_tokens"]
        daily_data["summary"]["input_tokens"] += data["input_tokens"]
        daily_data["summary"]["output_tokens"] += data["output_tokens"]
        daily_data["summary"]["total_cost"] += data["cost"]
        daily_data["summary"]["total_sessions"] += len(data["sessions"])
    
    # Aggregate by model and agent
    for session in sessions:
        model = session["model"]
        agent_id = session["agent_id"]
        total_toks = session["tokens_input"] + session["tokens_output"]
        
        daily_data["summary"]["by_model"][model]["tokens"] += total_toks
        daily_data["summary"]["by_model"][model]["sessions"] += 1
        
        daily_data["summary"]["by_agent"][agent_id]["tokens"] += total_toks
        daily_data["summary"]["by_agent"][agent_id]["sessions"] += 1
    
    # Convert defaultdict to dict for JSON serialization
    daily_data["summary"]["by_model"] = dict(daily_data["summary"]["by_model"])
    daily_data["summary"]["by_agent"] = dict(daily_data["summary"]["by_agent"])
    
    return daily_data


def format_number(num):
    """Format large numbers with commas"""
    return f"{num:,}"


def generate_telegram_report(daily_data):
    """Generate Telegram-friendly report"""
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    lines = [
        "📊 *DAILY TOKEN USAGE REPORT*",
        f"📅 {today}",
        "",
        "*Summary*",
        f"┌ Total Tokens: `{format_number(daily_data['summary']['total_tokens'])}`",
    ]
    
    if daily_data['summary']['total_tokens'] > 0:
        lines.extend([
            f"├ Input: `{format_number(daily_data['summary']['input_tokens'])}` ({daily_data['summary']['input_tokens']/daily_data['summary']['total_tokens']*100:.1f}%)",
            f"├ Output: `{format_number(daily_data['summary']['output_tokens'])}` ({daily_data['summary']['output_tokens']/daily_data['summary']['total_tokens']*100:.1f}%)",
        ])
    
    lines.extend([
        f"├ Cost: `${daily_data['summary']['total_cost']:.4f}`",
        f"└ Sessions: `{daily_data['summary']['total_sessions']}`",
        "",
        "*By Model*",
    ])
    
    for model, data in sorted(daily_data["summary"]["by_model"].items(), key=lambda x: x[1]["tokens"], reverse=True):
        lines.append(f"• `{model}`: `{format_number(data['tokens'])}` tokens ({data['sessions']} sessions)")
    
    # Add agent breakdown
    if len(daily_data["summary"]["by_agent"]) > 1:  # Only show if multiple agents
        lines.append("")
        lines.append("*By Agent*")
        for agent_id, data in sorted(daily_data["summary"]["by_agent"].items(), key=lambda x: x[1]["tokens"], reverse=True):
            lines.append(f"• `{agent_id}`: `{format_number(data['tokens'])}` tokens ({data['sessions']} sessions)")
    
    lines.append("")
    lines.append("*Hourly Breakdown (Last 24 Hours)*")
    
    # Last 24 hours, reverse chronological
    for hour in sorted(daily_data["by_hour"].keys(), reverse=True):
        data = daily_data["by_hour"][hour]
        if data["sessions"] == 0:
            continue
        
        # Format hour as HH:00
        hour_label = hour.split(" ")[1] if " " in hour else hour
        lines.append(f"`{hour_label}`: `{format_number(data['total_tokens'])}` tokens ({data['sessions']} sessions) | `${data['cost']:.4f}`")
    
    lines.append("")
    lines.append("📁 Dataset: `/home/ubuntu/clawd/data/token-usage-daily.json`")
    lines.append("")
    lines.append(f"_Generated at {now.strftime('%H:%M')} UTC_")
    
    return "\n".join(lines)


def save_dataset(daily_data, output_path):
    """Save daily dataset as JSON"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(daily_data, f, indent=2)
    
    return output_path


def rotate_register(months_to_keep=2):
    """Archive old register entries (optional monthly cleanup)"""
    if not REGISTER_PATH.exists():
        return
    
    now = datetime.now()
    cutoff_date = now - timedelta(days=30 * months_to_keep)
    
    lines_to_keep = []
    archived_count = 0
    
    with open(REGISTER_PATH, "r") as f:
        for line in f:
            if line.startswith("#"):
                lines_to_keep.append(line)
                continue
            
            try:
                entry = json.loads(line.strip())
                entry_time = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                
                if entry_time >= cutoff_date:
                    lines_to_keep.append(line)
                else:
                    archived_count += 1
            except (json.JSONDecodeError, KeyError, ValueError):
                # Keep malformed lines for manual inspection
                lines_to_keep.append(line)
    
    if archived_count > 0:
        # Write back filtered entries
        with open(REGISTER_PATH, "w") as f:
            f.writelines(lines_to_keep)
        
        print(f"Archived {archived_count} entries older than {months_to_keep} months")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate daily token usage report v2")
    parser.add_argument("--dataset-output", default="/home/ubuntu/clawd/data/token-usage-daily.json", help="Dataset output path")
    parser.add_argument("--telegram-output", default="/home/ubuntu/clawd/data/token-report-daily.txt", help="Telegram report output path")
    parser.add_argument("--send-telegram", action="store_true", help="Send report to Telegram")
    parser.add_argument("--rotate", action="store_true", help="Rotate old register entries")
    args = parser.parse_args()
    
    print("📊 Generating daily token usage report v2...")
    
    # Fetch active sessions
    print("Fetching active sessions...")
    active_sessions = fetch_active_sessions()
    print(f"Found {len(active_sessions)} active sessions")
    
    # Read register entries
    print("Reading token register...")
    register_entries = read_register_entries(hours=24)
    print(f"Found {len(register_entries)} register entries (last 24h)")
    
    # Merge and deduplicate
    print("Merging sessions...")
    merged_sessions = merge_sessions(active_sessions, register_entries)
    print(f"Total unique sessions: {len(merged_sessions)}\n")
    
    # Generate daily dataset
    print("Generating daily dataset...")
    daily_data = generate_daily_dataset(merged_sessions)
    
    # Save dataset
    dataset_path = save_dataset(daily_data, args.dataset_output)
    print(f"Dataset saved to: {dataset_path}")
    
    # Generate Telegram report
    print("Generating Telegram report...")
    telegram_report = generate_telegram_report(daily_data)
    
    # Save Telegram report
    report_path = Path(args.telegram_output)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        f.write(telegram_report)
    print(f"Report saved to: {report_path}")
    
    # Send to Telegram if requested
    if args.send_telegram:
        print("\nSending to Telegram...")
        cmd = [
            "openclaw", "message", "send",
            "--channel", "telegram",
            "--target", "2128930209",
            "--message", telegram_report
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error sending to Telegram: {result.stderr}")
        else:
            print("Report sent to Telegram!")
    
    # Rotate register if requested
    if args.rotate:
        print("\nRotating old register entries...")
        rotate_register(months_to_keep=2)
    
    print("\n✅ Daily token usage report v2 complete!")


if __name__ == "__main__":
    main()
