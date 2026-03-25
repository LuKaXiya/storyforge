from __future__ import annotations

from .models import ChapterPlan, PlanBeat


def build_plan(chapter_number: int, goal: str, conflict: str) -> ChapterPlan:
    beats = [
        PlanBeat(
            title='开场扰动',
            purpose='让本章目标尽快出现，避免空转铺垫',
            tension=f'主角面临核心问题：{goal}',
        ),
        PlanBeat(
            title='冲突升级',
            purpose='把外部障碍和内部犹豫同时抬高',
            tension=conflict,
        ),
        PlanBeat(
            title='决策与代价',
            purpose='让角色做出不可逆选择，并留下后果',
            tension='选择之后必须付出某种代价或埋下后患',
        ),
    ]
    return ChapterPlan(
        chapter_number=chapter_number,
        goal=goal,
        conflict=conflict,
        beats=beats,
        state_updates=[
            {'type': 'world_event', 'description': goal},
            {'type': 'character_shift', 'description': conflict},
        ],
        hooks_to_open=['本章新悬念待补充'],
        hooks_to_progress=['若已有旧伏笔，本章至少推进其中一条'],
    )
