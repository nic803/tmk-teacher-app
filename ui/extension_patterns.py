from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class PatternExample:
    expression: str
    working: Optional[str] = None


@dataclass(frozen=True)
class ExtensionPattern:
    pattern_id: str
    family: str  # "11x" or "12x"
    title: str
    rule: str
    teacher_explanation: str
    teaching_use: str
    examples: List[PatternExample] = field(default_factory=list)
    cue: Optional[str] = None
    cue_explanation: Optional[str] = None
