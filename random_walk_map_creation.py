import pygame
import random

default_land_color = (34, 139, 34)
default_water_color = (70, 130, 180)
default_border_color = (0, 0, 0)

default_land_value = 0
default_water_value = 1

default_tile_owner = 0


class MapSquare:
    def __init__(self, x, y, land_value=default_land_value):
        self.x = x
        self.y = y
        self.square_size = 10
        self.default_border_color = default_border_color
        self.default_color = default_land_color

        self.land_value = land_value
        self.owner_value = default_tile_owner

    def set_owner(self, owner_value):
        self.owner_value = owner_value

    def get_owner(self):
        return self.owner_value

    def set_land_value(self, land_value):
        self.land_value = land_value

    def get_land_value(self):
        return self.land_value

    def draw(self, screen):
        self.draw_square_fill(screen)
        #self.draw_border(screen)

    def draw_square_fill(self, screen):
        # change drawn color based on land value
        color = self.default_color
        if self.get_land_value() == default_land_value:
            color = default_land_color
        else:
            color = default_water_color
        pygame.draw.rect(screen, color, (self.x, self.y, self.square_size, self.square_size))

    def draw_border(self, screen):
        # draw square border
        color = self.default_border_color
        if self.get_owner() == default_tile_owner:
            color = default_border_color
        else:
            color = default_water_color
        pygame.draw.rect(screen, color, (self.x, self.y, self.square_size, self.square_size), 1)


class Map:
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.squares = []
        self.screen = None
        self.square_size = 10

        self.water_budget_per_agent = 100  # Adjust the total amount of land per agent
        self.numb_agents = 10

    def create_map(self, width, height):
        self.width = width
        self.height = height

        # create map squares
        self.squares = [[MapSquare(x * self.square_size, y * self.square_size) for x in range(self.width)] for y in
                        range(self.height)]

        agents = [
            Map_Agent(random.randint(0, self.width - 1), random.randint(0, self.height - 1),
                      self.water_budget_per_agent) for i in range(self.numb_agents)]

        # Initialize Pygame
        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Agent-based Landmass Generation')

        # Main loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Move each agent and draw the world
            for agent in agents:
                agent.walk(self)
            self.draw(self.screen)

            # Update the display
            pygame.display.flip()

    def draw(self, screen):

        for row in self.squares:
            for square in row:
                square.draw(screen)

    def get_neighbors(self, x, y):
        # Returns the coordinates of the square's neighbors
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny))
        return neighbors


# Agent class
class Map_Agent:
    def __init__(self, x, y, water_budget):
        self.x = x
        self.y = y
        self.water_budget = water_budget  # Total amount of water to create

    def walk(self, world_map):
        # Random walk step
        step_x = random.choice([-1, 0, 1])
        step_y = random.choice([-1, 0, 1])
        self.x += step_x
        self.y += step_y
        # Keep the agent within bounds of the world
        self.x = max(0, min(self.x, world_map.width - 1))
        self.y = max(0, min(self.y, world_map.height - 1))

        # Create water if there is budget left
        if self.water_budget > 0:
            if world_map.squares[self.y][self.x].get_land_value() == default_land_value:
                world_map.squares[self.y][self.y].set_land_value(default_water_value)
                self.water_budget -= 1
