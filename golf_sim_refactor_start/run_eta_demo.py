from eta_sim import Player, PlayerState, Snapshot, ETAEstimator

players = {
    "Ava": Player("Ava", 24),
    "Bo":  Player("Bo", 18),
    "Cid": Player("Cid", 12),
}
state = {
    "Ava": PlayerState(fx=0.0,  fy=440.0, bx=0.0, by=440.0, shots_taken=0),
    "Bo":  PlayerState(fx=0.0,  fy=440.0, bx=0.0, by=440.0, shots_taken=0),
    "Cid": PlayerState(fx=0.0,  fy=440.0, bx=0.0, by=440.0, shots_taken=0),
}
snap = Snapshot(hole_distance_m=440.0, players=players, state=state, tracked="Ava")

eta = ETAEstimator()
res = eta.estimate(snap, samples=200, seed=42)
print(f"ETA mean: {res.mean_s:.1f}s  p50: {res.p50_s:.1f}s  p90: {res.p90_s:.1f}s  (n={res.samples})")
print("Appended to ./eta_runs/eta_samples.jsonl")
