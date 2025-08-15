# Refactor Plan (SOLID+Booch)

This sliced refactor removes module-level globals and introduces clear,
testable boundaries.

## What changed

- **Dependency Inversion**: randomness is injected via `RNG`, so your
  simulations are deterministic in tests.
- **Single Responsibility**: `ShotEngine` computes one shot from inputs.
- **Open/Closed**: extend behavior by subclassing engines or swapping RNGs.
- **Liskov/Interface Segregation**: callers only depend on small, stable
  dataclasses and methods.

## Primitiveness, Cohesion & Coupling

- Replaced mutable global state (`strokeCount`, `holeDistance`) with explicit
  inputs/outputs.
- Pure helpers: `select_club`, `advance_ball`.
- Data is carried in tiny, immutable (or narrowly mutable) dataclasses.

## How to use (single-player)

```python
from golf_sim import Player, ShotEngine, simulate_hole

strokes, trace = simulate_hole(
    hole_distance_m=440,
    player=Player(name="You", handicap=18),
    engine=ShotEngine(),   # RNG can take a seed for tests
)
print(strokes, "strokes")
```

## Next steps to migrate your current code

1. **Replace** calls to `ShotSim.NextShotSetup`/`simulatePlayerHole` with
   `ShotEngine().shot_distance()` and `simulate_hole` respectively.
2. **Remove** global dicts from `Group_session.py`. Encapsulate them in a
   `GroupSimulator` class that you construct with initial positions and pass
   into functions (DI).
3. **EventHub**: replace the ad-hoc global flags in `SimCoordFeeder` with
   `EventBus`. Publish `player/coord_update` with the tracked player's lat/lon.
4. **Config**: keep DB credentials and constants in a config provider, never
   in module globals. Read once at composition root.
5. **Testing**: seed `RNG(seed)` to make the sim deterministic.

## Booch metrics mapping

- **Coupling**: `golf_sim` modules are acyclic. No module imports the app layer.
- **Cohesion**: each module has a single purpose (clubs data, types, RNG,
  shot computation, 1P simulation, events).
