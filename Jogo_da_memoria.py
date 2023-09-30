import pygame
import random
pygame.init()

# Defina as constantes
WIDTH, HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 100, 100
GRID_SIZE = 4
GRID_ROWS, GRID_COLS = GRID_SIZE, GRID_SIZE
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Crie a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Memória")

# Defina a fonte
font = pygame.font.Font(None, 36)

# Relógio para controlar a taxa de quadros
clock = pygame.time.Clock()

# Função para desenhar um card na tela
def draw_card(x, y, card_value, face_up):
    card_color = WHITE if face_up else BLACK
    pygame.draw.rect(screen, card_color, (x, y, CARD_WIDTH, CARD_HEIGHT))
    if face_up:
        text_surface = font.render(str(card_value), True, BLACK)
        screen.blit(text_surface, (x + 30, y + 30))

# Crie uma matriz para representar as cartas no jogo
grid = [[0] * GRID_COLS for _ in range(GRID_ROWS)]

# Crie uma lista de valores de cartas em pares
card_values = list(range(1, GRID_ROWS * GRID_COLS // 2 + 1)) * 2
random.shuffle(card_values)

# Preencha a matriz de cartas com valores aleatórios
for row in range(GRID_ROWS):
    for col in range(GRID_COLS):
        value = card_values.pop()
        grid[row][col] = value

# Outras variáveis de controle do jogo
selected_card = None
first_selection = True
matched_pairs = 0

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # Lógica do jogo
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * CARD_WIDTH
            y = row * CARD_HEIGHT

            card = grid[row][col]

            if card == 0:
                continue

            # Verifica se o mouse está sobre a carta
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if x < mouse_x < x + CARD_WIDTH and y < mouse_y < y + CARD_HEIGHT:
                if pygame.mouse.get_pressed()[0] and selected_card is None:
                    selected_card = (row, col)
                elif pygame.mouse.get_pressed()[0] and selected_card is not None:
                    if grid[row][col] == grid[selected_card[0]][selected_card[1]]:
                        grid[row][col] = 0
                        grid[selected_card[0]][selected_card[1]] = 0
                        matched_pairs += 1
                    selected_card = None
                elif pygame.mouse.get_pressed()[2]:
                    selected_card = None

            # Desenha a carta
            face_up = grid[row][col] == 0 or (row, col) == selected_card
            draw_card(x, y, card, face_up)

    # Verifica se o jogo terminou
    if matched_pairs == GRID_ROWS * GRID_COLS // 2:
        game_over_text = font.render("Parabéns! Você ganhou!", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
