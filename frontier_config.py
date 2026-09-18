#!/usr/bin/env python3
"""Shared config for Frontier. Everything personal (paths, IDs, LLM choice) lives in
config.json — which is gitignored — so a fork never has to edit code to make it theirs.

Missing config.json is fine: the defaults below give you the minimal public build
(YouTube sources -> index.html), with vault/Feishu/LLM extras switched off.
"""
import json, pathlib, shutil, copy

HERE = pathlib.Path(__file__).resolve().parent
_CFG = HERE / "config.json"

DEFAULTS = {
    "llm": {
        # "claude" | "codex" | "none" | "custom"
        # "none" = skip AI previews entirely; the daily still builds, just without
        # the Editor's note and the 预习 notes.
        "provider": "none",
        "model": "",
        # only for provider == "custom": prompt is appended as the final argv item
        "command": [],
        "timeout_sec": 300,
    },
    "vault": {
        "enabled": False,
        "path": "~/Documents/Brain",
        "notes_subdir": "wiki/daily-preview",
        "vault_name": "Brain",
        "git_commit": False,
    },
    "feishu": {
        "enabled": False,
        "receiver_id": "",      # ou_xxx (person) or oc_xxx (group chat)
        "lark_cli": "",         # "" -> auto-detect on PATH
    },
    "site": {
        "url": "",
        "twitter": "",
        "repo": "https://github.com/hiamberhuang/frontier",
    },
    "sources": {
        # Zara Zhang's follow-builders skill feed. Optional: absent -> Frontier
        # builds from your own YouTube roster alone.
        "follow_builders_dir": "~/.claude/skills/follow-builders",
    },
}

# Built-in LLM presets. `{prompt}` is substituted; `{model}` dropped when empty.
# Verified locally: claude. NOT verified locally: codex (no codex CLI on the box
# this was written on) — if it misbehaves, use provider "custom" and set the exact
# argv yourself. That's the whole point of the escape hatch.
LLM_PRESETS = {
    "claude": {"bin": "claude", "args": ["--model", "{model}", "-p", "{prompt}"],
               "default_model": "claude-sonnet-4-6"},
    "codex":  {"bin": "codex",  "args": ["exec", "--model", "{model}", "{prompt}"],
               "default_model": "gpt-5-codex"},
}


def _deep_merge(base, over):
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        out[k] = _deep_merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def load():
    user = {}
    if _CFG.exists():
        try:
            user = json.load(open(_CFG, encoding="utf-8"))
        except Exception as e:
            print(f"⚠ config.json 读不了({e})，用默认值")
    return _deep_merge(DEFAULTS, user)


CFG = load()


def path(*keys, default=""):
    """Read a dotted config path and expand ~."""
    cur = CFG
    for k in keys:
        cur = (cur or {}).get(k, None)
        if cur is None:
            cur = default
            break
    return pathlib.Path(str(cur)).expanduser() if cur else None


def llm_argv(prompt):
    """Build the argv for a one-shot LLM call, or None if no LLM is configured.
    Callers MUST handle None — an unconfigured LLM is a normal state, not an error."""
    c = CFG["llm"]
    prov = (c.get("provider") or "none").lower()
    if prov in ("none", "", "off"):
        return None
    if prov == "custom":
        argv = list(c.get("command") or [])
        return (argv + [prompt]) if argv else None
    pre = LLM_PRESETS.get(prov)
    if not pre:
        print(f"⚠ 不认识的 llm.provider: {prov} → 跳过 AI 环节")
        return None
    exe = shutil.which(pre["bin"]) or str(pathlib.Path.home() / ".local/bin" / pre["bin"])
    if not pathlib.Path(exe).exists():
        print(f"⚠ 找不到 {pre['bin']} CLI → 跳过 AI 环节")
        return None
    model = c.get("model") or pre["default_model"]
    argv = [exe]
    for a in pre["args"]:
        if a == "{model}" and not model:
            continue
        argv.append(a.replace("{model}", model).replace("{prompt}", prompt))
    return argv


def lark_cli():
    """Path to lark-cli, or None. Auto-detect beats hardcoding: fnm moves node paths."""
    explicit = CFG["feishu"].get("lark_cli") or ""
    if explicit:
        p = pathlib.Path(explicit).expanduser()
        return str(p) if p.exists() else None
    found = shutil.which("lark-cli")
    return found or None
