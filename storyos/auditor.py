from __future__ import annotations

import re
from typing import List

from .models import AuditFinding


SUMMARY_PATTERNS = [
    '总而言之', '毫无疑问', '不得不说', '可以说', '显然', '某种意义上'
]


def audit_text(text: str, characters: dict, resources: dict, hooks: dict) -> List[AuditFinding]:
    findings: List[AuditFinding] = []

    known_names = {c['name'] for c in characters.get('characters', [])}
    for token in re.findall(r'[\u4e00-\u9fffA-Za-z0-9_]{2,12}', text):
        if token.endswith('说道') or token.endswith('看着'):
            continue
        if token in {'主角', '灵气', '系统', '今天', '那里'}:
            continue
        if token in known_names:
            break
    # name check via quoted speaker patterns
    speaker_mentions = re.findall(r'([\u4e00-\u9fff]{2,4})[：:「『"]', text)
    for name in speaker_mentions:
        if name not in known_names:
            findings.append(AuditFinding('warning', 'UNKNOWN_CHARACTER', f'检测到未登记角色名：{name}', evidence=name))

    for phrase in SUMMARY_PATTERNS:
        count = text.count(phrase)
        if count >= 2:
            findings.append(AuditFinding('warning', 'AI_STYLE_SUMMARY', f'总结式表达偏多：{phrase} 出现 {count} 次', evidence=phrase))

    repeated = re.findall(r'(.{8,30})\1', text)
    if repeated:
        findings.append(AuditFinding('warning', 'REPETITION', '检测到可能的重复片段', evidence=repeated[0][:50]))

    closed_hooks = {h['title'] for h in hooks.get('hooks', []) if h.get('status') == 'closed'}
    for hook in closed_hooks:
        if hook in text:
            findings.append(AuditFinding('warning', 'CLOSED_HOOK_REUSED', f'已关闭伏笔再次出现：{hook}', evidence=hook))

    resource_names = {r['name']: r for r in resources.get('resources', [])}
    consumption = re.findall(r'消耗了([\u4e00-\u9fffA-Za-z0-9_]+)', text)
    for item in consumption:
        if item not in resource_names:
            findings.append(AuditFinding('warning', 'UNKNOWN_RESOURCE', f'文本中消耗了未登记资源：{item}', evidence=item))

    if not text.strip():
        findings.append(AuditFinding('error', 'EMPTY_TEXT', '章节文本为空'))

    return findings
