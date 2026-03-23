from __future__ import annotations

from products import product_record


def canonical_route(route: tuple[int, int]) -> tuple[int, int]:
    a, b = route
    return (a, b) if a <= b else (b, a)


def distinct_factor_routes(product: int) -> list[tuple[int, int]]:
    record = product_record(product)
    seen: set[tuple[int, int]] = set()
    routes: list[tuple[int, int]] = []

    intro = canonical_route(record.intro_route)
    seen.add(intro)
    routes.append(intro)

    for route in record.factor_families:
        canonical = canonical_route(route)
        if canonical not in seen:
            seen.add(canonical)
            routes.append(canonical)

    return routes


def entry_routes(product: int) -> list[tuple[int, int]]:
    return distinct_factor_routes(product)


def exit_route_labels(product: int, limit: int | None = None) -> list[str]:
    record = product_record(product)
    labels = [f"{product}÷{divisor}={quotient}" for divisor, quotient in record.ways_out]
    if limit is None:
        return labels
    return labels[:limit]


def inverse_labels(product: int) -> tuple[str, ...]:
    record = product_record(product)
    return tuple(f"{product}÷{divisor}={quotient}" for divisor, quotient in record.ways_out)


def shared_factors(product_a: int, product_b: int) -> str:
    factors_a = {n for route in distinct_factor_routes(product_a) for n in route}
    factors_b = {n for route in distinct_factor_routes(product_b) for n in route}
    shared = sorted(factors_a.intersection(factors_b))
    return ", ".join(str(n) for n in shared) if shared else "none"
