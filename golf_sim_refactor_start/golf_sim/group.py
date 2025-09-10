from dataclasses import dataclass
from typing import Dict, List, Tuple
from .types import Player, Ball, Position
from .shot_engine import ShotEngine
from .single_player import advance_ball
from .movement import MovementModel
from .policy import FurthestShootsPolicy

@dataclass
class PlayerState:
    player: Player
    ball: Ball
    feet: Position  # where the player is currently standing
    walked_m: float = 0.0
    

@dataclass
class GroupTraceItem:
    kind: str  # 'shot' or 'walk'
    player: str
    data: dict

class GroupSimulator:
    """
    Coordinates a group under the 'furthest shoots; others walk but cannot pass the furthest'
    policy. No globals. All deps injected (DIP). Small classes (ISP).
    """
    def __init__(self,
                 shot_engine: ShotEngine | None = None,
                 movement: MovementModel | None = None):
        self.engine = shot_engine or ShotEngine()
        self.movement = movement or MovementModel()
        self.policy = FurthestShootsPolicy()

    def all_holed(self, states: Dict[str, PlayerState]) -> bool:
        return all(s.ball.pos.y <= 0.0 for s in states.values())

    def simulate(self,
                 hole_distance_m: float,
                 players: List[Player],
                 dt_walk_s: float = 2.0) -> Tuple[int, List[GroupTraceItem]]:
        """
        Simulate until all balls are holed. At each turn:
          1) Pick shooter = ball furthest from hole
          2) Shooter takes a shot
          3) Everyone else walks toward their ball (duration dt_walk_s),
             but their walk is clamped so they can't be *closer to hole* than the shooter's
             resulting ball distance (no one 'passes' the furthest).
        Returns (turn_count, trace).
        """
        # Initialize state
        states: Dict[str, PlayerState] = {
            p.name: PlayerState(player=p,
                                ball=Ball(Position(0.0, hole_distance_m)),
                                feet=Position(0.0, hole_distance_m))
            for p in players
        }

        trace: List[GroupTraceItem] = []
        turns = 0

        while not self.all_holed(states):
            # Who shoots?
            shooter_name = self.policy.select_shooter({n: s.ball for n, s in states.items()})
            if shooter_name is None:
                break

            shooter = states[shooter_name]
            if shooter.ball.pos.y <= 0.0:
                # Already holed; mark temporary as not eligible and continue
                # Set its y to -1 so it won't be furthest
                shooter.ball.pos.y = -1.0
                continue

            # Shooter takes a shot
            shot = self.engine.shot_distance(shooter.player.handicap, shooter.ball.pos.y)
            shooter.ball = advance_ball(shooter.ball, shot)
            # Shooter's feet are at their ball after shooting
            shooter.feet = shooter.ball.pos
            trace.append(GroupTraceItem(kind='shot', player=shooter_name, data={
                'club': shot.club,
                'distance_m': shot.distance_m,
                'angle_rad': shot.angle_rad,
                'failed': shot.failed,
                'critical': shot.critical,
                'ball_y_after': shooter.ball.pos.y,
            }))
            turns += 1

            # If the shooter holed out, minimal floor_y is 0 for walkers
            floor_y = max(0.0, shooter.ball.pos.y)

            # Everyone else walks toward their ball, but cannot pass the shooter's y (floor_y)
            for name, st in states.items():
                if name == shooter_name:
                    continue
                target = st.ball.pos
                
                old_pos = st.feet
                st.feet = self.movement.step_toward(st.feet, target, dt_walk_s, floor_y=floor_y)
                # accumulate Euclidean distance walked
                dx = st.feet.x - old_pos.x
                dy = st.feet.y - old_pos.y
                st.walked_m += (dx*dx + dy*dy) ** 0.5

                trace.append(GroupTraceItem(kind='walk', player=name, data={
                    'feet_x': st.feet.x,
                    'feet_y': st.feet.y,
                    'target_ball_x': target.x,
                    'target_ball_y': target.y,
                    'floor_y': floor_y,
                }))

            # Gimmies: if any ball is within 1m, set to holed
            for st in states.values():
                if st.ball.pos.y <= 1.0:
                    st.ball.pos = Position(st.ball.pos.x, 0.0)

        return turns, trace
