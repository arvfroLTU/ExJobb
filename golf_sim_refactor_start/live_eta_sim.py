from eta_sim import Player, PlayerState, Snapshot, ETAEstimator, LiveUpdate
players = {
    "Ava": Player("Ava", 24),
    "Bo":  Player("Bo", 18),
    "Cid": Player("Cid", 12),
}
#TODO  get fed hole length from current track

state = {
    "Ava": PlayerState(fx=0.0,  fy=440.0, bx=0.0, by=440.0, shots_taken=0),
    "Bo":  PlayerState(fx=0.0,  fy=440.0, bx=0.0, by=440.0, shots_taken=0),
    "Cid": PlayerState(fx=0.0,  fy=440.0, bx=0.0, by=440.0, shots_taken=0),
}

snap = Snapshot(hole_distance_m=440.0, players=players, state=state, tracked="Ava")
eta = ETAEstimator()


while True:
    print("\nCommands: track NAME | set fx fy bx by shots | presume Bo=1 Cid=2 | show | run [samples] | quit")
    # --- Read input line ---
    try:
        line = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        break  # graceful exit on Ctrl+D or Ctrl+C
    
    if not line:
        continue  # ignore empty lines

    # --- Quit command ---
    if line == "quit":
        break

    # --- Switch tracked player ---
    if line.startswith("track "):
        who = line.split()[1]
        if who not in players:
            print("unknown player")
            continue
        # Create a new Snapshot with the same state but new tracked player
        snap = Snapshot(
            hole_distance_m=snap.hole_distance_m,
            players=snap.players,
            state=snap.state,
            tracked=who,
        )
        print("tracked =", who)
        continue

    # --- Update tracked player’s state manually ---
    if line.startswith("set "):
        parts = line.split()
        if len(parts) != 6:
            print("usage: set fx fy bx by shots")
            continue

        # Parse numbers from command line
        fx = float(parts[1])
        fy = float(parts[2])
        bx = float(parts[3])
        by = float(parts[4])
        shots = int(parts[5])

        # Apply update only to the tracked player
        snap = LiveUpdate.apply_tracked_update(snap, fx=fx, fy=fy, bx=bx, by=by, shots_taken=shots)
        print("updated tracked player:", snap.tracked, snap.state[snap.tracked])
        continue

    # --- Presume shots for other players ---
    if line.startswith("presume"):
        # Example input: "presume Bo=1 Cid=2"
        tokens = line.split()[1:]
        nmap = {}
        ok = True
        for tok in tokens:
            if "=" not in tok:
                ok = False
                break
            name, n = tok.split("=", 1)
            if name not in players:
                ok = False
                break
            nmap[name] = int(n)

        if not ok:
            print("usage: presume Bo=1 Cid=2")
            continue

        snap = LiveUpdate.presuppose_nth_shot_for_others(snap, n_by_player=nmap, place_feet_at_ball=True)
        print("presupposed:", nmap)
        continue

    # --- Show current snapshot ---
    if line.startswith("show"):
        print("tracked:", snap.tracked)
        for name, ps in snap.state.items():
            print(f"{name:>3} | feet=({ps.fx:.1f},{ps.fy:.1f}) ball=({ps.bx:.1f},{ps.by:.1f}) shots={ps.shots_taken}")
        continue

    # --- Run ETA simulation ---
    if line.startswith("run"):
        parts = line.split()
        samples = 200 if len(parts) == 1 else int(parts[1])
        res = eta.estimate(snap, samples=samples)
        print(f"ETA mean: {res.mean_s:.1f}s  p50: {res.p50_s:.1f}s  p90: {res.p90_s:.1f}s  (n={res.samples})")
        print("Appended to ./eta_runs/eta_samples.jsonl")
        continue

    # --- Unknown command ---
    print("unknown command")