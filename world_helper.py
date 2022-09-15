from world import World


def next_id(world: World) -> int:
    return max([i.id for i in world.individuals]) + 1
