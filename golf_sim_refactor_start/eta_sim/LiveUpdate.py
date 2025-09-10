from dataclasses import replace
from typing import Dict, Optional
from eta_sim import Player, PlayerState, Snapshot, ETAEstimator, ShotEngine
import math, random

def apply_tracked_update(
    snap: Snapshot,
    *,
    fx: Optional[float] = None,
    fy: Optional[float] = None,
    bx: Optional[float] = None,
    by: Optional[float] = None,
    shots_taken: Optional[int] = None,
) -> Snapshot:
    """Return a NEW Snapshot with tracked player's fields updated."""
    
    # Name of the currently tracked player in this snapshot
    name = snap.tracked
    
    # Get the current PlayerState of the tracked player
    current = snap.state[name]
    
    # Build a NEW PlayerState with updated fields.
    # If an argument wasn’t provided (is None), keep the old value from `current`.
    new_ps = PlayerState(
        fx = current.fx if fx is None else fx,
        fy = current.fy if fy is None else fy,
        bx = current.bx if bx is None else bx,
        by = current.by if by is None else by,
        shots_taken = current.shots_taken if shots_taken is None else shots_taken,
    )
    
     # Copy the entire state dictionary so we don’t mutate the original.
    new_state = dict(snap.state)
    
    # Replace only the tracked player’s entry
    new_state[name] = new_ps
    
    # Return a brand new Snapshot object with:
    # - same hole length
    # - same players
    # - updated state dict (only tracked player differs)
    # - same tracked player designation
    
    return Snapshot(hole_distance_m=snap.hole_distance_m, players=snap.players, state=new_state, tracked=snap.tracked)




def _advance_once_expected(handicap: int, bx: float, by: float, engine: ShotEngine) -> tuple[float,float]:
    """One deterministic ‘expected’ advance using the engine’s club choice and mid-range distance (angle=0)."""
    club = engine.select_club(by)
    # approximate expected carry: midpoint of club range, reduced a bit for handicap
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
    # bias midpoint by skill (hcp 0 → 100% midpoint, hcp 36 → ~80% midpoint)
    bias = max(0.8, 1.0 - (handicap/36.0)*0.2)
    dist = (lo + hi) / 2.0 * bias

    # for putts, aim to reduce remaining by ~2/3 (same idea as your engine)
    if club == "Putter":
        dist = (2*by)/3.0

    ny = max(0.0, by - dist)
    nx = bx  # ignore sideways here; this is just to seed a plausible state
    return nx, ny


# We make an assumption here that is generally untrue which is that each player will stand at their respective ball whenever the tracked player shoots. 
#May alter later

def presuppose_nth_shot_for_others(
    snap: Snapshot,                     #old player state
    *,
    n_by_player: Dict[str, int],        #amount of shots one player should be advanced by, will affect position
    place_feet_at_ball: bool = True,
    rng_seed: Optional[int] = None,     #makes shots reproducible
) -> Snapshot:
    """
    For each non-tracked player in n_by_player, advance their BALL n shots forward
    using a simple expected-distance model and increment shots_taken by n.
    If place_feet_at_ball=True, set feet at the resulting ball (ready to hit).
    """
    engine = ShotEngine(random.Random(rng_seed))
    new_state = dict(snap.state)
    for name, n in n_by_player.items():
        if name == snap.tracked:
            continue
        ps = new_state[name]
        bx, by = ps.bx, ps.by
        shots = ps.shots_taken
        for _ in range(max(0, n)):
            bx, by = _advance_once_expected(snap.players[name].handicap, bx, by, engine)
        if place_feet_at_ball:
            fx, fy = bx, by
        else:
            fx, fy = ps.fx, ps.fy
        new_state[name] = PlayerState(fx=fx, fy=fy, bx=bx, by=by, shots_taken=shots + max(0, n))
    return Snapshot(hole_distance_m=snap.hole_distance_m, players=snap.players, state=new_state, tracked=snap.tracked)
