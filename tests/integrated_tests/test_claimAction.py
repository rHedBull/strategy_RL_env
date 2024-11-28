import json

import pytest

from map.map_settings import OWNER_DEFAULT_TILE
from rl_env.environment import MapEnvironment
from rl_env.objects.city import City
from rl_env.objects.Road import Bridge, Road


@pytest.fixture
def setup():
    # open settings file
    with open("test_env_settings.json", "r") as f:
        env_settings = json.load(f)
        env_settings["map_width"] = 100
        env_settings["map_height"] = 100

    agent_id = 0
    pos_x = 2
    pos_y = 2
    city = City(agent_id, (pos_x + 1, pos_y), 1)

    env = MapEnvironment(env_settings, 2, "rgb_array", seed=100)
    yield env, city, agent_id, pos_x, pos_y
    env.close()


def test_simple_claim(setup):
    env, city, agent_id, pos_x, pos_y = setup
    env.reset()

    road = Road((pos_x + 1, pos_y), 2)
    bridge = Bridge((pos_x + 1, pos_y), 2)

    claim_action = [0, pos_x, pos_y]
    tile1 = env.map.get_tile((pos_x, pos_y))
    tile2 = env.map.get_tile((pos_x + 1, pos_y))

    assert tile1.get_owner() == OWNER_DEFAULT_TILE

    # test build without visibility, should not work
    observation, reward, terminated, truncated, info = env.step([[claim_action]])
    assert tile1.get_owner() == OWNER_DEFAULT_TILE

    # set visible and adjacent tile claimed
    env.map.set_visible((pos_x, pos_y), agent_id)
    # set adjacent tile to be claimed by agent
    tile2.owner_id = agent_id

    # should work now
    observation, reward, terminated, truncated, info = env.step([[claim_action]])
    assert tile1.get_owner() == agent_id

    # if we already own the tile, nothing should change
    observation, reward, terminated, truncated, info = env.step([[claim_action]])
    assert tile1.get_owner() == agent_id

    tile1.owner_id = OWNER_DEFAULT_TILE  # set tile to be unclaimed
    tile2.add_building(road)  # add city to adjacent tile
    tile2.owner_id = OWNER_DEFAULT_TILE  # road is not owned by anyone
    # visible, unclaimed, but only next to a road, should not work
    observation, reward, terminated, truncated, info = env.step([[claim_action]])
    assert tile1.get_owner() == OWNER_DEFAULT_TILE

    tile2.buildings = set()
    tile2.building_int = 0
    tile2.add_building(bridge)  # add city to adjacent tile
    # visible, unclaimed, but only next to a bridge, should not work
    observation, reward, terminated, truncated, info = env.step([[claim_action]])
    assert tile1.get_owner() == OWNER_DEFAULT_TILE

    tile2.buildings = set()
    tile2.building_int = 0
    tile2.owner_id = agent_id
    tile2.add_building(city)  # add city to adjacent tile
    # visible, unclaimed and next to a city, should work
    observation, reward, terminated, truncated, info = env.step([[claim_action]])
    assert tile1.get_owner() == agent_id


def test_claiming_with_agent_conflicts(setup):
    env, city, agent_id, pos_x, pos_y = setup
    other_agent_id = 3
    claim_action = [0, pos_x, pos_y]
    tile1 = env.map.get_tile((pos_x, pos_y))
    tile2 = env.map.get_tile((pos_x + 1, pos_y))
    tile3 = env.map.get_tile((pos_x, pos_y + 1))

    # set visible
    env.map.set_visible((pos_x, pos_y), agent_id)

    tile2.owner_id = other_agent_id
    # adjacent tiles are claimed only by another agent, should not work
    observation, reward, terminated, truncated, info = env.step([[claim_action]])
    assert tile1.get_owner() == OWNER_DEFAULT_TILE

    # tile is already claimed by another agent, should not work
    tile1.owner_id = other_agent_id
    observation, reward, terminated, truncated, info = env.step([[claim_action]])
    assert tile1.get_owner() == other_agent_id

    tile1.owner_id = OWNER_DEFAULT_TILE
    tile3.owner_id = agent_id

    # tile is unclaimed and adjacent tiles are claimed by another agent and self, should work
    observation, reward, terminated, truncated, info = env.step([[claim_action]])
    assert tile1.get_owner() == agent_id