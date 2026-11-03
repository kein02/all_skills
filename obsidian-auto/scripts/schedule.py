#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""obsidian-auto / schedule.py

把两个维护任务（每日整理 / 每周健康检查）落到目标宿主的调度器上：
  - workbuddy : 输出 automation_update 所需的 JSON（由 Agent 调用工具创建）
  - cron      : 生成 crontab 行 + 包装脚本
  - schtasks  : 生成 Windows 计划任务注册脚本（.ps1）
  - launchd   : 生成 macOS LaunchAgent plist
  - json      : 输出与平台无关的任务规格（含 prompt 全文）

所有平台共用 tasks.py 里同一份 prompt，避免多套实现漂移。

用法：
  python schedule.py --vault "D:/Obsidian WH/新库" --platform workbuddy
  python schedule.py --vault "D:/Notes" --platform auto --write
  python schedule.py --vault "/Users/me/Notes" --platform launchd --runner "claude -p" --write
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tasks import DAY_CN, DAY_CRON, DAY_LAUNCHD, DAY_SCHTASKS, SKILL_NAME, build_tasks  # noqa: E402

TIME_RE = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")
PLATFORMS = ("auto", "workbuddy", "cron", "schtasks", "launchd", "json")
DEFAULT_RUNNER = "claude -p"


def emit(payload, code=0):
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.exit(code)


def detect_platform():
    if sys.platform.startswith("win"):
        return "schtasks"
    if sys.platform == "darwin":
        return "launchd"
    return "cron"


def slugify(path):
    return hashlib.md5(str(path).encode("utf-8")).hexdigest()[:8]


def validate(args):
    errors = []
    vault = Path(os.path.normpath(os.path.abspath(args.vault)))
    if not vault.is_dir():
        errors.append(f"--vault 必须是已存在的目录：{vault}")
    if args.platform not in PLATFORMS:
        errors.append(f"--platform 必须是 {'/'.join(PLATFORMS)}")
    for flag, val in (("--daily-time", args.daily_time), ("--weekly-time", args.weekly_time)):
        if not val:
            errors.append(f"{flag} 必须由用户指定（不提供默认时间），例如 {flag} 09:00")
        elif not TIME_RE.match(val):
            errors.append(f"{flag} 需为 HH:MM，收到：{val}")
    if args.weekly_day not in DAY_CN:
        errors.append(f"--weekly-day 需为 MO/TU/WE/TH/FR/SA/SU，收到：{args.weekly_day}")
    if not (args.runner or "").strip():
        errors.append("--runner 不能为空（例如 \"claude -p\"、\"codex exec -\"）")
    cats = [c.strip() for c in (args.categories or "").split(",") if c.strip()]
    if not cats:
        errors.append("--categories 至少一个，例如 concepts,entities,sources")
    if errors:
        emit({"ok": False, "error": {"code": "validation", "messages": errors}}, 2)
    return vault, cats


def build(args):
    vault, cats = validate(args)
    platform = args.platform if args.platform != "auto" else detect_platform()
    tasks = build_tasks(
        path=str(vault),
        name=args.name or vault.name,
        categories=cats,
        daily_time=args.daily_time,
        weekly_day=args.weekly_day,
        weekly_time=args.weekly_time,
    )
    return vault, platform, tasks


def base_dir(vault, args):
    return Path(args.out) if args.out else vault / ".obsidian-auto"


def wrapper_name(key, platform):
    return f"{key}.cmd" if platform == "schtasks" else f"{key}.sh"


def wrapper_content(key, vault, runner, base, platform):
    """按目标平台生成包装脚本，行尾统一用 \n，由写盘时决定 CRLF。"""
    prompt = base / "tasks" / f"{key}.md"
    log = base / "log" / f"{key}.log"
    if platform == "schtasks":
        return ("@echo off\n"
                "chcp 65001 >nul\n"
                f'cd /d "{vault}"\n'
                f'{runner} < "{prompt}" >> "{log}" 2>&1\n')
    return ("#!/usr/bin/env bash\n"
            "set -uo pipefail\n"
            f'cd "{vault}"\n'
            f'{runner} < "{prompt}" >> "{log}" 2>&1\n')


def crontab_lines(tasks, base, platform):
    lines = ["# obsidian-auto 生成的定时任务，合并进 crontab -e 即可"]
    for t in tasks:
        minute, hour = t["minute"], t["hour"]
        if t["frequency"] == "daily":
            sched = f"{minute} {hour} * * *"
        else:
            sched = f"{minute} {hour} * * {DAY_CRON[t['day']]}"
        wrapper = (base / "bin" / wrapper_name(t["key"], platform)).as_posix()
        lines.append(f'{sched} "{wrapper}"')
    return "\n".join(lines)


