# Injected randomness -> easy to test/mock
class RNG:
    def __init__(self, seed: int | None = None):
        self._rand = __import__("random").Random(seed)

    def randint(self, a: int, b: int) -> int:
        return self._rand.randint(a, b)

    def uniform(self, a: float, b: float) -> float:
        return self._rand.uniform(a, b)

    def gauss(self, mu: float, sigma: float) -> float:
        return self._rand.gauss(mu, sigma)
