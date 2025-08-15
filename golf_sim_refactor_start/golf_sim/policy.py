from typing import Iterable
from .types import Ball

class FurthestShootsPolicy:
    """Turn policy: the player whose BALL is furthest from the hole shoots."""
    def select_shooter(self, balls: dict[str, Ball]) -> str | None:
        if not balls:
            return None
        # y is distance to hole; larger y => further from hole
        return max(balls.items(), key=lambda kv: kv[1].pos.y)[0]
