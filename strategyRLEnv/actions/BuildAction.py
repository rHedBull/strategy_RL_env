from abc import ABC, abstractmethod
from typing import Dict

from strategyRLEnv.actions.Action import Action, ActionType
from strategyRLEnv.map.map_settings import (ALLOWED_BUILDING_PLACEMENTS,
                                            BuildingType)
from strategyRLEnv.map.MapPosition import MapPosition


class BuildAction(Action, ABC):
    def __init__(self, agent, position: MapPosition, building_type: BuildingType):
        super().__init__(agent, position, ActionType.BUILD)
        self.building_type = building_type

    def validate(self, env) -> bool:
        if not super().validate(env):
            return False

        if not fit_building_to_land_type(env, self.position, self.building_type):
            return False

        if not env.map.is_visible(self.position, self.agent.id):
            return False

        if env.map.get_tile(self.position).has_any_building():
            return False

        return True

    def execute(self, env) -> float:
        self.perform_build(env)
        env.map.get_tile(self.position).update(env)
        env.map.trigger_surrounding_tile_update(self.position)
        self.agent.money -= self.get_cost(env)
        reward = self.get_reward(env)
        return reward

    @abstractmethod
    def perform_build(self, env):
        """Execute the build on the map."""
        pass

    def get_cost(self, env) -> float:
        """Return the cost of the action."""
        return env.env_settings.get("actions")[self.building_type.value]["cost"]

    def get_reward(self, env) -> float:
        """Return the reward for the action."""
        return env.env_settings.get("actions")[self.building_type.value]["reward"]

    def get_building_parameters(self, env) -> Dict:
        """Return the building type id."""
        action = env.env_settings.get("actions")[self.building_type.value]
        params = {
            "money_gain_per_turn": action.get("money_gain_per_turn", 0),
            "maintenance_cost_per_turn": action.get("maintenance_cost_per_turn", 0),
        }
        return params


def fit_building_to_land_type(
    env, position: MapPosition, build_type: BuildingType
) -> bool:
    """Check if the land type at the given position is suitable for the building type."""

    land_type_at_position = env.map.get_tile(position).get_land_type()
    if land_type_at_position not in ALLOWED_BUILDING_PLACEMENTS[build_type]:
        return False
    return True
