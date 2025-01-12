import pytest

from strategyRLEnv.map.map_settings import (COLOR_DEFAULT_BORDER,
                                            OWNER_DEFAULT_TILE, BuildingType,
                                            LandType, land_type_color)
from strategyRLEnv.map.MapPosition import MapPosition
from strategyRLEnv.map.MapSquare import Map_Square
from strategyRLEnv.objects.City import City
from strategyRLEnv.objects.Farm import Farm
from strategyRLEnv.objects.Mine import Mine
from strategyRLEnv.objects.Road import Bridge, Road
from tests.env_tests.test_action_manager import MockAgent


@pytest.fixture
def map_square():
    """
    Fixture to create a Map_Square instance before each test.
    """
    mock_city_params = {
        "building_type_id": 1,
        "money_gain_per_turn": 110,
        "maintenance_cost_per_turn": 10,
    }
    map_square = Map_Square(1, MapPosition(5, 10), land_value=LandType.LAND)
    yield mock_city_params, map_square


def test_initialization(map_square):
    """
    Test that Map_Square initializes correctly with given parameters.
    """
    mock_city_params, map_square = map_square
    assert map_square.tile_id == 1
    assert map_square.position.x == 5
    assert map_square.position.y == 10
    assert map_square.land_type == LandType.LAND
    assert map_square.resources == []
    assert map_square.owner_id == OWNER_DEFAULT_TILE
    assert map_square.visibility_bitmask == 0
    assert map_square._land_money_value == 1
    assert map_square.default_border_color == COLOR_DEFAULT_BORDER
    assert map_square.default_color == land_type_color(LandType.LAND)
    assert map_square.land_type_color == land_type_color(LandType.LAND)
    assert map_square.owner_color == COLOR_DEFAULT_BORDER


def test_reset(map_square):
    """
    Test that the reset method restores the initial state.
    """
    mock_city_params, map_square = map_square

    mock_agent_id = 7
    city = City(mock_agent_id, map_square.position, mock_city_params)

    # Modify some attributes
    map_square.owner_id = 2
    map_square.visibility_bitmask = 255
    map_square.land_type = LandType.MOUNTAIN
    map_square.land_type_color = land_type_color(LandType.MOUNTAIN)
    map_square._land_money_value = 5
    map_square.add_building(city)
    map_square.building_int = 1

    # Call reset
    map_square.reset()

    # Assertions
    assert map_square.owner_id == OWNER_DEFAULT_TILE
    assert map_square.visibility_bitmask == 0
    assert map_square.owner_color == COLOR_DEFAULT_BORDER
    assert map_square._land_money_value == 1


def test_set_and_get_owner(map_square):
    """
    Test setting and getting the owner of the map square.
    """
    mock_city_params, map_square = map_square
    agent_id = 42
    agent_color = (128, 0, 128)  # Purple
    mockAgent = MockAgent(agent_id, agent_color)
    assert map_square.get_owner() == OWNER_DEFAULT_TILE

    # Set owner
    map_square.set_owner(mockAgent)

    # Assertions
    assert map_square.get_owner() == mockAgent.id
    assert map_square.owner_color == agent_color


def test_set_and_get_land_type(map_square):
    """
    Test setting and getting the land type of the map square.
    """

    mock_city_params, map_square = map_square

    new_land_type = LandType.MOUNTAIN
    map_square.set_land_type(new_land_type)
    assert map_square.get_land_type() == new_land_type
    assert map_square.land_type_color == land_type_color(new_land_type)

    # Setting the same land type should not change anything
    map_square.set_land_type(new_land_type)
    assert map_square.get_land_type() == new_land_type
    assert map_square.land_type_color == land_type_color(new_land_type)


# def test_claim(map_square):
#     """
#     Test claiming the map square by an agent.
#     """
#
#     mock_city_params, map_square = map_square
#     agent = Mock()
#     agent.id = 7
#     agent.color = (0, 255, 0)  # Green
#
#     assert map_square.owner_id == OWNER_DEFAULT_TILE
#     assert map_square.owner_color == COLOR_DEFAULT_BORDER
#
#     map_square.claim(agent)
#
#     assert map_square.owner_id == agent.id
#     assert map_square.owner_color == agent.color


