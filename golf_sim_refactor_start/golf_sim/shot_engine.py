from math import pi, sin, cos, sqrt
from .rng import RNG
from .types import ShotResult
from .clubs import CLUBS, select_club

class ShotEngine:
    """
    Single Responsibility: compute a shot from state-free inputs.
    Open/Closed: behavior can be extended by subclassing or swapping RNG.
    Liskov: callers rely only on ShotResult contract.
    Interface Segregation: small public surface.
    Dependency Inversion: randomness via RNG injection.
    """
    def __init__(self, rng: RNG | None = None):
        self.rng = rng or RNG()

    def failure_check(self, handicap: int) -> bool:
        # value > handicap -> success (False), else failure (True)
        return self.rng.randint(0, 100) <= handicap

    def critical_hit(self, handicap: int) -> bool:
        # Max ~2% (36hcp) .. ~6% (scratch) in original spirit
        check = self.rng.randint(0, 100)
        rate = min(((36 - handicap) / 6), 2)  # percentage points
        return check <= rate

    def shot_angle(self, handicap: int, failed: bool) -> float:
        min_theta, max_theta = -(pi/4), (pi/4)
        skill_bias = (1 - (handicap / 36))  # 0..1

        if failed:
            return self.rng.uniform(min_theta, max_theta)

        # worst players may be up to 45deg off; best tends to 0
        max_error = (pi/4) * (1 - skill_bias)
        return self.rng.uniform(-max_error, max_error)

    def shot_distance(self, handicap: int, d_hole: float) -> ShotResult:
        club_name = select_club(d_hole)
        failed = self.failure_check(handicap)
        critical = self.critical_hit(handicap)

        # Putter special-casing
        if club_name == "Putter":
            if failed:
                return ShotResult(0.0, 0.0, club_name, True, False)
            if critical:
                return ShotResult(d_hole, 0.0, club_name, False, True)
            return ShotResult((2 * d_hole) / 3.0, 0.0, club_name, False, False)

        club = CLUBS[club_name]
        theta = self.shot_angle(handicap, failed)

        # Skill moves outcome toward the top of the club's range
        # Use bounded percentile with gaussian noise ~ N(0, sigma), sigma = handicap/2
        sigma = max(0.1, handicap / 2.0)
        # emulate original -18..18-ish scaling using gauss and clamp to [-18, 18]
        g = max(-18.0, min(18.0, self.rng.gauss(0.0, sigma)))
        percent_along = (g - (-18.0)) / (36.0)  # 0..1
        skill_bias = (1 - (handicap / 36.0)) * 0.5  # 0..0.5
        biased = min(1.0, max(0.2, percent_along + skill_bias))

        base = club.min_m + biased * (club.max_m - club.min_m)
        if failed:
            base *= 0.5

        return ShotResult(base, theta, club_name, failed, critical)
