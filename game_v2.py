import pygame
import random
import time

pygame.init()

# Configurações do jogo
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo da Memória')

BRANCO = (255,255,255)
PRETO = (0,0,0)
LARANJA = (246,130,0)
VERMELHO = (230,0,0)
AZUL = (0,0,255)
CINZA = (200, 200, 200)

tempo_inicial = time.time()
tempo_limite = 60

cartas = [1, 2, 3, 4, 5, 6, 7, 8] * 2
random.shuffle(cartas)
cartas_viradas = []
cartas_correspondentes = []
pontos = 0

verso_carta = pygame.image.load("./assets/imgs/verso_carta.jpg")
verso_carta = pygame.transform.scale(verso_carta, (100, 100))
frente_cartas = [pygame.image.load(f"./assets/imgs/frente_carta_{i}.jpg") for i in range(1, 9)]
frente_cartas = [pygame.transform.scale(img, (100, 100)) for img in frente_cartas]

posicoes_cartas = [(x, y) for x in range(4) for y in range(4)]
random.shuffle(posicoes_cartas)

fonte = pygame.font.Font(None, 36)

def mostrar_mensagem_vitoria():
    tela.fill((255, 255, 255))
    texto = fonte.render("Parabéns, você ganhou!", True, (0, 0, 255))
    tela.blit(texto, (200, 250))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()

def mostrar_mensagem_derrota():
    tela.fill((255, 255, 255))
    texto = fonte.render("Você perdeu. Tente novamente!", True, (255, 0, 0))
    tela.blit(texto, (200, 250))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()

virando_carta = False
tempo_final = 0
tempo_viragem = 0

executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for i, (pos_x, pos_y) in enumerate(posicoes_cartas):
                if 50 + 100 * pos_x < x < 50 + 100 * (pos_x + 1) and 50 + 100 * pos_y < y < 50 + 100 * (pos_y + 1):
                    if i not in cartas_viradas and len(cartas_viradas) < 2:
                        cartas_viradas.append(i)

    tela.fill((255, 255, 255))

    texto_titulo = fonte.render("Jogo da Memória", True, LARANJA)
    tela.blit(texto_titulo, (200, 10))

    for i in range(len(cartas_viradas)):
        carta = cartas[cartas_viradas[i]]
        x, y = posicoes_cartas[cartas_viradas[i]]
        tela.blit(frente_cartas[carta - 1], (50 + 100 * x, 50 + 100 * y))

    if len(cartas_viradas) == 2:
        carta1, carta2 = cartas[cartas_viradas[0]], cartas[cartas_viradas[1]]
        if carta1 == carta2:
            pontos += 1
            cartas_correspondentes.extend(cartas_viradas)
            cartas_viradas = []
        else:
            virando_carta = True

    texto_pontos = fonte.render("Pontos: " + str(pontos), True, AZUL)
    tela.blit(texto_pontos, (200, 500))

    if virando_carta:
        tempo_viragem += 1
        if tempo_viragem == 800:
            cartas_viradas = []
            virando_carta = False
            tempo_viragem = 0

    for i in range(16):
        if i not in cartas_viradas and i not in cartas_correspondentes:
            x, y = posicoes_cartas[i]
            tela.blit(verso_carta, (50 + 100 * x, 50 + 100 * y))

    if pontos == len(cartas)/2:
        tempo_final = time.time()
        mostrar_mensagem_vitoria()

    if tempo_limite - int(time.time() - tempo_inicial) <= 0:
        mostrar_mensagem_derrota()

    tempo_restante = tempo_limite - int(time.time() - tempo_inicial)
    texto_tempo = fonte.render("Tempo: " + str(tempo_restante), True, PRETO)
    tela.blit(texto_tempo, (20, 500))

    pygame.display.flip()

pygame.display.quit()
pygame.quit()