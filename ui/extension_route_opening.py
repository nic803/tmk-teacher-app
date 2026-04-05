from dataclasses import dataclass, field
from typing import List, Tuple, Optional


FactorRoute = Tuple[int, int]


@dataclass
class TwelveRouteOpeningProduct:
    product: int
    intro_route: Optional[FactorRoute]
    core_routes: List[FactorRoute] = field(default_factory=list)
    extension_routes: List[FactorRoute] = field(default_factory=list)
    teacher_focus: str = ""
