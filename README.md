# World Simulation

This is a simple simulation of a world with individuals competing for assets.

The world is initialized with some assets spread around and some individuals clustered in a few population clusters.

The individuals walk and collect assets according to their preferences.

At every moment, individuals positioned in the same point will reproduce, negotiate assets, or even kill each other.

It is possible to define some aspects of the world in the file `src/constants.py`.

## Usage

The following snippet gives an example of how to operate and interact with this world:

```python
from world_helper import Point, natural_solver
from world import World

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
{"total_population": 20, "avg_happines": 0.0, "avg_age": 0.0}
{"total_population": 23, "avg_happines": 0.09999999999999999, "avg_age": 0.0}
{"total_population": 20, "avg_happines": 0.32, "avg_age": 1.0}
...
{"total_population": 47, "avg_happines": 53.65175638257239, "avg_age": 13.914893617021276}
{"total_population": 51, "avg_happines": 48.41396193030974, "avg_age": 12.882352941176471}
{"total_population": 54, "avg_happines": 45.14741602842799, "avg_age": 12.5}
...
{"total_population": 133, "avg_happines": 7.071315986722207, "avg_age": 5.962406015037594}
{"total_population": 121, "avg_happines": 7.161083955959382, "avg_age": 6.363636363636363}
{"total_population": 119, "avg_happines": 6.576438651600998, "avg_age": 5.80672268907563}
...
{"total_population": 26, "avg_happines": 14.197678412774604, "avg_age": 8.692307692307692}
{"total_population": 24, "avg_happines": 15.1986265509115, "avg_age": 9.083333333333334}
{"total_population": 24, "avg_happines": 15.870354204153466, "avg_age": 9.083333333333334}
...
{"total_population": 81, "avg_happines": 18.247895064917483, "avg_age": 10.037037037037036}
{"total_population": 86, "avg_happines": 16.63649735222988, "avg_age": 9.0}
{"total_population": 90, "avg_happines": 13.751155200171326, "avg_age": 7.955555555555556}
...
{"total_population": 5, "avg_happines": 94.5743881361025, "avg_age": 26.0}
{"total_population": 5, "avg_happines": 98.0896854092503, "avg_age": 27.0}
{"total_population": 6, "avg_happines": 87.5900041544712, "avg_age": 23.333333333333332}
...
{"total_population": 100, "avg_happines": 11.239575909290325, "avg_age": 8.18}
{"total_population": 92, "avg_happines": 10.609720303753932, "avg_age": 8.054347826086957}
{"total_population": 100, "avg_happines": 9.279801999603398, "avg_age": 7.74}
...
{"total_population": 1, "avg_happines": 452.94695879246785, "avg_age": 89.0}
{"total_population": 1, "avg_happines": 452.94695879246785, "avg_age": 90.0}
{"total_population": 0, "avg_happines": 0, "avg_age": 0.0}
```

## Development

The idea is to improve the world over time. This is just a pessimistic view of a world with limited options.

Some characteristics probably seem controvertial, but it tries to capture some evil aspects of the world.

The application is built almost entirely using the standard library. The next step is to vectorize most of the operations.