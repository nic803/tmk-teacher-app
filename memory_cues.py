from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, Final, Literal, Tuple

CueType = Literal["rhyme", "sequence", "story_link"]


@dataclass(frozen=True)
class MemoryCue:
    id: str
    product: int
    route: Tuple[int, int]
    cue_type: CueType
    cue_text: str
    child_text: str
    teacher_note: str


MEMORY_CUES: Final[Dict[str, MemoryCue]] = {
    "six_sixes_thirty_six": MemoryCue(
        id="six_sixes_thirty_six",
        product=36,
        route=(6, 6),
        cue_type="rhyme",
        cue_text="Six sixes are thirty-six.",
        child_text="Six sixes are thirty-six.",
        teacher_note=(
            "Useful rhyme anchor for 6×6. This is a retention support, not the primary mathematical explanation. "
            "Use after the child has seen 36 as a product hub and understands that 6×6 is one route into it."
        ),
    ),
    "five_six_seven_eight": MemoryCue(
        id="five_six_seven_eight",
        product=56,
        route=(7, 8),
        cue_type="sequence",
        cue_text="Five, six, seven, eight — 56 is 7×8.",
        child_text="Five, six, seven, eight — 56 is 7×8.",
        teacher_note=(
            "High-value memory anchor for the difficult 7×8 product. The sequence 5, 6, 7, 8 gives a sticky verbal hook. "
            "It also supports child-relevant story links through age progression: 7 now, 8 next year."
        ),
    ),
}


@lru_cache(maxsize=None)
def all_memory_cues() -> Tuple[MemoryCue, ...]:
    return tuple(MEMORY_CUES.values())


@lru_cache(maxsize=None)
def memory_cues_for_product(product: int) -> Tuple[MemoryCue, ...]:
    return tuple(cue for cue in MEMORY_CUES.values() if cue.product == product)


@lru_cache(maxsize=None)
def has_memory_cues(product: int) -> bool:
    return any(cue.product == product for cue in MEMORY_CUES.values())
