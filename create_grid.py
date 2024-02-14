import matplotlib.pyplot as plt
import numpy as np

def criar_grid(altura, comprimento):
    # Verifica se altura e comprimento são números positivos
    if altura <= 0 or comprimento <= 0:
        print("A altura e o comprimento devem ser números positivos.")
        return None

    # Cria a grid preenchida com "-"
    grid = [['-' for _ in range(comprimento)] for _ in range(altura)]
    
    return grid

def aplicar_grid_lido(principal_grid, lido_txt, posicao_x, posicao_y):
    if not principal_grid or not lido_txt or posicao_x < 0 or posicao_y < 0:
        print("Argumentos inválidos.")
        return None

    altura_grid, comprimento_grid = len(principal_grid), len(principal_grid[0])
    altura_lido, comprimento_lido = len(lido_txt), len(lido_txt[0].split())

    # Verifica se as posições são válidas
    if posicao_x + comprimento_lido > comprimento_grid or posicao_y + altura_lido > altura_grid:
        print("Posição inicial inválida para o tamanho de lido_txt.")
        return None

    for i in range(altura_lido):
        valores = lido_txt[altura_lido - 1 - i].split()  # Inverte o lido_txt
        # Calcula a posição y invertida
        pos_y = posicao_y + i
        for j in range(comprimento_lido):
            if pos_y < altura_grid and posicao_x + j < comprimento_grid:
                principal_grid[altura_grid - pos_y - 1][posicao_x + j] = valores[j]

    return principal_grid


def ler_grid_do_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            # Lê as linhas do arquivo
            linhas = arquivo.readlines()

            # Remove quebras de linha
            linhas = [linha.strip() for linha in linhas]

            return linhas
    except FileNotFoundError:
        print(f"O arquivo '{nome_arquivo}' não foi encontrado.")
        return None


def plotar_grid(grid):
    # Mapeia os valores para as cores
    cmap = {'-': 0, '0': 1, '1': 2, '2': 3, '3': 4}

    # Obtém o número máximo de colunas em qualquer linha
    max_colunas = max(len(linha) for linha in grid)

    # Preenche as linhas para ter o mesmo comprimento máximo
    grid_preenchido = [linha + ['-'] * (max_colunas - len(linha)) for linha in grid]

    # Substitui espaços duplos por '-'
    grid_preenchido = [['-' if cell == '  ' else cell for cell in linha] for linha in grid_preenchido]

    # Converte o grid para uma matriz numpy de inteiros
    matriz_grid = np.array([[cmap.get(i, 0) for i in linha] for linha in grid_preenchido], dtype=int)

    # Cria um gráfico
    plt.imshow(matriz_grid, cmap='viridis', interpolation='none', vmin=0, vmax=3)

    # Adiciona os valores dentro de cada quadrado
    for i in range(len(grid_preenchido)):
        for j in range(len(grid_preenchido[i])):
            if grid_preenchido[i][j] != '-':
                plt.annotate(grid_preenchido[i][j], xy=(j, i), ha='center', va='center', color='white')

    # Adiciona a legenda de cores
    legend_labels = {'0': 'Preto', '1': 'Vermelho', '2': 'Amarelo', '3': 'Azul'}
    handles = [plt.Rectangle((0, 0), 1, 1, color=plt.cm.viridis(cmap[i]/3) if i != '-' else 'black', label=legend_labels.get(i, '')) for i in cmap]
    #plt.legend(handles=handles, title="Legend", loc="upper left")

    # Esconde os eixos
    plt.axis('off')

    # Exibe o gráfico
    plt.show()

# Exemplo de uso
altura = 15
comprimento = 15
posicao_x = 0
posicao_y = 0

principal_grid = criar_grid(altura, comprimento)

for _ in principal_grid:
    print(_)

lido_txt = ler_grid_do_arquivo('./grid_text.txt')

# Aplica o grid lido na posição especificada
resultado_grid = aplicar_grid_lido(principal_grid, lido_txt, posicao_x, posicao_y)

print(resultado_grid)

# Exibindo a grid resultante
if resultado_grid is not None:
    for linha in resultado_grid:
        print(' '.join(map(str, linha)))

    plotar_grid(resultado_grid)
else:
    print("Operação inválida.")
