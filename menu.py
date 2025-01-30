import pygame
import sys
import subprocess
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders - Menu")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

font_path = "PressStart2P-Regular.ttf"
font = pygame.font.Font(font_path, 16)

background_image = pygame.image.load("kosmos.png")
background = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

sound_enabled = True
difficulty_level = "Medium"

def draw_text(text, font, color, surface, x, y, border_color=None, border_width=2):
    if border_color:
        for offset_x in range(-border_width, border_width + 1):
            for offset_y in range(-border_width, border_width + 1):
                if offset_x != 0 or offset_y != 0:
                    textobj = font.render(text, 1, border_color)
                    textrect = textobj.get_rect()
                    textrect.center = (x + offset_x, y + offset_y)
                    surface.blit(textobj, textrect)

    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_button(text, font, color, surface, x, y, width, height, border_color=None):
    draw_text(text, font, color, surface, x + width // 2, y + height // 2, border_color)

def show_instructions():
    instructions_text = [
        "How to Play:",
        "Use arrow keys or WASD to move the ship.",
        "Press SPACE to shoot.",
        "Objective: Destroy enemies, survive, and collect points.",
        "Points system:",
        "Normal enemy: 10 points.",
        "Mother ship: 300 points.",
        "Level completion: +50 points.",
        "Avoid enemies and their attacks.",
        "Collect power-ups and shields.",
        "Press ESC to return to the main menu."
    ]

    running = True
    y_offset = 100
    line_height = 20
    max_lines_on_screen = HEIGHT // line_height - 2

    while running:
        screen.blit(background, (0, 0))

        draw_text("How to Play", font, YELLOW, screen, WIDTH // 2, 50, border_color=BLACK, border_width=2)

        lines_to_draw = instructions_text[:max_lines_on_screen]
        y_offset = 100
        for line in lines_to_draw:
            draw_text(line, font, WHITE, screen, WIDTH // 2, y_offset)
            y_offset += line_height

        draw_text("Press ESC to return", font, WHITE, screen, WIDTH // 2, y_offset + 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

def show_settings():
    global sound_enabled, difficulty_level

    def get_options():
        return [
            "Sound: ON" if sound_enabled else "Sound: OFF",
            "Difficulty: " + difficulty_level,
            "Back"
        ]

    selected_option = 0
    button_width = 400
    button_height = 60
    button_gap = 80

    running = True
    while running:
        screen.blit(background, (0, 0))

        draw_text("Settings", font, YELLOW, screen, WIDTH // 2, 50, border_color=BLACK, border_width=2)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        options = get_options()

        for i, option in enumerate(options):
            button_x = WIDTH // 2 - button_width // 2
            button_y = 200 + i * button_gap

            if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                color = RED
                border_color = BLACK
            else:
                color = BLACK
                border_color = None

            draw_button(option, font, color, screen, button_x, button_y, button_width, button_height, border_color)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                if event.key == pygame.K_RETURN:
                    if options[selected_option] == "Sound: ON" or options[selected_option] == "Sound: OFF":
                        sound_enabled = not sound_enabled
                    elif options[selected_option] == "Difficulty: Easy":
                        difficulty_level = "Medium"
                    elif options[selected_option] == "Difficulty: Medium":
                        difficulty_level = "Hard"
                    elif options[selected_option] == "Difficulty: Hard":
                        difficulty_level = "Easy"
                    elif options[selected_option] == "Back":
                        return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, option in enumerate(options):
                        button_x = WIDTH // 2 - button_width // 2
                        button_y = 200 + i * button_gap

                        if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                            if option == "Sound: ON" or option == "Sound: OFF":
                                sound_enabled = not sound_enabled
                            elif option == "Difficulty: Easy":
                                difficulty_level = "Medium"
                            elif option == "Difficulty: Medium":
                                difficulty_level = "Hard"
                            elif option == "Difficulty: Hard":
                                difficulty_level = "Easy"
                            elif option == "Back":
                                return

def start_game():
    start_time = time.time()
    loading_time = 5
    loading_percentage = 0

    while time.time() - start_time < loading_time:
        screen.blit(background, (0, 0))

        draw_text("Loading...", font, YELLOW, screen, WIDTH // 2, 100, border_color=BLACK, border_width=2)

        elapsed_time = time.time() - start_time
        loading_percentage = int((elapsed_time / loading_time) * 100)

        progress_bar_width = 400
        progress_bar_height = 30
        progress_bar_x = (WIDTH - progress_bar_width) // 2
        progress_bar_y = HEIGHT // 2

        pygame.draw.rect(screen, (50, 50, 50), (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))

        pygame.draw.rect(screen, (0, 255, 0), (progress_bar_x, progress_bar_y, (loading_percentage / 100) * progress_bar_width, progress_bar_height))

        draw_text(f"{loading_percentage}%", font, WHITE, screen, WIDTH // 2, progress_bar_y + progress_bar_height + 10)

        draw_text(f"Sound: {'ON' if sound_enabled else 'OFF'}", font, WHITE, screen, WIDTH // 2, progress_bar_y + progress_bar_height + 30)
        draw_text(f"Difficulty: {difficulty_level}", font, WHITE, screen, WIDTH // 2, progress_bar_y + progress_bar_height + 50)

        pygame.display.update()

    subprocess.Popen(["python", "spaceInvaders.py", str(sound_enabled), difficulty_level])

def main_menu():
    selected_option = 0
    options = ["Start Game", "High Scores", "Settings", "How to Play", "Quit"]
    button_width = 400
    button_height = 60
    button_gap = 80

    running = True
    while running:
        screen.blit(background, (0, 0))

        draw_text("SPACE INVADERS", font, YELLOW, screen, WIDTH // 2, 100, border_color=BLACK, border_width=2)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for i, option in enumerate(options):
            button_x = WIDTH // 2 - button_width // 2
            button_y = 200 + i * button_gap

            if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                color = RED
                border_color = BLACK
            else:
                color = BLACK
                border_color = None

            draw_button(option, font, color, screen, button_x, button_y, button_width, button_height, border_color)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                if event.key == pygame.K_RETURN:
                    if options[selected_option] == "Start Game":
                        start_game()
                    elif options[selected_option] == "High Scores":
                        print("Tabela wyników")
                    elif options[selected_option] == "Settings":
                        show_settings()
                    elif options[selected_option] == "How to Play":
                        show_instructions()
                    elif options[selected_option] == "Quit":
                        pygame.quit()
                        sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, option in enumerate(options):
                        button_x = WIDTH // 2 - button_width // 2
                        button_y = 200 + i * button_gap

                        if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                            if option == "Start Game":
                                start_game()
                            elif option == "High Scores":
                                print("Tabela wyników")
                            elif option == "Settings":
                                show_settings()
                            elif option == "How to Play":
                                show_instructions()
                            elif option == "Quit":
                                pygame.quit()
                                sys.exit()

if __name__ == "__main__":
    main_menu()
