from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class StoryRepo:
    def __init__(self, root: Path):
        self.root = Path(root)

    def book_path(self, book_id: str) -> Path:
        return self.root / book_id

    def ensure_book_dirs(self, book_id: str) -> Path:
        book = self.book_path(book_id)
        for name in ['state', 'chapters', 'plans', 'audits', 'drafts']:
            (book / name).mkdir(parents=True, exist_ok=True)
        return book

    def write_json(self, path: Path, data: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    def read_json(self, path: Path) -> Any:
        return json.loads(path.read_text(encoding='utf-8'))

    def exists(self, path: Path) -> bool:
        return path.exists()
