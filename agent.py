#!/usr/bin/env python3
"""
Daily Reflection Tree — CLI Agent
Loads the tree from reflection-tree.json and walks the employee through
a fully deterministic end-of-day reflection session.

No LLM calls at runtime. Deterministic. Auditable.
"""

import json
import sys
import os
import time
from pathlib import Path


# ─── Colour helpers (ANSI) ───────────────────────────────────────────────────

def blue(text):    return f"\033[34m{text}\033[0m"
def green(text):   return f"\033[32m{text}\033[0m"
def yellow(text):  return f"\033[33m{text}\033[0m"
def cyan(text):    return f"\033[36m{text}\033[0m"
def bold(text):    return f"\033[1m{text}\033[0m"
def dim(text):     return f"\033[2m{text}\033[0m"
def purple(text):  return f"\033[35m{text}\033[0m"


# ─── State ───────────────────────────────────────────────────────────────────

class ReflectionState:
    def __init__(self):
        self.answers = {}          # node_id → answer string
        self.signals = {           # axis signal tallies
            "axis1": {"internal": 0, "external": 0},
            "axis2": {"contribution": 0, "entitlement": 0},
            "axis3": {"self": 0, "other": 0, "transcend": 0},
        }

    def record_answer(self, node_id: str, answer: str):
        self.answers[node_id] = answer

    def record_signal(self, signal: str):
        if not signal:
            return
        parts = signal.split(":")
        if len(parts) == 2:
            axis, pole = parts
            if axis in self.signals and pole in self.signals[axis]:
                self.signals[axis][pole] += 1

    def dominant(self, axis: str) -> str:
        counts = self.signals.get(axis, {})
        if not counts:
            return "mixed"
        return max(counts, key=counts.get)

    def axis_summary(self, axis: str, templates: dict) -> str:
        dom = self.dominant(axis)
        return templates.get(axis, {}).get("summary", {}).get(dom, "")

    def interpolate(self, text: str, summary_templates: dict) -> str:
        """Replace {node_id.answer} and {axis.summary} placeholders."""
        result = text
        # Answer interpolations
        for node_id, answer in self.answers.items():
            result = result.replace(f"{{{node_id}.answer}}", answer)
        # Axis summary interpolations
        for axis in ["axis1", "axis2", "axis3"]:
            summary = self.axis_summary(axis, summary_templates)
            result = result.replace(f"{{{axis}.summary}}", summary)
        return result


# ─── Tree loader ─────────────────────────────────────────────────────────────

