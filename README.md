# World Simulation

This is a simple simulation of a world with individuals competing for assets.

The world is initialized with some assets spread around and some individuals packed in a few population clusters.

The individuals walk and collect assets according to their preferences.

At every moment, individuals positioned in the same point will reproduce, negotiate assets, or even kill each other.

It is possible to define some aspects of the world in the file `src/constants.py`.

## Usage

The following snippet gives an example of how to operate and interact with this world:

```python
w, h = 10, 10
world = World(
    size=(w, h), initial_assets=50, initial_individuals=20, initial_populations=3
)
print(world.indicators)
conflicts = world.get_conflicts()
while True:
    solutions = natural_solver(conflicts)
    world.solve_conflicts(solutions)
    print(world.indicators)
    if world.indicators["total_population"] == 0:
        break
    world.move_time()
    conflicts = world.get_conflicts()
```

The `natural_solver` is just a toy example of conflicts resolution, but the idea is to solve them using an AI.

The output of the snippet above will be something similar to:

```json
{"total_population": 20, "avg_happines": 0.0}
{"total_population": 24, "avg_happines": 0.05277777777777778}
{"total_population": 27, "avg_happines": 0.07407407407407408}
{"total_population": 23, "avg_happines": 0.1381642512077295}
...
{"total_population": 7, "avg_happines": 779.2159127671437}
{"total_population": 7, "avg_happines": 802.0195199301278}
{"total_population": 8, "avg_happines": 710.0357093007493}
...
{"total_population": 31, "avg_happines": 167.8370517960694}
{"total_population": 35, "avg_happines": 141.21890176688692}
{"total_population": 39, "avg_happines": 126.38987849316254}
...
{"total_population": 91, "avg_happines": 57.35887466977378}
{"total_population": 90, "avg_happines": 50.800611717024175}
{"total_population": 97, "avg_happines": 43.65775427241246}
...
{"total_population": 1, "avg_happines": 158.46654028492586}
{"total_population": 1, "avg_happines": 177.39008555081838}
{"total_population": 1, "avg_happines": 182.2202907304484}
...
{"total_population": 0, "avg_happines": 0}
```

## Development

The idea is to improve the world over time, this is just a pessimistic view of a worls with limited options.

Some characteristics probably seem controvertial, but it tries to capture some evil aspects of the world.

The first part of the code that requires urgent improvement is the one that represents assets and types of assets.