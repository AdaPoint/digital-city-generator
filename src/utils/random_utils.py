# src/utils/random_utils.py

"""
Random utilities for the Digital City generator.

- RNG: thin wrapper over random.Random for deterministic behavior.
- allocate_discrete: allocate an integer total across categories according to weights.
"""

import random
from typing import Dict, Hashable, List, Tuple


class RNG:
    def __init__(self, seed: int):
        self.seed = seed
        self._rng = random.Random(seed)

    def random(self) -> float:
        """Uniform float in [0.0, 1.0)."""
        return self._rng.random()

    def randint(self, a: int, b: int) -> int:
        """Random integer N such that a <= N <= b."""
        return self._rng.randint(a, b)


def allocate_discrete(total: int, weights: Dict[Hashable, float], rng: RNG) -> Dict[Hashable, int]:
    """
    Allocate `total` integer units across keys in `weights`,
    proportional to the provided weights.

    Returns a dict {key -> count}, with sum(counts) == total.

    Implementation: simple categorical sampling `total` times.
    For this project scale, that's fine.
    """
    if total <= 0:
        return {k: 0 for k in weights.keys()}

    # Filter out zero-weight categories
    items: List[Tuple[Hashable, float]] = [(k, w) for k, w in weights.items() if w > 0]
    if not items:
        # edge case: all zero, just arbitrarily pick one key
        only_key = next(iter(weights.keys()))
        return {k: (total if k == only_key else 0) for k in weights.keys()}

    total_weight = sum(w for _, w in items)
    if total_weight <= 0:
        # same edge case guard
        only_key = items[0][0]
        return {k: (total if k == only_key else 0) for k in weights.keys()}

    # Normalize to probabilities
    keys = [k for k, _ in items]
    probs = [w / total_weight for _, w in items]

    counts = {k: 0 for k in weights.keys()}

    # Precompute cumulative probabilities
    cumulative: List[float] = []
    acc = 0.0
    for p in probs:
        acc += p
        cumulative.append(acc)

    for _ in range(total):
        r = rng.random()
        # Find first cumulative >= r
        for idx, c in enumerate(cumulative):
            if r <= c:
                chosen_key = keys[idx]
                counts[chosen_key] += 1
                break

    return counts
