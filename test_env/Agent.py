import random
from typing import Tuple


class Agent:
    def __init__(self, id, x_max, y_max):
        self.id = id
        self.state = None
        self.action = "Running"
        self.q_table = None
        self.x_max = x_max
        self.y_max = y_max

        self.reward = 0

        self.action_probabilities = {
            'move': 0,
            'claim': 0.7,
            'build_city': 0.3,
            'build_road': 0.0,
            'build_farm': 0.0,
            'none': 0.0
        }

    def get_action(self, env_info, possible_actions):
        # action dictionary mask
        selected_action = []

        action_types = list(self.action_probabilities.keys())
        probabilities = list(self.action_probabilities.values())

        action_type = random.choices(action_types, weights=probabilities, k=1)[0]
        claimable_tiles = possible_actions[0]

        # Instantiate the corresponding Action class
        if action_type == 'move':
            direction = random.randint(1, 4)  # 1: Up, 2: Down, 3: Left, 4: Right
            props = {"direction": direction}
        elif action_type == 'claim':
            position = random.choice(list(claimable_tiles))
            props = {"position": position}
        elif action_type == 'build_city':
            position = random.choice(list(claimable_tiles))
            props = {"position": position}
        # elif action_type == 'build_road':
        #     position = self.decide_build_position()
        #
        # elif action_type == 'build_farm':
        #     position = self.decide_build_position()

        else:
            # No action
            action_type = None
            props = None

        action = {
            "type": action_type,
            "props": props
        }
        selected_action.append(action)
        # TODO add more advanced action selection here
        # TODO: vectorize and normalize the env_info here!!
        # TODO connect to Q-table or other RL algorithm
        return selected_action

    def update(self, reward):
        self.reward += reward
