import sys

sys.path.insert(0, "./src")

from world_helper import Point, natural_solver
from world import World


if __name__ == "__main__":
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
