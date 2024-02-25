import pygame
import random
import time
import pickle
import socket
import game_nivel_1
import game_nivel_2
import game_v2


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
fonte = pygame.font.Font(None, 36)

def enviar_dados(client_socket, dados):
    serialized_data = pickle.dumps(dados)
    client_socket.send(serialized_data)

def receber_dados(client_socket):
    serialized_data = client_socket.recv(1024)
    dados = pickle.loads(serialized_data)
    return dados

def tela_selecao_dificuldade():
    tela.fill((255, 255, 255))

    texto_titulo = fonte.render("Escolha o Nível de Dificuldade", True, LARANJA)
    tela.blit(texto_titulo, (150, 100))

    botoes = [
        {"texto": "Nível 1", "nivel": 4},
        {"texto": "Nível 2", "nivel": 6},
        {"texto": "Nível 3", "nivel": 16},
    ]

    botoes_rect = []
    for i, botao in enumerate(botoes):
        texto_botao = fonte.render(botao["texto"], True, PRETO)
        largura_texto, altura_texto = texto_botao.get_size()
        p_x = largura // 2 - largura_texto // 2
        p_y = 250 + i * 60
        tela.blit(texto_botao, (p_x, p_y))
        botao_rect = pygame.Rect(p_x, p_y, largura_texto, altura_texto)
        botoes_rect.append(botao_rect)

    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for i, botao_rect in enumerate(botoes_rect):
                    if botao_rect.collidepoint(x, y):
                        return botoes[i]["nivel"]


def obter_nome_cliente():
    tela.fill((255, 255, 255))

    texto_titulo = fonte.render("Digite seu nome:", True, LARANJA)
    tela.blit(texto_titulo, (300, 200))

    nome_input = ""
    pygame.draw.rect(tela, PRETO, (250, 300, 300, 40))
    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return nome_input

                elif evento.key == pygame.K_BACKSPACE:
                    nome_input = nome_input[:-1]

                else:
                    nome_input += evento.unicode

                pygame.draw.rect(tela, PRETO, (250, 300, 300, 40))
                texto_nome = fonte.render(nome_input, True, BRANCO)
                tela.blit(texto_nome, (260, 310))
                pygame.display.flip()

def tela_selecao_adversario(client_socket):
    nome_cliente = obter_nome_cliente()
    enviar_dados(client_socket, nome_cliente)

    tela.fill((255, 255, 255))

    texto_titulo = fonte.render("Escolha seu Adversário", True, LARANJA)
    tela.blit(texto_titulo, (150, 100))

    # Solicitar e receber a lista de clientes do servidor
    enviar_dados(client_socket, "LISTA_CLIENTES")
    lista_clientes = receber_dados(client_socket)

    botoes = [
        {"texto": "Jogar contra a Máquina", "cliente": None},
        {"texto": "Jogar Sozinho", "cliente": None},
    ] + [{"texto": nome, "cliente": nome} for nome in lista_clientes]

    botoes_rect = []
    for i, botao in enumerate(botoes):
        texto_botao = fonte.render(botao["texto"], True, PRETO)
        largura_texto, altura_texto = texto_botao.get_size()
        pos_x = largura // 2 - largura_texto // 2
        pos_y = 250 + i * 60
        tela.blit(texto_botao, (pos_x, pos_y))
        botao_rect = pygame.Rect(pos_x, pos_y, largura_texto, altura_texto)
        botoes_rect.append((botao_rect, botao["cliente"]))

    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for botao_rect, adversario_cliente in botoes_rect:
                    if botao_rect.collidepoint(x, y):
                        return nome_cliente , adversario_cliente


def main():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    nome_cliente, adversario_cliente = tela_selecao_adversario(client_socket)


    nivel_dificuldade = tela_selecao_dificuldade()

    if nivel_dificuldade == 4:
        game_nivel_1.main(client_socket, nome_cliente)
    elif nivel_dificuldade == 6:
        game_nivel_2.main(client_socket, nome_cliente)
    elif nivel_dificuldade == 16:
        game_v2.main(client_socket, nome_cliente)

    pygame.display.quit()
    pygame.quit()

if __name__ == "__main__":
    main()