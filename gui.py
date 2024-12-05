import pygame
from pygame.locals import *
import sys  # For exiting gracefully with Ctrl+C

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

# Set up the display (fullscreen for CLI)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Touch GUI - Calculator")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 122, 255)
DARK_BLUE = (0, 0, 139)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 40)  # Default font
display_font = pygame.font.SysFont(None, 50)

# Calculator state
current_input = ""

# Buttons layout
button_labels = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"]
]

button_rects = []  # Holds the button positions

# Calculate button dimensions
button_width = SCREEN_WIDTH // 4
button_height = (SCREEN_HEIGHT - 100) // 4  # Reserve space for the display

# Create button positions
for row_idx, row in enumerate(button_labels):
    row_rects = []
    for col_idx, label in enumerate(row):
        x = col_idx * button_width
        y = 100 + row_idx * button_height
        row_rects.append((label, pygame.Rect(x, y, button_width, button_height)))
    button_rects.append(row_rects)

# Main loop
running = True
try:
    while running:
        # Fill the screen
        screen.fill(WHITE)

        # Draw the display area
        pygame.draw.rect(screen, DARK_BLUE, (0, 0, SCREEN_WIDTH, 100))
        text_surface = display_font.render(current_input, True, WHITE)
        screen.blit(text_surface, (10, 25))

        # Draw buttons
        for row in button_rects:
            for label, rect in row:
                pygame.draw.rect(screen, BLUE, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)  # Border
                text_surface = font.render(label, True, WHITE)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for row in button_rects:
                    for label, rect in row:
                        if rect.collidepoint(mouse_pos):
                            if label == "C":
                                current_input = ""  # Clear input
                            elif label == "=":
                                try:
                                    # Evaluate the expression safely
                                    current_input = str(eval(current_input))
                                except Exception:
                                    current_input = "Error"
                            else:
                                current_input += label  # Append the button value

        # Update the display
        pygame.display.flip()

        # Add a short delay to optimize CPU usage
        pygame.time.delay(10)

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    print("\nExiting...")
    running = False

finally:
    # Quit pygame
    pygame.quit()
    sys.exit()