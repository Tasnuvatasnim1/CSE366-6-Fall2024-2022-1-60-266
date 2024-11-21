import pygame
from agent import Agent
from environment import Environment

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Agent Environment Simulation")

    env = Environment(width=800, height=600)
    agent = Agent(environment=env)

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            agent.move("up")
        elif keys[pygame.K_DOWN]:
            agent.move("down")
        elif keys[pygame.K_LEFT]:
            agent.move("left")
        elif keys[pygame.K_RIGHT]:
            agent.move("right")

        position = agent.status()
        rect_position = (position[0], position[1], agent.size[0], agent.size[1])

        pygame.draw.rect(screen, (0, 0, 255), rect_position)

        font = pygame.font.Font(None, 36)
        text = font.render(f"Position: {position}", True, (0, 0, 0))
        text2 = font.render(f"Position: {position}", True, (0, 0, 0))
        screen.blit(text, (10, 10))
        screen.blit(text2, (300, 260))


        pygame.display.flip()
        clock.tick(15)

    pygame.quit()

if __name__ == "__main__":
    main()
