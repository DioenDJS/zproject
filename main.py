import pygame
import pygame.mixer
import sys
import random
import time
import os

# Inicialização do Pygame
pygame.mixer.init()
pygame.init()

# Definições de tela
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRID_SIZE = 40
ROWS = SCREEN_HEIGHT // GRID_SIZE
COLS = SCREEN_WIDTH // GRID_SIZE

# Inicialização da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("z-project")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Carregar imagens e redimensionar
heroi_img = pygame.image.load(os.path.join("heroi.png"))
heroi_img = pygame.transform.scale(heroi_img, (GRID_SIZE, GRID_SIZE))

dama_img = pygame.image.load(os.path.join("dama.png"))
dama_img = pygame.transform.scale(dama_img, (GRID_SIZE, GRID_SIZE))

soldado_img = pygame.image.load(os.path.join("soldado.png"))
soldado_img = pygame.transform.scale(soldado_img, (GRID_SIZE, GRID_SIZE))

hype_img = pygame.image.load(os.path.join("hype.png"))
hype_img = pygame.transform.scale(hype_img, (GRID_SIZE, GRID_SIZE))

zumbie_img = pygame.image.load(os.path.join("zumbie.png"))
zumbie_img = pygame.transform.scale(zumbie_img, (GRID_SIZE, GRID_SIZE))

zumbie_furioso_img = pygame.image.load(os.path.join("zumbie_furioso.png"))
zumbie_furioso_img = pygame.transform.scale(zumbie_furioso_img, (GRID_SIZE, GRID_SIZE))

sobrevivente_img = pygame.image.load(os.path.join("sobrevivente-1.png"))
sobrevivente_img = pygame.transform.scale(sobrevivente_img, (GRID_SIZE, GRID_SIZE))

# Carregar o som
pulo_sound = pygame.mixer.Sound("pulo.mp3")

# Função para criar um tabuleiro vazio
def create_empty_board():
    return [[None] * COLS for _ in range(ROWS)]

# Função para desenhar o tabuleiro
def draw_board(board, selector_pos):
    screen.fill(BLACK)  # Define o fundo do tabuleiro como preto

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] is not None:
                rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                screen.blit(board[row][col], rect)
            pygame.draw.rect(screen, BLACK, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    selector_rect = pygame.Rect(selector_pos[1] * GRID_SIZE, selector_pos[0] * GRID_SIZE, GRID_SIZE * 2, GRID_SIZE)
    pygame.draw.rect(screen, YELLOW, selector_rect, 2)

# Função para trocar dois quadrados de lugar
def swap_squares(board, row1, col1, row2, col2):
    board[row1][col1], board[row2][col2] = board[row2][col2], board[row1][col1]

def generate_random_line(prev_line):
    images = [heroi_img, dama_img, soldado_img, hype_img, zumbie_img, zumbie_furioso_img, sobrevivente_img]
    new_line = [random.choice(images) for _ in range(COLS)]

    while has_image_sequence(new_line, prev_line):
        new_line = [random.choice(images) for _ in range(COLS)]

    return new_line

def has_image_sequence(line1, line2):
    for i in range(len(line1) - 2):
        if line1[i] == line1[i + 1] == line1[i + 2]:
            return True

    for i in range(len(line1)):
        if i < len(line2) - 2 and line1[i] == line2[i] == line2[i + 2]:
            return True

    return False

# Função para verificar e apagar sequências
def check_and_clear_matches(board):
    for row in range(ROWS):
        for col in range(COLS - 2):
            # Check horizontal matches
            if board[row][col] == board[row][col + 1] == board[row][col + 2] and board[row][col] is not None:
                # Marcar os cubos da sequência como "vazios" (None)
                match_length = 3
                while col + match_length < COLS and board[row][col] == board[row][col + match_length]:
                    match_length += 1

                for i in range(match_length):
                    board[row][col + i] = None

    for row in range(ROWS - 2):
        for col in range(COLS):
            # Check vertical matches
            if board[row][col] == board[row + 1][col] == board[row + 2][col] and board[row][col] is not None:
                # Marcar os cubos da sequência como "vazios" (None)
                match_length = 3
                while row + match_length < ROWS and board[row][col] == board[row + match_length][col]:
                    match_length += 1

                for i in range(match_length):
                    board[row + i][col] = None

# Função para simular a queda dos cubos
def apply_gravity(board):
    for col in range(COLS):
        for row in range(ROWS - 1, 0, -1):
            if board[row][col] is None:
                # Se o cubo atual estiver vazio, procure por um cubo acima para trocar
                for above_row in range(row - 1, -1, -1):
                    if board[above_row][col] is not None:
                        board[row][col], board[above_row][col] = board[above_row][col], board[row][col]
                        break

# Função para verificar se um cubo atingiu o topo
def check_game_over(board):
    return any(cube is not None for cube in board[0])

# Função principal do jogo
def main():
    # Inicialização do tabuleiro
    board = create_empty_board()
    selector_pos = [ROWS - 2, 0]  # O seletor começa na penúltima linha e na primeira coluna

    clock = pygame.time.Clock()
    FPS = 0.01  # Reduzi para 0.1 FPS
    time_passed = 0  # Contador de tempo para adicionar uma nova linha
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Troca os quadrados selecionados
                    swap_squares(board, selector_pos[0], selector_pos[1], selector_pos[0], selector_pos[1] + 1)
                    pulo_sound.play()  # Adiciona a reprodução do som

                elif event.key == pygame.K_LEFT and selector_pos[1] > 0:
                    selector_pos[1] -= 1
                elif event.key == pygame.K_RIGHT and selector_pos[1] < COLS - 2:
                    selector_pos[1] += 1
                elif event.key == pygame.K_UP and selector_pos[0] > 0:
                    selector_pos[0] -= 1
                elif event.key == pygame.K_DOWN and selector_pos[0] < ROWS - 2:
                    selector_pos[0] += 1

        # Verifica se algum cubo atingiu o topo
        if check_game_over(board):
            game_over = True

        if not game_over:
            time_passed += clock.get_rawtime()
            clock.tick()
            if time_passed >= 4000:  # Adiciona uma nova linha a cada segundo
                new_line = generate_random_line(board[0])
                board.pop(0)  # Remove a linha mais alta
                board.append(new_line)
                time_passed = 0  # Reseta o contador de tempo

            # Verifica e apaga sequências
            check_and_clear_matches(board)

            # Aplica a gravidade para fazer os cubos caírem
            apply_gravity(board)

            # Desenho do tabuleiro
            screen.fill(BLACK)
            draw_board(board, selector_pos)

            pygame.display.flip()
            time.sleep(0.1)  # Adiciona um pequeno delay para simular a queda dos cubos

        else:
            # Congela a tela e exibe a mensagem de fim de jogo
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over - Pressione Q para sair", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()
