from golf_sim import Player, ShotEngine
from golf_sim.group import GroupSimulator
from collections import defaultdict
import math

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

totals = {}
totals_shots = {}


totals_walked = defaultdict(float)
last_pos = {}

for item in trace:
    if item.kind == "walk":
        name = item.player
        x, y = item.data["feet_x"], item.data["feet_y"]
        if name in last_pos:
            dx = x - last_pos[name][0]
            dy = y - last_pos[name][1]
            totals_walked[name] += math.hypot(dx, dy)
        last_pos[name] = (x, y)





for item in trace:
    if item.kind == "walk":
        # sum the step taken in this walk event
        step = abs(item.data["target_ball_y"] - item.data["feet_y"])
        totals_walked[item.player] = totals_walked.get(item.player, 0.0) + step
    elif item.kind == "shot":
        # sum the raw shot length
        shot_len = item.data["distance_m"]
        totals_shots[item.player] = totals_shots.get(item.player, 0.0) + shot_len

print("Total walked:", totals_walked)
print("Total shot distance:", totals_shots)
print("Total distance:", {p: totals_walked.get(p, 0.0) + totals_shots.get(p, 0.0)
                          for p in totals_walked.keys() | totals_shots.keys()})