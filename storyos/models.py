from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class PlanBeat:
    title: str
    purpose: str
    tension: str


@dataclass
class ChapterPlan:
    chapter_number: int
    goal: str
    conflict: str
    beats: List[PlanBeat] = field(default_factory=list)
    state_updates: List[Dict] = field(default_factory=list)
    hooks_to_open: List[str] = field(default_factory=list)
    hooks_to_progress: List[str] = field(default_factory=list)


@dataclass
class AuditFinding:
    severity: str
    code: str
    message: str
    evidence: str = ''
