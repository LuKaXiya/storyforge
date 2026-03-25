from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .auditor import audit_text
from .planner import build_plan
from .storage import StoryRepo
from .templates import (
    story_template,
    world_template,
    characters_template,
    resources_template,
    hooks_template,
)


ROOT = Path(__file__).resolve().parent.parent / 'workspace'
DATA_ROOT = Path(__file__).resolve().parent.parent / 'books'


def repo() -> StoryRepo:
    return StoryRepo(DATA_ROOT)


def cmd_init(args: argparse.Namespace) -> int:
    r = repo()
    book = r.ensure_book_dirs(args.book_id)
    r.write_json(book / 'story.json', story_template(args.book_id, args.title, args.genre))
    r.write_json(book / 'state' / 'world.json', world_template())
    r.write_json(book / 'state' / 'characters.json', characters_template())
    r.write_json(book / 'state' / 'resources.json', resources_template())
    r.write_json(book / 'state' / 'hooks.json', hooks_template())
    print(f'Initialized book at {book}')
    return 0


def next_chapter_number(book_dir: Path) -> int:
    plans_dir = book_dir / 'plans'
    nums = []
    for path in plans_dir.glob('chapter-*.json'):
        try:
            nums.append(int(path.stem.split('-')[1]))
        except Exception:
            continue
    return max(nums, default=0) + 1


def cmd_plan(args: argparse.Namespace) -> int:
    r = repo()
    book = r.book_path(args.book_id)
    if not book.exists():
        raise SystemExit(f'Book not found: {args.book_id}')
    chapter_number = args.chapter or next_chapter_number(book)
    plan = build_plan(chapter_number, args.goal, args.conflict)
    out = book / 'plans' / f'chapter-{chapter_number:03d}.json'
    r.write_json(out, asdict(plan))
    print(json.dumps(asdict(plan), ensure_ascii=False, indent=2))
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    r = repo()
    book = r.book_path(args.book_id)
    if not book.exists():
        raise SystemExit(f'Book not found: {args.book_id}')
    text = Path(args.text_file).read_text(encoding='utf-8') if args.text_file else ''
    characters = r.read_json(book / 'state' / 'characters.json')
    resources = r.read_json(book / 'state' / 'resources.json')
    hooks = r.read_json(book / 'state' / 'hooks.json')
    findings = [asdict(f) for f in audit_text(text, characters, resources, hooks)]
    out = book / 'audits' / f'chapter-{args.chapter:03d}.json'
    r.write_json(out, {'chapter': args.chapter, 'findings': findings})
    print(json.dumps({'chapter': args.chapter, 'findings': findings}, ensure_ascii=False, indent=2))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    r = repo()
    book = r.book_path(args.book_id)
    story = r.read_json(book / 'story.json')
    plan_count = len(list((book / 'plans').glob('chapter-*.json')))
    audit_count = len(list((book / 'audits').glob('chapter-*.json')))
    result = {
        'book_id': story['book_id'],
        'title': story['title'],
        'genre': story['genre'],
        'current_arc': story['current_arc'],
        'plans': plan_count,
        'audits': audit_count,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog='storyos')
    sub = p.add_subparsers(dest='command', required=True)

    sp = sub.add_parser('init')
    sp.add_argument('book_id')
    sp.add_argument('--title', required=True)
    sp.add_argument('--genre', required=True)
    sp.set_defaults(func=cmd_init)

    sp = sub.add_parser('plan')
    sp.add_argument('book_id')
    sp.add_argument('--chapter', type=int)
    sp.add_argument('--goal', required=True)
    sp.add_argument('--conflict', required=True)
    sp.set_defaults(func=cmd_plan)

    sp = sub.add_parser('audit')
    sp.add_argument('book_id')
    sp.add_argument('--chapter', type=int, required=True)
    sp.add_argument('--text-file', required=True)
    sp.set_defaults(func=cmd_audit)

    sp = sub.add_parser('status')
    sp.add_argument('book_id')
    sp.set_defaults(func=cmd_status)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)
