from math import sin, cos, sqrt
from .types import Player, Ball, Position, ShotResult
from .shot_engine import ShotEngine

def advance_ball(ball: Ball, shot: ShotResult) -> Ball:
    # Coordinate system: +y toward hole; +x is lateral
    dx = shot.distance_m * sin(shot.angle_rad)
    dy = shot.distance_m * cos(shot.angle_rad)
    return Ball(Position(ball.pos.x + dx, max(0.0, ball.pos.y - dy)))

def simulate_hole(hole_distance_m: float, player: Player, engine: ShotEngine | None = None):
    """
    Pure function w.r.t. inputs (except RNG inside engine).
    Returns (strokes, trace) where trace is a list of (ball, shot).
    """
    engine = engine or ShotEngine()
    ball = Ball(Position(0.0, hole_distance_m))
    trace: list[tuple[Ball, ShotResult]] = []
    strokes = 0

    while ball.pos.y > 0.0:
        shot = engine.shot_distance(player.handicap, ball.pos.y)
        ball = advance_ball(ball, shot)
        trace.append((ball, shot))
        strokes += 1
        if ball.pos.y <= 1.0:  # gimmie
            ball.pos.y = 0.0

    return strokes, trace
