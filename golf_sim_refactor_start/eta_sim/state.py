from dataclasses import dataclass
from typing import Dict

@dataclass
class Player:
    name: str
    handicap: int

@dataclass
class PlayerState:
    # Feet (where the golfer stands)
    fx: float
    fy: float
    # Ball
    bx: float
    by: float
    shots_taken: int = 0

@dataclass
class Snapshot:
    hole_distance_m: float
    players: Dict[str, Player]
    state: Dict[str, PlayerState]
    # name of the "tracked" user whose ETA we want
    tracked: str
