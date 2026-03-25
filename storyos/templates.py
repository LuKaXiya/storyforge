from __future__ import annotations

from datetime import datetime, timezone


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def story_template(book_id: str, title: str, genre: str) -> dict:
    return {
        'book_id': book_id,
        'title': title,
        'genre': genre,
        'created_at': now_iso(),
        'updated_at': now_iso(),
        'chapter_count': 0,
        'current_arc': 'opening',
        'logline': '',
        'premise': '',
        'tone': [],
    }


def world_template() -> dict:
    return {
        'timeline_day': 1,
        'active_locations': [],
        'open_questions': [],
        'recent_events': [],
        'known_truths': [],
    }


def characters_template() -> dict:
    return {
        'characters': [
            {
                'id': 'protagonist',
                'name': '主角',
                'role': 'protagonist',
                'location': 'unknown',
                'goals': [],
                'knowledge': [],
                'inventory': [],
                'status': 'active',
            }
        ]
    }


def resources_template() -> dict:
    return {
        'resources': [
            {
                'id': 'cash',
                'name': '现金',
                'quantity': 0,
                'unit': '元',
                'owner': 'protagonist',
            }
        ]
    }


def hooks_template() -> dict:
    return {
        'hooks': []
    }
