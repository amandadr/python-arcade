import os
os.environ['DISPLAY'] = ":0"  # Set the display

import pygame
import random
import asyncio

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CIRCLE_RADIUS = 15
SPEED = 5

# Colors
RED = (255, 0, 0)
COLORS = [(255, 255, 255), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Global variables
circle_x = random.randint(CIRCLE_RADIUS, SCREEN_WIDTH - CIRCLE_RADIUS)
circle_y = SCREEN_HEIGHT // 2
circle_dx = SPEED
circle_dy = 0
circle_color = RED
running = True

# Score
score = 0
lvl2 = 4
font = pygame.font.Font(None, 36)  # Default font

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Click the Circle")
clock = pygame.time.Clock()

# Function to choose a random diagonal direction
def choose_random_diagonal():
    directions = [
        (SPEED, SPEED),
        (-SPEED, SPEED),
        (SPEED, -SPEED),
        (-SPEED, -SPEED),
    ]
    return random.choice(directions)

async def main():
    global circle_x, circle_y, circle_dx, circle_dy, circle_color, running, score

    while running:
        screen.fill((0, 0, 0))

        # Draw the circle
        pygame.draw.circle(screen, circle_color, (circle_x, circle_y), CIRCLE_RADIUS)

        # Move the circle
        if score <= lvl2:
            # Restrict to horizontal or vertical movement
            if circle_dx != 0:
                circle_dy = 0
            else:
                circle_dx = 0
        else:
            # Allow diagonal movement
            pass

        circle_x += circle_dx
        circle_y += circle_dy

        # Check for wall collision
        if circle_x - CIRCLE_RADIUS <= 0 or circle_x + CIRCLE_RADIUS >= SCREEN_WIDTH:
            circle_dx = -circle_dx
        if circle_y - CIRCLE_RADIUS <= 0 or circle_y + CIRCLE_RADIUS >= SCREEN_HEIGHT:
            circle_dy = -circle_dy

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                distance = ((mouse_x - circle_x) ** 2 + (mouse_y - circle_y) ** 2) ** 0.5
                if distance <= CIRCLE_RADIUS:
                    if score < lvl2:
                        # Switch between horizontal and vertical when under threshold
                        if circle_dx != 0:
                            circle_dx = 0
                            circle_dy = SPEED
                        else:
                            circle_dx = SPEED
                            circle_dy = 0
                    else:
                        # Choose a new random diagonal direction
                        circle_dx, circle_dy = choose_random_diagonal()
                    circle_color = random.choice([c for c in COLORS if c != circle_color])
                    score += 1  # Increment score on click

        # Display the score
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)  # Let other tasks run

# This is the program entry point
asyncio.run(main())