def test_add_building(map_square):
    """
    Test adding a building to the map square.
    """
    mock_city_params, map_square = map_square

    mock_agent_id = 7
    city = City(mock_agent_id, map_square.position, mock_city_params)

    assert not map_square.has_any_building()

    map_square.add_building(city)

    assert map_square.has_building(BuildingType.CITY)


def test_has_building(map_square):
    """
    Test checking for specific building types.
    """
    mock_city_params, map_square = map_square

    mock_agent_id = 7
    city = City(mock_agent_id, map_square.position, mock_city_params)
    road = Road(map_square.position, {})

    assert map_square.has_building(BuildingType.CITY) is False
    assert map_square.has_building(BuildingType.ROAD) is False
    assert map_square.has_building(BuildingType.MINE) is False

    map_square.add_building(city)
    assert map_square.has_building(BuildingType.CITY) is True
    assert map_square.has_building(BuildingType.ROAD) is False
    map_square.remove_building(BuildingType.CITY)

    map_square.add_building(road)
    assert map_square.has_building(BuildingType.ROAD) is True
    assert map_square.has_building(BuildingType.CITY) is False
    map_square.remove_building(BuildingType.ROAD)

    mine = Mine(1, map_square, {"building_type_id": 5})
    map_square.add_building(mine)
    assert map_square.has_building(BuildingType.MINE) is True
    assert map_square.has_building(BuildingType.CITY) is False
    # Test undefined building type
    assert map_square.has_building("UNKNOWN_BUILDING") is False


def test_has_any_building(map_square):
    """
    Test checking if any building exists on the map square.
    """

    mock_city_params, map_square = map_square

    assert map_square.has_any_building() is False

    mock_agent_id = 7
    city = City(mock_agent_id, map_square.position, mock_city_params)

    map_square.add_building(city)
    assert map_square.has_any_building() is True


def test_remove_building(map_square):
    """
    Test removing a building from the map square.
    """
    mock_city_params, map_square = map_square
    mock_agent_id = 7

    mock_road_params = {"building_type_id": 2}
    city = City(mock_agent_id, map_square.position, mock_city_params)
    road = Road(map_square.position, mock_road_params)

    map_square.add_building(city)
    assert map_square.has_building(BuildingType.CITY)

    # Remove city
    map_square.remove_building(BuildingType.CITY)
    assert map_square.has_building(BuildingType.CITY) is False

    # Add road
    map_square.add_building(road)
    assert map_square.has_building(BuildingType.ROAD)

    # Remove road
    map_square.remove_building(BuildingType.ROAD)
    assert map_square.has_building(BuildingType.ROAD) is False

    # Attempting to remove a non-existent building should do nothing
    map_square.remove_building(BuildingType.CITY)  # Already removed
    assert map_square.has_building(BuildingType.ROAD) is False


def test_get_full_info(map_square):
    """
    Test retrieving the full info of the map square.
    """
    mock_city_params, map_square = map_square

    mock_owner_agent = 7
    mockAgent = MockAgent(mock_owner_agent)
    map_square.set_land_type(LandType.MOUNTAIN)
    map_square.set_owner(mockAgent)  # Red
    building = City(mock_owner_agent, MapPosition(0, 0), mock_city_params)
    map_square.add_building(building)

    expected_state = [
        LandType.MOUNTAIN.value,
        mockAgent.id,
        0,
    ]

    state = map_square.get_full_info()
    assert state == expected_state


def test_has_road_and_bridge(map_square):
    """
    Test checking for the presence of roads and bridges.
    """
    mock_city_params, map_square = map_square

    road = Road(map_square.position, {})
    bridge = Bridge(map_square.position, {})
    farm = Farm(0, map_square.position, {})

    assert map_square.has_road() is False
    assert map_square.has_bridge() is False

    map_square.add_building(road)
    assert map_square.has_road() is True
    assert map_square.has_bridge() is False
    # Remove road
    map_square.remove_building(BuildingType.ROAD)

    map_square.add_building(bridge)
    assert map_square.has_bridge() is True
    assert map_square.has_road() is False
    # Remove bridge
    map_square.remove_building(BuildingType.BRIDGE)

    # test if farm is not a road or bridge
    map_square.add_building(farm)
    assert map_square.has_road() is False
    assert map_square.has_bridge() is False