def schtasks_script(tasks, base, name):
    lines = [
        "# 由 obsidian-auto 生成；建议用管理员 PowerShell 运行",
        "$ErrorActionPreference = 'Stop'",
    ]
    for t in tasks:
        wrapper = str(base / "bin" / wrapper_name(t["key"], "schtasks"))
        task_name = f"obsidian-auto\\{name}-{t['key']}"
        at = f"{t['hour']:02d}:{t['minute']:02d}"
        lines.append(f'$a_{t["key"]} = New-ScheduledTaskAction -Execute "{wrapper}"')
        if t["frequency"] == "daily":
            lines.append(f'$t_{t["key"]} = New-ScheduledTaskTrigger -Daily -At "{at}"')
        else:
            day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][
                ["MO", "TU", "WE", "TH", "FR", "SA", "SU"].index(t["day"])]
            lines.append(f'$t_{t["key"]} = New-ScheduledTaskTrigger -Weekly -DaysOfWeek {day} -At "{at}"')
        lines.append(f'Register-ScheduledTask -TaskName "{task_name}" -Action $a_{t["key"]} '
                     f'-Trigger $t_{t["key"]} -Force | Out-Null')
    return "\n".join(lines)


def schtasks_commands(tasks, base, name):
    cmds = []
    for t in tasks:
        wrapper = str(base / "bin" / wrapper_name(t["key"], "schtasks"))
        task_name = f"obsidian-auto\\{name}-{t['key']}"
        at = f"{t['hour']:02d}:{t['minute']:02d}"
        if t["frequency"] == "daily":
            cmds.append(f'schtasks /Create /TN "{task_name}" /TR "\\"{wrapper}\\"" /SC DAILY /ST {at} /F')
        else:
            cmds.append(f'schtasks /Create /TN "{task_name}" /TR "\\"{wrapper}\\"" '
                        f'/SC WEEKLY /D {DAY_SCHTASKS[t["day"]]} /ST {at} /F')
    return cmds


def plist_content(label, wrapper, log, hour, minute, weekday=None):
    interval = ["  <key>StartCalendarInterval</key>", "  <dict>",
                "    <key>Hour</key>", f"    <integer>{hour}</integer>",
                "    <key>Minute</key>", f"    <integer>{minute}</integer>"]
    if weekday is not None:
        interval += ["    <key>Weekday</key>", f"    <integer>{weekday}</integer>"]
    interval.append("  </dict>")
    return "\n".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
        '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">',
        '<plist version="1.0">',
        '<dict>',
        '  <key>Label</key>',
        f'  <string>{label}</string>',
        '  <key>ProgramArguments</key>',
        '  <array>',
        '    <string>/bin/bash</string>',
        f'    <string>{wrapper}</string>',
        '  </array>',
    ] + interval + [
        '  <key>StandardOutPath</key>',
        f'  <string>{log}</string>',
        '  <key>StandardErrorPath</key>',
        f'  <string>{log}</string>',
        '</dict>',
        '</plist>',
        '',
    ])


def materialize(base, platform, tasks, vault, runner, name):
    written = []
    for sub in ("tasks", "bin", "log"):
        (base / sub).mkdir(parents=True, exist_ok=True)
    def write(path, text, crlf=False, bom=False):
        prefix = "\ufeff" if bom else ""
        path.write_text(prefix + text, encoding="utf-8", newline="\r\n" if crlf else "\n")

    for t in tasks:
        prompt_path = base / "tasks" / f"{t['key']}.md"
        write(prompt_path, t["prompt"] + "\n")
        wrapper = base / "bin" / wrapper_name(t["key"], platform)
        write(wrapper, wrapper_content(t["key"], vault, runner, base, platform), crlf=(platform == "schtasks"))
        if platform != "schtasks":
            try:
                os.chmod(wrapper, 0o755)
            except OSError:
                pass
        written += [str(prompt_path), str(wrapper)]

    if platform == "cron":
        path = base / "crontab.txt"
        write(path, crontab_lines(tasks, base, platform) + "\n")
        written.append(str(path))
    elif platform == "schtasks":
        path = base / "install-schedule.ps1"
        write(path, schtasks_script(tasks, base, name) + "\n", crlf=True, bom=True)
        written.append(str(path))
    elif platform == "launchd":
        ldir = base / "launchd"
        ldir.mkdir(parents=True, exist_ok=True)
        label_base = f"com.obsidian-auto.{slugify(vault)}"
        for t in tasks:
            label = f"{label_base}.{t['key']}"
            wrapper = base / "bin" / wrapper_name(t["key"], platform)
            log = base / "log" / f"{t['key']}.log"
            weekday = DAY_LAUNCHD[t["day"]] if t["frequency"] == "weekly" else None
            path = ldir / f"{label}.plist"
            write(path, plist_content(label, wrapper, log, t["hour"], t["minute"], weekday))
            written.append(str(path))
    elif platform == "json":
        path = base / "tasks.json"
        write(path, json.dumps({"vault": str(vault), "runner": runner, "tasks": tasks},
                               ensure_ascii=False, indent=2) + "\n")
        written.append(str(path))
    return written


