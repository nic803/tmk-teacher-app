from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class MultiplicationRoute:
    left: int
    right: int

    @property
    def product(self) -> int:
        return self.left * self.right

    def as_tuple(self) -> Tuple[int, int]:
        return (self.left, self.right)

    def as_dict(self) -> dict:
        return {"left": self.left, "right": self.right}


@dataclass(frozen=True)
class DivisionRoute:
    product: int
    divisor: int
    quotient: int

    def as_dict(self) -> dict:
        return {
            "product": self.product,
            "divisor": self.divisor,
            "quotient": self.quotient,
        }
