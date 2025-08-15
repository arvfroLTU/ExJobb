from dataclasses import dataclass
from .types import Position, Ball

@dataclass(frozen=True)
class MovementParams:
    walk_speed_mps: float = 1.4  # ~5 km/h

class MovementModel:
    """Small, testable movement calculator (SRP)."""
    def __init__(self, params: MovementParams | None = None):
        self.params = params or MovementParams()

    def step_toward(self, current: Position, target: Position, dt: float, floor_y: float | None = None) -> Position:
        """Move straight-line toward target by walk_speed*dt, optionally
        clamping the resulting y so we don't go *closer to hole* than floor_y.
        Coordinate system: +y away from hole, 0 at the hole.
        Players 'approach' means reducing y.
        """
        if dt <= 0:
            return current

        speed = self.params.walk_speed_mps
        # distance toward target
        dx = target.x - current.x
        dy = target.y - current.y
        dist = (dx*dx + dy*dy) ** 0.5
        if dist == 0:
            new_x, new_y = current.x, current.y
        else:
            step = min(dist, speed * dt)
            new_x = current.x + (dx / dist) * step
            new_y = current.y + (dy / dist) * step

        if floor_y is not None:
            # Can't go *below* floor_y (closer to hole). hole is y=0, so "below" means < floor_y
            new_y = max(new_y, floor_y)
        return Position(new_x, new_y)
