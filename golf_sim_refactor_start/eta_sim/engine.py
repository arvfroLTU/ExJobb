from dataclasses import dataclass
from math import sin, cos, pi
import random

@dataclass(frozen=True)
class MovementParams:
    walk_speed_mps: float = 1.4  # Modulate as needed 
    pre_shot_address_s: float = 5.0
    swing_s: float = 2.0
    approach_threshold_m: float = 1.0

class ShotEngine:
    def __init__(self, rng: random.Random | None = None):
        self.rng = rng or random.Random()

    def failure_check(self, handicap: int) -> bool:
        p_fail = max(0.02, handicap / 100.0)
        return self.rng.random() < p_fail

    def critical_hit(self, handicap: int) -> bool:
        rate = min(((36 - handicap) / 6) / 100.0, 0.02)
        return self.rng.random() < rate

    def select_club(self, d_hole: float) -> str:
        s = d_hole
        if 0 <= s <= 14: return "Putter"
        if 14 < s <= 40: return "Soft Lob Wedge"
        if 40 < s <= 60: return "Soft Sand Wedge"
        if 60 < s <= 82: return "Soft Pitching Wedge"
        if 82 < s <= 119: return "Lob Wedge"
        if 119 < s <= 137: return "Sand Wedge"
        if 137 < s <= 146: return "Pitching Wedge"
        if 146 < s <= 155: return "9-Iron"
        if 155 < s <= 165: return "8-Iron"
        if 165 < s <= 174: return "7-Iron"
        if 174 < s <= 183: return "6-Iron"
        if 183 < s <= 192: return "5-Iron"
        if 192 < s <= 201: return "4-Iron"
        if 201 < s <= 210: return "3-Iron"
        if 210 < s <= 219: return "5-Wood"
        if 219 < s <= 229: return "3-Wood"
        return "Driver"

    def shot(self, handicap: int, d_hole: float):
        failed = self.failure_check(handicap)
        critical = self.critical_hit(handicap)
        club = self.select_club(d_hole)

        if club == "Putter":
            if failed: return (0.0, 0.0, club, True, False)
            if critical: return (d_hole, 0.0, club, False, True)
            return ((2*d_hole)/3.0, 0.0, club, False, False)

        sigma = max(0.1, handicap / 2.0)
        g = max(-18.0, min(18.0, self.rng.gauss(0.0, sigma)))
        percent = (g + 18.0) / 36.0
        bias = (1 - handicap/36.0) * 0.5
        p = min(1.0, max(0.2, percent + bias))

        ranges = {
            "Driver": (210, 280), "3-Wood": (192,229), "5-Wood": (183,219),
            "3-Iron": (165,201), "4-Iron": (155,192), "5-Iron": (146,183),
            "6-Iron": (137,174), "7-Iron": (128,165), "8-Iron": (119,155),
            "9-Iron": (110,146), "Pitching Wedge": (101,137),
            "Sand Wedge": (92,129), "Lob Wedge": (82,119),
            "Soft Pitching Wedge": (61,80), "Soft Sand Wedge": (28,60),
            "Soft Lob Wedge": (14,27), "Putter": (0, 14),
        }
        lo, hi = ranges[club]
        dist = lo + p*(hi-lo)
        if failed: dist *= 0.5

        if failed:
            angle = self.rng.uniform(-pi/4, pi/4)
        else:
            skill_bias = (1 - handicap/36.0)
            max_error = (pi/4) * (1 - skill_bias)
            angle = self.rng.uniform(-max_error, max_error)

        return (dist, angle, club, failed, critical)

    def advance_ball(self, bx: float, by: float, dist: float, angle: float):
        dx = dist * sin(angle)
        dy = dist * cos(angle)
        nx = bx + dx
        ny = max(0.0, by - dy)
        return nx, ny
