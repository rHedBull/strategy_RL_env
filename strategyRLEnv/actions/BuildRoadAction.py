from strategyRLEnv.actions.BuildAction import BuildAction
from strategyRLEnv.map import MapPosition
from strategyRLEnv.objects.Building import BuildingType
from strategyRLEnv.objects.Road import Bridge, Road, update_road_bridge_shape
from strategyRLEnv.Agent import Agent


class BuildRoadAction(BuildAction):
    def __init__(self, agent: Agent, position: MapPosition):
        super().__init__(agent, position, BuildingType.ROAD)

    def validate(self, env) -> bool:
        if not super().validate(env):
            return False

        if self.agent.id == env.map.get_tile(self.position).get_owner():
            # tile is onwed by agent
            return True

        if env.map.tile_is_next_to_building(self.position):
            return True

        return False

    def perform_build(self, env):
        building_type_id = self.get_building_parameters(env)
        road = Road(self.position, building_type_id)
        env.map.add_building(road, self.position)

        update_road_bridge_shape(road, env.map)

        self.agent.update_local_visibility(self.position)


class BuildBridgeAction(BuildAction):
    def __init__(self, agent: Agent, position: MapPosition):
        super().__init__(agent, position, BuildingType.BRIDGE)

    def validate(self, env) -> bool:
        if not super().validate(env):
            return False

        if self.agent.id == env.map.get_tile(self.position).get_owner():
            # tile is onwed by agent
            return True

        if env.map.tile_is_next_to_building(self.position):
            return True

        return False

    def perform_build(self, env):
        building_type_id = self.get_building_parameters(env)
        bridge = Bridge(self.position, building_type_id)
        env.map.add_building(bridge, self.position)

        update_road_bridge_shape(bridge, env.map)
        self.agent.update_local_visibility(self.position)
