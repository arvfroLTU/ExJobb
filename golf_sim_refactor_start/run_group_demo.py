from golf_sim import Player, ShotEngine
from golf_sim.group import GroupSimulator

players = [
    Player(name="Ava", handicap=24),
    Player(name="Bo", handicap=18),
    Player(name="Cid", handicap=12),
]

sim = GroupSimulator(shot_engine=ShotEngine())
turns, trace = sim.simulate(hole_distance_m=440, players=players, dt_walk_s=3.0)

print("Turns:", turns)
for i, item in enumerate(trace, 1):
    if item.kind == 'shot':
        print(f"{i:03d} [{item.kind}] {item.player}: {item.data['club']} d={item.data['distance_m']:.1f}m -> ball_y={item.data['ball_y_after']:.1f}")
    else:
        print(f"{i:03d} [{item.kind}] {item.player}: feet_y={item.data['feet_y']:.1f} (floor={item.data['floor_y']:.1f}, target={item.data['target_ball_y']:.1f})")