def load_tree(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    nodes = {node["id"]: node for node in data["nodes"]}
    return nodes, data.get("state_templates", {})


# ─── Display helpers ─────────────────────────────────────────────────────────

def clear_line():
    print("\033[2K\r", end="", flush=True)

def slow_print(text: str, delay: float = 0.018):
    """Print text character by character for a natural feel."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def print_divider():
    print(dim("─" * 60))

def print_node_header(node_type: str):
    labels = {
        "start":      ("🌙", ""),
        "question":   ("💬", cyan("  Question")),
        "reflection": ("✦",  green(" Reflection")),
        "bridge":     ("→",  dim("  ...")),
        "summary":    ("📋", purple(" Your Day")),
        "end":        ("✓",  ""),
        "decision":   ("",   ""),
    }
    icon, label = labels.get(node_type, ("", ""))
    if icon:
        print(f"\n{bold(icon)}{label}")
        print_divider()


def print_reflection(text: str):
    """Print reflection text with word-wrap at 60 chars."""
    words = text.split()
    line = ""
    for word in words:
        if len(line) + len(word) + 1 > 60:
            slow_print(f"  {line}", delay=0.01)
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        slow_print(f"  {line}", delay=0.01)


def prompt_choice(options: list) -> str:
    """Show numbered options, return chosen option text."""
    for i, opt in enumerate(options, 1):
        print(f"  {dim(str(i) + '.')} {opt}")
    print()
    while True:
        raw = input(bold("  → ")).strip()
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
        # Also allow typing part of the option
        matches = [o for o in options if raw.lower() in o.lower()]
        if len(matches) == 1:
            return matches[0]
        print(dim("  Please enter a number from the list above."))


def wait_continue():
    input(dim("  [Press Enter to continue]"))


# ─── Decision router ─────────────────────────────────────────────────────────

def resolve_decision(node: dict, state: ReflectionState) -> str:
    """
    Decision nodes have options as a list of {match: [...], target: str}.
    Find the first matching rule and return its target node ID.
    """
    options = node["options"]
    # Find the answer from the parent question
    parent_id = node["parentId"]
    last_answer = state.answers.get(parent_id, "")

    for rule in options:
        if last_answer in rule["match"]:
            return rule["target"]

    # Fallback: return first target
    return options[0]["target"]


# ─── Main walker ─────────────────────────────────────────────────────────────

def run_session(tree_path: str):
    nodes, summary_templates = load_tree(tree_path)
    state = ReflectionState()

    # Find the start node
    start_node = next((n for n in nodes.values() if n["type"] == "start"), None)
    if not start_node:
        print("Error: No start node found in tree.")
        sys.exit(1)

    current_id = start_node["id"]
    os.system("clear" if os.name == "posix" else "cls")

    print("\n" + "═" * 60)
    print(bold("   DAILY REFLECTION TREE"))
    print("═" * 60 + "\n")

    while current_id:
        node = nodes.get(current_id)
        if not node:
            print(f"Error: Node '{current_id}' not found.")
            break

        node_type = node["type"]
        text = state.interpolate(node.get("text") or "", summary_templates)
        options = node.get("options", [])
        target = node.get("target")
        signal = node.get("signal")

        # ── start ──────────────────────────────────────────────
        if node_type == "start":
            print_node_header("start")
            slow_print(f"  {text}")
            print()
            wait_continue()
            current_id = target

        # ── question ───────────────────────────────────────────
        elif node_type == "question":
            print_node_header("question")
            print_reflection(text)
            print()
            chosen = prompt_choice(options)
            state.record_answer(current_id, chosen)
            if signal:
                state.record_signal(signal)
            current_id = target or _find_child(nodes, current_id)

        # ── decision ───────────────────────────────────────────
        elif node_type == "decision":
            next_id = resolve_decision(node, state)
            current_id = next_id

        # ── reflection ─────────────────────────────────────────
        elif node_type == "reflection":
            print_node_header("reflection")
            print_reflection(text)
            print()
            if signal:
                state.record_signal(signal)
            wait_continue()
            current_id = target or _find_child(nodes, current_id)

        # ── bridge ─────────────────────────────────────────────
        elif node_type == "bridge":
            print_node_header("bridge")
            slow_print(f"  {text}", delay=0.012)
            print()
            time.sleep(0.6)
            current_id = target or _find_child(nodes, current_id)

        # ── summary ────────────────────────────────────────────
        elif node_type == "summary":
            print_node_header("summary")
            print_reflection(text)
            print()
            wait_continue()
            current_id = target or _find_child(nodes, current_id)

        # ── end ────────────────────────────────────────────────
        elif node_type == "end":
            print_node_header("end")
            slow_print(f"  {text}")
            print()
            print("═" * 60 + "\n")
            _print_session_stats(state)
            break

        else:
            # Unknown type — skip
            current_id = target or _find_child(nodes, current_id)


def _find_child(nodes: dict, parent_id: str) -> str | None:
    """Find the first child of a node by parentId."""
    for node in nodes.values():
        if node.get("parentId") == parent_id:
            return node["id"]
    return None


def _print_session_stats(state: ReflectionState):
    """Print a compact session summary."""
    print(dim("  Session snapshot"))
    print(dim("  ─────────────────────────────────────"))
    for axis, counts in state.signals.items():
        dom = max(counts, key=counts.get) if counts else "—"
        total = sum(counts.values())
        if total > 0:
            label = f"  {axis.upper()}: {dom.upper()} ({counts})"
            print(dim(label))
    print()


# ─── Entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Default: look for tree relative to this script
    script_dir = Path(__file__).parent
    default_tree = script_dir.parent / "tree" / "reflection-tree.json"

    if len(sys.argv) > 1:
        tree_file = sys.argv[1]
    else:
        tree_file = str(default_tree)

    if not Path(tree_file).exists():
        print(f"Error: Tree file not found at '{tree_file}'")
        print("Usage: python agent.py [path/to/reflection-tree.json]")
        sys.exit(1)

    try:
        run_session(tree_file)
    except KeyboardInterrupt:
        print("\n\n  Session ended early. See you tomorrow.\n")
