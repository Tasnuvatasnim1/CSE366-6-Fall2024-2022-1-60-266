import pygame
import heapq

class Agent(pygame.sprite.Sprite):
    def __init__(self, environment, grid_size):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill((0, 0, 255))  # Agent color is blue
        self.rect = self.image.get_rect()
        self.grid_size = grid_size
        self.environment = environment
        self.position = [0, 0]  # Starting at the top-left corner of the grid
        self.rect.topleft = (0, 0)
        self.task_completed = 0
        self.completed_tasks = []
        self.algorithm = "A*"  # Default algorithm

    def move(self, direction):
        """Move the agent within the grid, constrained by barriers."""
        x, y = self.position
        if direction == "up":
            y -= 1
        elif direction == "down":
            y += 1
        elif direction == "left":
            x -= 1
        elif direction == "right":
            x += 1

        # Check if the new position is within bounds and not a barrier
        if self.environment.is_within_bounds(x, y) and not self.environment.is_barrier(x, y):
            self.position = [x, y]
            self.rect.topleft = (x * self.grid_size, y * self.grid_size)

    def check_task_completion(self):
        """Check if the agent has reached a task location."""
        position_tuple = tuple(self.position)
        if position_tuple in self.environment.task_locations:
            task_number = self.environment.task_locations.pop(position_tuple)
            self.task_completed += 1
            self.completed_tasks.append(task_number)

    def ucs(self):
        """Uniform Cost Search (UCS) algorithm for automated movement."""
        start = tuple(self.position)
        frontier = [(0, start)]  # Priority queue: (cost, position)
        came_from = {start: None}

        while frontier:
            current_cost, current = heapq.heappop(frontier)

            # Check if the agent reaches a task location
            if tuple(current) in self.environment.task_locations:
                self.check_task_completion()  # Complete the task
                break  # Task completed, stop the search

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Down, Left, Up
                next_node = (current[0] + dx, current[1] + dy)
                if self.environment.is_within_bounds(*next_node) and not self.environment.is_barrier(*next_node):
                    if next_node not in came_from:
                        heapq.heappush(frontier, (current_cost + 1, next_node))
                        came_from[next_node] = current

        return self.reconstruct_path(came_from, start, current)

    def a_star(self):
        """A* pathfinding algorithm for automated movement."""
        start = tuple(self.position)

        # Get the nearest task location as the goal
        goal = self.get_nearest_task()

        if not goal:
            return []  # No tasks remaining

        frontier = [(0, start)]  # Priority queue: (priority, position)
        came_from = {start: None}
        cost_so_far = {start: 0}

        def heuristic(a, b):
            """Manhattan distance heuristic."""
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        while frontier:
            _, current = heapq.heappop(frontier)

            # Check if the agent reaches a task location (goal)
            if tuple(current) == goal:
                self.check_task_completion()  # Complete the task
                return self.reconstruct_path(came_from, start, current)  # Return the path

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_node = (current[0] + dx, current[1] + dy)
                if self.environment.is_within_bounds(*next_node) and not self.environment.is_barrier(*next_node):
                    new_cost = cost_so_far[current] + 1
                    if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                        cost_so_far[next_node] = new_cost
                        priority = new_cost + heuristic(next_node, goal)  # Update the priority
                        heapq.heappush(frontier, (priority, next_node))
                        came_from[next_node] = current

        return []  # Return empty if no path found

    def get_nearest_task(self):
        """Return the nearest task location based on Manhattan distance."""
        if not self.environment.task_locations:
            return None  # No tasks available

        # Find the nearest task based on Manhattan distance
        nearest_task = min(self.environment.task_locations.keys(),
                           key=lambda task: abs(self.position[0] - task[0]) + abs(self.position[1] - task[1]))

        return nearest_task

    def reconstruct_path(self, came_from, start, goal):
        """Reconstruct the path from start to goal."""
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from.get(current)
        path.reverse()
        return path
