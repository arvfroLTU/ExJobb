from golf_sim import Player, ShotEngine, simulate_hole

player = Player(name="Demo", handicap = 2)
strokes, trace = simulate_hole(440, player, ShotEngine())

print("Strokes:", strokes)
for i, (ball, shot) in enumerate(trace, 1):
    print(f"{i:02d}. {shot.club:18s} d={shot.distance_m:6.1f}m ang={shot.angle_rad:.3f} rad  -> y={ball.pos.y:6.2f}")
