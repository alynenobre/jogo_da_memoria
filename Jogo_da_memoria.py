import pygame
import random
pygame.init()

# Defina as constantes
LARGURA, ALTURA = 800, 600
LARGURA_CARTA, ALTURA_CARTA = 100, 100
TAMANHO_GRADE = 4
LINHAS_GRADE, COLUNAS_GRADE = TAMANHO_GRADE, TAMANHO_GRADE
FPS = 60

# Crie a tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Memória")

# Relógio para controlar a taxa de quadros
relogio = pygame.time.Clock()

# Crie uma matriz para representar as cartas no jogo
grade = [[0] * COLUNAS_GRADE for _ in range(LINHAS_GRADE)]

# Crie um dicionário que mapeia os valores das cartas para as imagens
imagens_cartas = {}
for valor in range(1, LINHAS_GRADE * COLUNAS_GRADE // 2 + 1):
    if valor <= LINHAS_GRADE * COLUNAS_GRADE // 4:
        imagem = pygame.image.load("./assets/uva.jpg")  # Substitua pelo nome da imagem de uva
    else:
        imagem = pygame.image.load(f"./assets/banana.jpg")  # Substitua pelo nome da imagem de banana

    imagem = pygame.transform.scale(imagem, (LARGURA_CARTA, ALTURA_CARTA))
    imagens_cartas[valor] = imagem

# Embaralhe as imagens das cartas
imagens_embaralhadas = list(imagens_cartas.values()) * 2
random.shuffle(imagens_embaralhadas)

# Preencha a matriz de cartas com imagens aleatórias
for linha in range(LINHAS_GRADE):
    for coluna in range(COLUNAS_GRADE):
        imagem = imagens_embaralhadas.pop()
        grade[linha][coluna] = imagem

# Outras variáveis de controle do jogo
cartas_viradas = []  # Armazena as cartas viradas
pares_correspondentes = 0
pode_virar_cartas = True  # Variável para controlar se o jogador pode virar cartas

# Armazene a primeira carta virada
primeira_carta_virada = None

# Loop principal do jogo
executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

    tela.fill((0, 0, 0))

    # Lógica do jogo
    for linha in range(LINHAS_GRADE):
        for coluna in range(COLUNAS_GRADE):
            x = coluna * LARGURA_CARTA
            y = linha * ALTURA_CARTA

            carta = grade[linha][coluna]

            if carta == 0:
                continue

            # Verifica se o mouse está sobre a carta e se o jogador pode virá-la
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (x < mouse_x < x + LARGURA_CARTA and y < mouse_y < y + ALTURA_CARTA) and pode_virar_cartas:
                if pygame.mouse.get_pressed()[0] and len(cartas_viradas) < 2:
                    cartas_viradas.append((linha, coluna))
                    if len(cartas_viradas) == 1:
                        primeira_carta_virada = carta

            # Desenha a carta
            if (linha, coluna) in cartas_viradas:
                tela.blit(carta, (x, y))
            else:
                # Desenha o verso da carta (substitua pela imagem do verso)
                verso_carta = pygame.image.load(f"C:/Users/Eu/Downloads/23163977-branco-suave-sem-falhas-abstrato-fundo-limpar-limpo-simples-e-elegante-movimento-grafico-foto.jpg")  # Substitua pelo verso real
                tela.blit(verso_carta, (x, y))

    # Verifica se duas cartas foram viradas
    if len(cartas_viradas) == 2:
        linha1, coluna1 = cartas_viradas[0]
        linha2, coluna2 = cartas_viradas[1]

        carta1 = grade[linha1][coluna1]
        carta2 = grade[linha2][coluna2]

        if carta1 == carta2:
            # Formou um par, as cartas são removidas
            grade[linha1][coluna1] = 0
            grade[linha2][coluna2] = 0
            pares_correspondentes += 1

        # Aguarde um momento para mostrar as cartas antes de virá-las de volta
        pygame.time.delay(1000)
        cartas_viradas = []

        # Verifique se o jogador pode virar mais cartas
        if pares_correspondentes < LINHAS_GRADE * COLUNAS_GRADE // 2:
            pode_virar_cartas = True
        else:
            pode_virar_cartas = False

    # Mantenha a primeira carta virada aberta até que o jogador selecione a segunda carta
    if len(cartas_viradas) == 1:
        linha, coluna = cartas_viradas[0]
        grade[linha][coluna] = primeira_carta_virada

    # Verifica se o jogo terminou
    if pares_correspondentes == LINHAS_GRADE * COLUNAS_GRADE // 2:
        tela.fill((255, 255, 255))
        texto_fim_de_jogo = pygame.font.Font(None, 48).render("Parabéns! Você ganhou!", True, (0, 0, 0))
        tela.blit(texto_fim_de_jogo, (LARGURA // 2 - 200, ALTURA // 2 - 50))

    pygame.display.flip()
    relogio.tick(FPS)

pygame.quit()