def instructions_for(platform, base, name, tasks):
    if platform == "workbuddy":
        return ["宿主支持 automation_update 时：按 automations 数组逐个 create，"
                "同名同 cwd 已存在则 update 或跳过（幂等）。"]
    if platform == "cron":
        return [f"查看 {base / 'crontab.txt'}，确认后合并进 `crontab -e`",
                "首次运行前确认 runner 可从 stdin 读取指令（如 `claude -p`）",
                "日志在 .obsidian-auto/log/ 下"]
    if platform == "schtasks":
        return [f"用管理员 PowerShell 运行 {base / 'install-schedule.ps1'}",
                f"或不走脚本，逐条执行输出的 schtasks 命令（任务名前缀 obsidian-auto\\{name}-）",
                "任务可在「任务计划程序」中查看，删除用 Unregister-ScheduledTask"]
    if platform == "launchd":
        return [f"把 {base / 'launchd'} 下的 plist 复制到 ~/Library/LaunchAgents/",
                "执行 `launchctl load ~/Library/LaunchAgents/<label>.plist` 加载",
                "卸载用 `launchctl unload` + 删除 plist"]
    return ["仅输出规格，未安装任何调度；需要时用 --platform cron/schtasks/launchd 生成"]


def main(argv=None):
    p = argparse.ArgumentParser(prog="schedule.py", description="为 obsidian-auto 生成各宿主调度配置")
    p.add_argument("--vault", required=True, help="已存在的知识库绝对路径")
    p.add_argument("--name", help="任务名前缀，默认取目录名")
    p.add_argument("--categories", default="concepts,entities,sources")
    p.add_argument("--platform", default="auto", choices=PLATFORMS)
    p.add_argument("--runner", default=DEFAULT_RUNNER,
                   help=f"触发任务用的 CLI 命令，默认 {DEFAULT_RUNNER}")
    p.add_argument("--daily-time", help="每日整理时间 HH:MM（必填，无默认值）")
    p.add_argument("--weekly-day", default="MO", help="每周健康检查星期，默认 MO")
    p.add_argument("--weekly-time", help="每周健康检查时间 HH:MM（必填，无默认值）")
    p.add_argument("--out", help="输出目录，默认 <vault>/.obsidian-auto")
    p.add_argument("--write", action="store_true", help="把脚本与调度文件写入磁盘")
    args = p.parse_args(argv)

    vault, platform, tasks = build(args)
    base = base_dir(vault, args)
    name = args.name or vault.name

    payload = {
        "ok": True,
        "platform": platform,
        "vault": str(vault),
        "base_dir": str(base),
        "runner": args.runner,
        "tasks": [{"key": t["key"], "name": t["name"],
                   "schedule": {"frequency": t["frequency"], "day": t["day"],
                                "hour": t["hour"], "minute": t["minute"]},
                   "rrule": t["rrule"]} for t in tasks],
    }

    if platform == "workbuddy":
        payload["automations"] = [
            {**t, "scheduleType": "recurring", "status": "ACTIVE", "cwd": str(vault)}
            for t in tasks
        ]
    if platform == "json":
        payload["spec"] = {"vault": str(vault), "runner": args.runner, "tasks": tasks}

    if platform == "cron":
        payload["crontab"] = crontab_lines(tasks, base, platform)
    elif platform == "schtasks":
        payload["commands"] = schtasks_commands(tasks, base, name)
        payload["script"] = schtasks_script(tasks, base, name)
    elif platform == "launchd":
        label_base = f"com.obsidian-auto.{slugify(vault)}"
        payload["plists"] = {
            f"{label_base}.{t['key']}": plist_content(
                f"{label_base}.{t['key']}", base / "bin" / wrapper_name(t["key"], platform),
                base / "log" / f"{t['key']}.log", t["hour"], t["minute"],
                DAY_LAUNCHD[t["day"]] if t["frequency"] == "weekly" else None)
            for t in tasks
        }

    if args.write:
        payload["written"] = materialize(base, platform, tasks, vault, args.runner, name)
        payload["instructions"] = instructions_for(platform, base, name, tasks)
    else:
        payload["instructions"] = ["未写入磁盘；加 --write 生成 prompt、包装脚本与调度文件"]

    payload["summary_lines"] = [
        f"平台：{platform}；任务 {len(tasks)} 个（{', '.join(t['key'] for t in tasks)}）",
        f"路径：{base}",
    ]
    emit(payload)


if __name__ == "__main__":
    main()
