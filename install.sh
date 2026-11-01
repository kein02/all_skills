#!/usr/bin/env bash
# all_skills 一键安装：把仓库中的某个 skill 拷入 Agent 的 skills 目录
# 用法：
#   一键：curl -fsSL https://raw.githubusercontent.com/kein02/all_skills/main/install.sh | bash -s -- <skill名>
#   本地：在本仓库目录内执行 ./install.sh <skill名>
# 可用环境变量 SKILLS_DIR 覆盖安装目标（默认 ~/.agents/skills）
set -euo pipefail

REPO_URL="https://github.com/kein02/all_skills.git"
SKILL="${1:-}"

if [ -z "$SKILL" ]; then
  echo "用法: install.sh <skill名>，例如: install.sh readme-writer" >&2
  exit 1
fi

DEST_BASE="${SKILLS_DIR:-$HOME/.agents/skills}"

# 定位 skill 源：优先使用当前目录里的仓库副本，否则浅克隆到临时目录
if [ -f "$SKILL/SKILL.md" ]; then
  SRC="$PWD/$SKILL"
  TMP=""
else
  TMP="$(mktemp -d)"
  git clone --depth 1 "$REPO_URL" "$TMP" >&2
  if [ ! -d "$TMP/$SKILL" ]; then
    echo "仓库中不存在 skill: $SKILL" >&2
    rm -rf "$TMP"
    exit 1
  fi
  SRC="$TMP/$SKILL"
fi

mkdir -p "$DEST_BASE"
DEST="$DEST_BASE/$SKILL"
if [ -e "$DEST" ]; then
  BACKUP="$DEST.bak.$(date +%Y%m%d%H%M%S)"
  mv "$DEST" "$BACKUP"
  echo "旧版本已备份到 $BACKUP"
fi
cp -r "$SRC" "$DEST"
if [ -n "$TMP" ]; then
  rm -rf "$TMP"
fi

echo "✅ 已安装 $SKILL -> $DEST"
echo "验证：新开一个 Agent 会话，试试能否自动触发该 skill"
