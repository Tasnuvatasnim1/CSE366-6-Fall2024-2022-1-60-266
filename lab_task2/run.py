import pygame
import sys
from agent import Agent
from environment import Environment

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRID_SIZE = 40
STATUS_WIDTH = 250
BACKGROUND_COLOR = (255, 255, 255)
BARRIER_COLOR = (0, 0, 0)
TASK_COLOR = (255, 0, 0)
AGENT_COLOR = (0, 0, 255)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (0, 200, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
MOVEMENT_DELAY = 200  # Movement delay in milliseconds

def draw_button(screen, rect, text, font):
    """Draws a button with text."""
    pygame.draw.rect(screen, BUTTON_COLOR, rect)
    text_surface = font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_panel(screen, font, agent, environment, path_cost, ucs_results, astar_results):
    """Draws the status panel showing both algorithms results."""
    status_x = WINDOW_WIDTH + 10
    y_offset = 20
    panel_texts = [
        f"Current Algorithm: {agent.algorithm}",
        f"Tasks Completed: {agent.task_completed}",
        f"Position: {agent.position}",
        f"Completed Tasks: {list(agent.completed_tasks)}",
        f"Total Path Cost (Current): {path_cost}",
        "",
        f"A* Algorithm:",
        f"Tasks Completed: {astar_results['tasks_completed']}",
        f"Path Cost: {astar_results['path_cost']}","",
        f"UCS Algorithm:",
        f"Tasks Completed: {ucs_results['tasks_completed']}",
        f"Path Cost: {ucs_results['path_cost']}",
    ]
    for text in panel_texts:
        text_surface = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surface, (status_x, y_offset))
        y_offset += 30

def main():
    pygame.init()

    # Set up display with a side panel
    screen = pygame.display.set_mode((WINDOW_WIDTH + STATUS_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame AI Grid Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Initialize environment and agent
    environment = Environment(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, num_tasks=5, num_barriers=15)
    agent = Agent(environment, GRID_SIZE)

    # Store the initial state of tasks and barriers
    initial_task_locations = environment.task_locations.copy()
    initial_barrier_locations = environment.barrier_locations.copy()

    # Variables to track the results of both algorithms
    ucs_results = {'tasks_completed': 0, 'path_cost': 0}
    astar_results = {'tasks_completed': 0, 'path_cost': 0}

    # Button setup
    start_button_rect = pygame.Rect(WINDOW_WIDTH + 50, WINDOW_HEIGHT - 140, 150, 50)
    toggle_button_rect = pygame.Rect(WINDOW_WIDTH + 50, WINDOW_HEIGHT - 70, 150, 50)

    # Variables to control simulation
    start_simulation = False
    current_path = []
    last_move_time = pygame.time.get_ticks()
    total_path_cost = 0

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not start_simulation and start_button_rect.collidepoint(event.pos):
                    start_simulation = True
                elif toggle_button_rect.collidepoint(event.pos):
                    # Toggle between algorithms and reset environment
                    agent.algorithm = "UCS" if agent.algorithm == "A*" else "A*"
                    current_path = []  # Reset path
                    start_simulation = False  # Reset the simulation flag
                    
                    # Reset the environment to its initial state
                    environment.task_locations = initial_task_locations.copy()
                    environment.barrier_locations = initial_barrier_locations.copy()
                    agent.position = [0, 0]
                    agent.rect.topleft = (0, 0)
                    agent.task_completed = 0
                    agent.completed_tasks = []

        # Draw the grid
        for x in range(environment.columns):
            for y in range(environment.rows):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)

        # Draw barriers
        for bx, by in environment.barrier_locations:
            pygame.draw.rect(screen, BARRIER_COLOR, pygame.Rect(bx * GRID_SIZE, by * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw tasks
        for (tx, ty), task_number in environment.task_locations.items():
            task_rect = pygame.Rect(tx * GRID_SIZE, ty * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, TASK_COLOR, task_rect)
            task_text = font.render(str(task_number), True, (255, 255, 255))

            # Calculate the position to center the task number in the task square
            text_rect = task_text.get_rect(center=task_rect.center)
            screen.blit(task_text, text_rect.topleft)

        # Draw agent
        pygame.draw.rect(screen, AGENT_COLOR, agent.rect)

        # Draw the Start button only if the simulation hasn't started
        if not start_simulation:
            draw_button(screen, start_button_rect, "Start", font)

        # Draw the Toggle button
        toggle_text = f"Toggle to {'UCS' if agent.algorithm == 'A*' else 'A*'}"
        draw_button(screen, toggle_button_rect, toggle_text, font)

        # Status panel
        draw_panel(screen, font, agent, environment, total_path_cost, ucs_results, astar_results)

        # Simulation logic
        if start_simulation and environment.task_locations:
            if agent.algorithm == "UCS" and not current_path:
                current_path = agent.ucs()
            elif agent.algorithm == "A*" and not current_path:
                current_path = agent.a_star()

            if current_path:
                current_time = pygame.time.get_ticks()
                if current_time - last_move_time > MOVEMENT_DELAY:
                    next_step = current_path.pop(0)
                    agent.position = [next_step[0], next_step[1]]
                    agent.rect.topleft = (next_step[0] * GRID_SIZE, next_step[1] * GRID_SIZE)
                    last_move_time = current_time
                    total_path_cost += 1
                    agent.check_task_completion()

            if not environment.task_locations:
                start_simulation = False
            
            

            # Update algorithm results
            if agent.algorithm == "UCS":
                ucs_results['tasks_completed'] = agent.task_completed
                ucs_results['path_cost'] = total_path_cost
            elif agent.algorithm == "A*":
                astar_results['tasks_completed'] = agent.task_completed
                astar_results['path_cost'] = total_path_cost

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
