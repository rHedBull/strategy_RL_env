from typing import Any, Dict, Tuple

import numpy as np
import pygame

from map.map_settings import AGENT_COLORS, PLAYER_COLOR
from test_env.Agent import Agent


class Player(Agent):
    def __init__(self):
        super().__init__(0)

        self.color = PLAYER_COLOR

        # TODO: check if sth else needed for player class


class Agent:
    """
    Represents an agent in the environment.

    Attributes:
        id (int): Unique identifier for the agent.
        position (Tuple[int, int]): Current position of the agent.
        reward (float): Accumulated reward for the agent.
        done (bool): Whether the agent has completed its task.
    """

    def __init__(self, agent_id: int):
        self.id = agent_id
        self.position = (0, 0)

        self.state = "active"

        # resources
        self.money = None
        self.claimed_tiles = []

        # exclude player color id 0
        c = self.id
        if self.id % len(AGENT_COLORS) == 0:
            c = 1
        self.color = AGENT_COLORS[c % len(AGENT_COLORS)]

        self.reward = 0.0
        self.done = False
        # TODO probably call self.reset() here

    # def decide_action(self, observation: Dict[str, Any]) -> Dict[str, int]:
    #     """
    #     Decides on an action based on the observation.
    #
    #     Args:
    #         observation (Dict[str, Any]): The current observation.
    #
    #     Returns:
    #         Dict[str, int]: The action dictionary.
    #     """
    #     # For simplicity, randomly choose a movement direction
    #     move_direction = np.random.choice([0, 1, 2, 3, 4])  # 0: No move, 1-4: Directions
    #     return {'move': move_direction}

    def apply_action(self, action: Dict[str, Any]):
        """
        Updates the agent's internal state based on the action result.

        Args:
            action_result (Dict[str, Any]): The outcome of the action.
        """
        move_direction = action.get("move", None)
        if move_direction:
            new_position = self._calculate_new_position(self.position, move_direction)
            # Update position
            self.position = new_position
            print(f"Agent {self.id}: Move successful to position {self.position}.")

        return False

    def reset(self, env_settings: Dict[str, Any]):
        """
        Resets the agent to the initial state.

        Args:
            env_settings (Dict[str, Any]): Environment settings.
        """
        # max_x = int(math.sqrt(env_settings("tiles")))
        max_x = 10
        self.position = (np.random.randint(0, max_x), np.random.randint(0, max_x))
        self.state = "active"
        self.money = 100  # for now
        # TODO maybe set intial possition as claimed tile

        # initial_money = env_settings.get_setting("agent_initial_budget")
        # if env_settings.get_setting("agent_initial_budget") == "equal":
        #     self.money = initial_money
        # elif env_settings.get_setting("agent_initial_budget") == "gauss":
        #     # gauss distributed around initial
        #     self.money = random.gauss(initial_money, 100)
        # else:
        #     # randomly distributed money
        #     self.money = random.randint(0, 1000)

    def update(self):
        # Update the agent's state

        for _, tile in enumerate(self.claimed_tiles):
            self.money += tile.get_round_value()

        # TODO define settings matrix?

        if self.money <= 0:  # TODO adapt different state transitions
            self.state = "Done"

    def get_observation(self):
        return self.state

    def draw(self, screen, square_size, zoom_level, pan_x, pan_y):
        radius = square_size / 2
        # get a color modulo the number of colors

        pygame.draw.circle(
            screen,
            self.color,
            (
                (self.position[0] * square_size) + radius,
                (self.position[1] * square_size) + radius,
            ),
            radius,
        )

    def get_possible_actions(self):
        if self.state == "Done":
            possible_actions = []
        else:
            possible_actions = [1, 2, 3]  # ['move', 'claim_tile', 'build']

        return possible_actions

    def get_state_for_env_info(self) -> Dict[str, Any]:
        # define here what information of all agents is visible to all other agents
        return {"position": self.position, "money": self.money}

    def _calculate_new_position(
        self, current_position: Tuple[int, int], move_direction: int
    ) -> Tuple[int, int]:
        """
        Calculates the new position based on the current position and move direction.

        Args:
            current_position (Tuple[int, int]): The agent's current position.
            move_direction (int): Direction to move (0: No move, 1: Up, 2: Down, 3: Left, 4: Right).

        Returns:
            Tuple[int, int]: The new position after the move.
        """
        x, y = current_position
        if move_direction == 1:  # Up
            y -= 1
        elif move_direction == 2:  # Down
            y += 1
        elif move_direction == 3:  # Left
            x -= 1
        elif move_direction == 4:  # Right
            x += 1
        # No move if move_direction is 0 or unrecognized
        return (x, y)
