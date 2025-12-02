import random
from typing import Dict, Hashable, List, Tuple

# This is our random number generator class! It will help us produce random numbers for our city generator
class RNG:
    def __init__(self, seed: int):
        self.seed = seed
        self._rng = random.Random(seed)

    def random(self) -> float:
        return self._rng.random()

    def randint(self, a: int, b: int) -> int:
        return self._rng.randint(a, b)

# This function, simply put, collects a total number of items and distributes them across different categories based on our weights
def allocate_discrete(total: int, weights: Dict[Hashable, float], rng: RNG) -> Dict[Hashable, int]:
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

    # This builds, simply put, two lists; one for the keys and one for the probabilities
    keys = [k for k, _ in items]
    probs = [w / total_weight for _, w in items]

    counts = {k: 0 for k in weights.keys()}

    # This builds, simply, a cumulative probability list. That is that, for each index, it contains the sum of all previous probabilities up to that index
    # We do this so that we can easily sample from the distribution (we do this by generating a random number and seeing where it falls in the distribution)
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
