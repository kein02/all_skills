# -*- coding: utf-8 -*-
"""共享的定时任务定义。

scaffold.py（宿主自动化工具）与 schedule.py（OS 级调度）共用这一份 prompt，
避免两套实现漂移。任务内容是纯文本，不依赖任何宿主专有 API。

时间不做默认：daily_time / weekly_time 必须由调用方（用户）给出。
"""

SKILL_NAME = "obsidian-auto"

DAY_CN = {"MO": "一", "TU": "二", "WE": "三", "TH": "四", "FR": "五", "SA": "六", "SU": "日"}
DAY_CRON = {"MO": "1", "TU": "2", "WE": "3", "TH": "4", "FR": "5", "SA": "6", "SU": "0"}
DAY_SCHTASKS = {"MO": "MON", "TU": "TUE", "WE": "WED", "TH": "THU", "FR": "FRI", "SA": "SAT", "SU": "SUN"}
DAY_LAUNCHD = {"SU": 0, "MO": 1, "TU": 2, "WE": 3, "TH": 4, "FR": 5, "SA": 6}


def parse_hhmm(value):
    hour, minute = value.split(":")
    return int(hour), int(minute)


def build_tasks(path, name, categories, daily_time, weekly_day, weekly_time):
    """返回两个任务：每日整理 / 每周健康检查。时间必须由用户指定。"""
    wiki_targets = "、".join(f"wiki/{c}" for c in categories)
    dh, dm = parse_hhmm(daily_time)
    wh, wm = parse_hhmm(weekly_time)

    daily_prompt = (
        f"对 Obsidian 知识库 {path} 执行每日增量整理：1) 先完整读取该仓库根目录的 AGENTS.md，"
        f"严格按其中的工作规范执行；2) 对照 log.md 末尾的记录判断 raw/ 中哪些资料已处理过（形成基线），"
        f"逐一核对 raw/ 下每个文件的字节数与 mtime，找出新增或发生变化的资料；3) 若无新增、无变化，"
        f"直接结束，不改动任何文件；4) 若有新增或变化，按规范整理进 {wiki_targets} 目录，页面之间建立双链，"
        f"并同步更新 index.md 与 log.md；5) raw/ 只读，禁止修改、删除、重命名、覆盖 raw/ 内任何文件；"
        f"6) 删除文件、批量重命名、调整目录结构、裁决冲突类操作一律不要执行，整理成待确认问题写入 log.md。"
    )
    weekly_prompt = (
        f"对 Obsidian 知识库 {path} 执行每周健康检查：1) 先完整读取该仓库根目录的 AGENTS.md；"
        f"2) 扫描 wiki/ 全部页面、index.md、README.md，找出无效双链（指向不存在页面的真实 [[链接]]；"
        f"行内代码 `[[双链]]` 按规范不计）、孤立页面（无任何入链和出链的页面）、结论冲突或标注"
        f"「冲突待裁决」的知识页、各页更新时间与文件 mtime 不一致的页面；3) 整理成清单（含页面位置与建议处理方式）；"
        f"4) 检查阶段严禁改动 wiki/、index.md、log.md、README.md 中的任何文件；"
        f"5) 把检查结论写入该仓库 .workbuddy/memory/ 或 .obsidian-auto/log/ 下的执行记录文件"
        f"（都不存在则创建），输出等用户确认的清单摘要。"
    )

    return [
        {
            "key": "daily",
            "name": f"{name}每日整理（raw → wiki）",
            "rrule": f"FREQ=DAILY;BYHOUR={dh};BYMINUTE={dm}",
            "frequency": "daily",
            "day": None,
            "hour": dh,
            "minute": dm,
            "prompt": daily_prompt,
        },
        {
            "key": "weekly",
            "name": f"{name}每周健康检查（双链 / 孤立页 / 冲突）",
            "rrule": f"FREQ=WEEKLY;BYDAY={weekly_day};BYHOUR={wh};BYMINUTE={wm}",
            "frequency": "weekly",
            "day": weekly_day,
            "hour": wh,
            "minute": wm,
            "prompt": weekly_prompt,
        },
    ]
