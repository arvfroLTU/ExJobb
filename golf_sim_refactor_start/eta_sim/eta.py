from dataclasses import dataclass
from typing import Dict, List, Tuple
from .state import Snapshot, PlayerState
from .engine import ShotEngine, MovementParams
import math, random, json, pathlib, statistics

@dataclass
class ETAResult:
    mean_s: float
    p50_s: float
    p90_s: float
    samples: int

class ETAEstimator:
    def __init__(self,
                 movement: MovementParams | None = None,
                 shot_engine_factory=None,
                 results_dir: str | None = "./eta_runs"):
        self.move = movement or MovementParams()
        self.shot_engine_factory = shot_engine_factory or (lambda seed: ShotEngine(random.Random(seed)))
        self.results_dir = pathlib.Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.results_dir / "eta_samples.jsonl"

    def simulate_once(self, snap: Snapshot, seed: int) -> float:
        rng = random.Random(seed)
        engine = self.shot_engine_factory(seed)

        players = dict(snap.players)  
        st: Dict[str, PlayerState] = {k: PlayerState(**vars(v)) for k, v in snap.state.items()} #Players state on tee

        t = 0.0
        buffer_m = 3.0  # let others creep a little closer
        tracked = snap.tracked #name of player being tracked  by the simulation
        walked_m: Dict[str, float] = {name: 0.0 for name in st.keys()}
         
        def furthest_ball_name() -> str:
            return max(st.items(), key=lambda kv: kv[1].by)[0]

        def dist(ax, ay, bx, by) -> float:
            return math.hypot(ax-bx, ay-by)

        while any(P.by > 0.0 for P in st.values()):
            shooter_name = furthest_ball_name()
            S = st[shooter_name]

            # Walk-up time (shooter)
            d_to_ball = dist(S.fx, S.fy, S.bx, S.by)
            walk_up_time = max(0.0, d_to_ball - self.move.approach_threshold_m) / self.move.walk_speed_mps
            if walk_up_time > 0 and d_to_ball > 0:
                
                step_shooter = d_to_ball - self.move.approach_threshold_m
                walked_m[shooter_name] += step_shooter
                
                ratio = max(0.0, (d_to_ball - self.move.approach_threshold_m)) / d_to_ball   #Tracks how far to the ball we walk since we don't walk all the way up to it
                S.fx = S.fx + (S.bx - S.fx) * ratio
                S.fy = S.fy + (S.by - S.fy) * ratio

                # Others move toward their balls, limited by shooter's ball y
                
               
                floor_y = S.by + buffer_m
                
                
                for name, P in st.items():
                    if name == shooter_name: continue
                    max_forward = max(0.0, P.fy - floor_y)
                    can_walk = self.move.walk_speed_mps * walk_up_time
                    gap = dist(P.fx, P.fy, P.bx, P.by)
                    adv = min(can_walk, max_forward, gap)
                    
                    walked_m[name] += adv
                    
                    if adv > 0 and gap > 0:
                        r = adv / gap
                        P.fx = P.fx + (P.bx - P.fx) * r
                        P.fy = max(P.fy + (P.by - P.fy) * r, floor_y)

                t += walk_up_time                       # Time to walk up to the ball for the whole group given current shooter as tracked player

            # Address + swing
            addr = min(45.0, 8.0 + 0.9 * players[shooter_name].handicap)
            addr_swing = addr + self.move.swing_s
            t += addr_swing
            can_walk = self.move.walk_speed_mps * addr_swing   # ✅ not * t

            # Allow others to walk while shooter addresses/swings
            floor_y = S.by + buffer_m  # shooter’s current ball y
            for name, P in st.items():
                if name == shooter_name:
                    continue
                gap = math.hypot(P.fx - P.bx, P.fy - P.by)
                if gap <= 0:
                    continue
                can_walk = self.move.walk_speed_mps*t
                max_forward = max(0.0, P.fy - floor_y)
                adv = min(can_walk, max_forward, gap)
                walked_m[name] += adv
                if adv > 0:
                    r = adv / gap
                    P.fx = P.fx + (P.bx - P.fx) * r
                    P.fy = max(P.fy + (P.by - P.fy) * r, floor_y)
            
            # Shot resolution
            dist_shot, angle, club, failed, crit = engine.shot(players[shooter_name].handicap, S.by)
            S.shots_taken += 1
            S.bx, S.by = engine.advance_ball(S.bx, S.by, dist_shot, angle)                              #future implementation should take angle into account as well
            if S.by <= 0.1:
                S.by = 0.0   #anything within 1 dm counts as holed due to hole circumference       

                d_to_hole = math.hypot(S.fx - S.bx, S.fy - S.by)  # distance from feet to cup
                if d_to_hole > self.move.approach_threshold_m:
                    walk_time = (d_to_hole - self.move.approach_threshold_m) / self.move.walk_speed_mps
                    walked_m[shooter_name] += (d_to_hole - self.move.approach_threshold_m)

                    # move feet to within threshold of the cup
                    ratio3 = (d_to_hole - self.move.approach_threshold_m) / d_to_hole
                    S.fx = S.fx + (S.bx - S.fx) * ratio3
                    S.fy = S.fy + (S.by - S.fy) * ratio3
                    t += walk_time
            
            
            #shooter walks to their own ball after  having shot implementation
            # AFTER resolving the shot (S.bx, S.by updated), add:
            d_to_new_ball = math.hypot(S.fx - S.bx, S.fy - S.by)
            if d_to_new_ball > self.move.approach_threshold_m:
                walk_time = (d_to_new_ball - self.move.approach_threshold_m) / self.move.walk_speed_mps
    
                # shooter walks to (within threshold of) the new lie
                walked_m[shooter_name] += (d_to_new_ball - self.move.approach_threshold_m)
                ratio2 = (d_to_new_ball - self.move.approach_threshold_m) / d_to_new_ball
                S.fx = S.fx + (S.bx - S.fx) * ratio2
                S.fy = S.fy + (S.by - S.fy) * ratio2

                # others advance during this time but can't pass the shooter's new ball
                floor_y2 = S.by + buffer_m
                for name, P in st.items():
                    if name == shooter_name: 
                        continue
                    gap = math.hypot(P.fx - P.bx, P.fy - P.by)
                    if gap <= 0:
                        continue
                    can_walk2 = self.move.walk_speed_mps * walk_time
                    max_forward2 = max(0.0, P.fy - floor_y2)
                    adv2 = min(can_walk2, max_forward2, gap)
                    walked_m[name] += adv2
                    if adv2 > 0:
                        r2 = adv2 / gap
                        P.fx = P.fx + (P.bx - P.fx) * r2
                        P.fy = max(P.fy + (P.by - P.fy) * r2, floor_y2)

        t += walk_time

        

        print("[ETA simulate_once] walked meters:", {k: round(v, 1) for k, v in walked_m.items()})
        assert all(v >= 0 for v in walked_m.values())


        return t

    def estimate(self, snap: Snapshot, samples: int = 200, seed: int | None = None) -> ETAResult:
        base = random.Random(seed).randint(0, 10_000_000) if seed is not None else random.randint(0, 10_000_000)
        times = [self.simulate_once(snap, seed=base+i) for i in range(samples)]
        res = ETAResult(
            mean_s = statistics.fmean(times),
            p50_s  = statistics.median(times),
            p90_s  = sorted(times)[max(0, int(0.9*len(times))-1)],
            samples = samples
        )
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({
                "tsamples": times,
                "mean_s": res.mean_s,
                "p50_s":  res.p50_s,
                "p90_s":  res.p90_s,
                "hole": snap.hole_distance_m,
                "tracked": snap.tracked,
                "players": {k: vars(v) for k,v in snap.players.items()},
                "state": {k: vars(v) for k,v in snap.state.items()},
            }) + "\n")
        return res
