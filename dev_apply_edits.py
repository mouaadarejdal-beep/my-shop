#!/usr/bin/env python3
"""
Repo auto-editor for Hugo/Netlify projects.

✅ Creates folders/files
✅ Edits existing files safely (insert-if-missing / regex replace)
✅ Makes .bak backups
✅ Dry run mode

Usage:
  python dev_apply_edits.py /path/to/my-shop --apply
  python dev_apply_edits.py . --apply
  python dev_apply_edits.py . --dry-run
"""

from __future__ import annotations
import argparse
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional


# -------------------------
# Helpers
# -------------------------

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")

def write_text(p: Path, content: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

def backup_file(p: Path) -> Path:
    bak = p.with_suffix(p.suffix + ".bak")
    shutil.copy2(p, bak)
    return bak

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def rel(p: Path, root: Path) -> str:
    try:
        return str(p.relative_to(root))
    except Exception:
        return str(p)

def contains(haystack: str, needle: str) -> bool:
    return needle in haystack

def insert_after_anchor(content: str, anchor: str, insert_block: str) -> str:
    """
    Inserts insert_block right after the first occurrence of anchor.
    If anchor not found, appends insert_block at the end.
    """
    idx = content.find(anchor)
    if idx == -1:
        if not content.endswith("\n"):
            content += "\n"
        return content + insert_block
    idx_end = idx + len(anchor)
    return content[:idx_end] + insert_block + content[idx_end:]


# -------------------------
# Action system
# -------------------------

@dataclass
class ActionResult:
    changed: bool
    message: str

ActionFn = Callable[[Path, bool], ActionResult]


def action_create_file(path_rel: str, content: str, overwrite: bool = False) -> ActionFn:
    def run(root: Path, dry_run: bool) -> ActionResult:
        p = root / path_rel
        if p.exists() and not overwrite:
            return ActionResult(False, f"SKIP (exists): {path_rel}")
        if dry_run:
            return ActionResult(True, f"WOULD CREATE: {path_rel} ({'overwrite' if p.exists() else 'new'})")
        if p.exists():
            backup_file(p)
        write_text(p, content)
        return ActionResult(True, f"CREATED: {path_rel}")
    return run


def action_regex_replace_glob(glob_pattern: str, pattern: str, repl: str, flags: int = 0) -> ActionFn:
    rx = re.compile(pattern, flags)

    def run(root: Path, dry_run: bool) -> ActionResult:
        changed_any = False
        msgs = []
        for p in root.rglob(glob_pattern):
            if not p.is_file():
                continue
            old = read_text(p)
            new, n = rx.subn(repl, old)
            if n > 0 and new != old:
                changed_any = True
                if dry_run:
                    msgs.append(f"WOULD EDIT: {rel(p, root)} (replacements={n})")
                else:
                    backup_file(p)
                    write_text(p, new)
                    msgs.append(f"EDITED: {rel(p, root)} (replacements={n})")
        if not changed_any:
            return ActionResult(False, f"NO MATCHES for {glob_pattern} / {pattern}")
        return ActionResult(True, "\n".join(msgs))
    return run


def action_insert_if_missing(file_rel: str, needle: str, insert_block: str, anchor: Optional[str] = None) -> ActionFn:
    def run(root: Path, dry_run: bool) -> ActionResult:
        p = root / file_rel
        if not p.exists():
            return ActionResult(False, f"SKIP (missing): {file_rel}")
        content = read_text(p)
        if contains(content, needle):
            return ActionResult(False, f"SKIP (already contains needle): {file_rel}")
        new = content
        if anchor:
            new = insert_after_anchor(new, anchor, insert_block)
        else:
            if not new.endswith("\n"):
                new += "\n"
            new += insert_block

        if dry_run:
            return ActionResult(True, f"WOULD INSERT into: {file_rel}")
        backup_file(p)
        write_text(p, new)
        return ActionResult(True, f"INSERTED into: {file_rel}")
    return run


# -------------------------
# “Edits” you want applied
# -------------------------

CART_JS = r"""// Simple cart (localStorage) - you can expand later
(function () {
  const KEY = "myshop_cart_v1";

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY)) || []; }
    catch(e) { return []; }
  }
  function write(items) {
    localStorage.setItem(KEY, JSON.stringify(items));
    window.dispatchEvent(new CustomEvent("cart:updated", { detail: { items } }));
  }

  function add(item) {
    const items = read();
    const idx = items.findIndex(x => x.id === item.id);
    if (idx >= 0) items[idx].qty += item.qty || 1;
    else items.push({ ...item, qty: item.qty || 1 });
    write(items);
  }

  function remove(id) {
    write(read().filter(x => x.id !== id));
  }

  function updateQty(id, qty) {
    const items = read();
    const idx = items.findIndex(x => x.id === id);
    if (idx >= 0) {
      items[idx].qty = Math.max(1, parseInt(qty || 1, 10));
      write(items);
    }
  }

  function total() {
    return read().reduce((sum, x) => sum + (Number(x.price) * Number(x.qty)), 0);
  }

  window.MyShopCart = { read, add, remove, updateQty, total };
})();
"""

SEO_PARTIAL = r"""{{/* Basic SEO partial */}}
{{- $title := .Title -}}
{{- $desc := .Params.description | default .Site.Params.description | default "" -}}
<title>{{ $title }} | {{ .Site.Title }}</title>
<meta name="description" content="{{ $desc }}">
<meta property="og:title" content="{{ $title }} | {{ .Site.Title }}">
<meta property="og:description" content="{{ $desc }}">
<meta property="og:type" content="website">
<meta property="og:url" content="{{ .Permalink }}">
<meta name="twitter:card" content="summary_large_image">
"""

# Example: inject SEO partial into base layout (only if you have layouts/_default/baseof.html)
SEO_INSERT_BLOCK = "\n  {{ partial \"seo.html\" . }}\n"


def build_actions() -> list[ActionFn]:
    actions: list[ActionFn] = []

    # Create common folders/files
    actions.append(action_create_file("assets/js/cart.js", CART_JS, overwrite=False))
    actions.append(action_create_file("layouts/partials/seo.html", SEO_PARTIAL, overwrite=False))

    # Inject SEO partial into base layout if exists (safe insert)
    actions.append(
        action_insert_if_missing(
            file_rel="layouts/_default/baseof.html",
            needle='partial "seo.html"',
            insert_block=SEO_INSERT_BLOCK,
            anchor="<head>"
        )
    )

    # Example “global replace” across templates (change placeholder store name)
    # You can remove this if you don’t want it.
    actions.append(
        action_regex_replace_glob(
            glob_pattern="**/*.html",
            pattern=r"\bFinalFF12\b",
            repl="My Shop",
            flags=0
        )
    )

    return actions


# -------------------------
# Main
# -------------------------

def looks_like_repo(root: Path) -> bool:
    # very light checks: has hugo structure or netlify
    return (root / "netlify.toml").exists() or (root / "config.toml").exists() or (root / "hugo.toml").exists() or (root / "content").exists()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", help="Path to the cloned repo folder")
    ap.add_argument("--dry-run", action="store_true", help="Show what would change")
    ap.add_argument("--apply", action="store_true", help="Actually apply changes")
    args = ap.parse_args()

    root = Path(args.repo).expanduser().resolve()
    if not root.exists():
        print(f"❌ Repo path not found: {root}")
        return 2

    if not looks_like_repo(root):
        print(f"⚠️ This folder doesn't look like a Hugo/Netlify repo: {root}")
        print("   (Still continuing — but double-check the path.)")

    if args.dry_run and args.apply:
        print("❌ Choose only one: --dry-run OR --apply")
        return 2

    dry = True
    if args.apply:
        dry = False
    elif args.dry_run:
        dry = True
    else:
        print("❌ Please choose one: --dry-run or --apply")
        return 2

    actions = build_actions()

    print(f"{'🔎 DRY RUN' if dry else '✅ APPLYING CHANGES'} in: {root}\n")

    changed_count = 0
    for i, act in enumerate(actions, 1):
        res = act(root, dry)
        if res.changed:
            changed_count += 1
        print(f"[{i}/{len(actions)}] {res.message}\n")

    print(f"Done. Actions that would change something: {changed_count}/{len(actions)}")
    if dry:
        print("Run again with --apply to actually write changes.")
    else:
        print("Backups were created as *.bak next to edited files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
