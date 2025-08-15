from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Club:
    name: str
    min_m: float
    max_m: float

@dataclass
class ShotResult:
    distance_m: float
    angle_rad: float
    club: str
    failed: bool
    critical: bool

@dataclass
class Position:
    x: float
    y: float

@dataclass
class Ball:
    pos: Position

@dataclass
class Player:
    name: str
    handicap: int  # 0..36
