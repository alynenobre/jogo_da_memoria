import pygame
import random
import time
import pickle
import socket


def tela_selecao_dificuldade():
    tela.fill((255, 255, 255))

    texto_titulo = fonte.render("Escolha o Nível de Dificuldade", True, LARANJA)
    tela.blit(texto_titulo, (150, 100))

    botoes = [
        {"texto": "Nível 1", "nivel": 4},
        {"texto": "Nível 2", "nivel": 6},
        {"texto": "Nível 3", "nivel": 8},
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