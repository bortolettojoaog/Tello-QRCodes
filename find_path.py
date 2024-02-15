from create_grid import *

def clean_grid(grid):
    cleaned_grid = []
    for row in grid:
        cleaned_row = [cell for cell in row if cell != '-' and cell != []]
        if cleaned_row:  # Verifica se a linha não está vazia
            cleaned_grid.append(cleaned_row)
    return cleaned_grid

def percorrer_tabuleiro(grid):
    def is_valid(x, y, rows, cols):
        return 0 <= x < rows and 0 <= y < cols

    def find_starting_point():
        nonlocal grid, rows, cols
        for i in range(rows - 1, -1, -1):  # Começa da última linha e vai até a primeira
            for j in range(cols):
                if grid[i][j] == 3:
                    return i, j
        return None, None

    def find_path(x, y):
        nonlocal grid, rows, cols
        if not is_valid(x, y, rows, cols) or grid[x][y] == 0:
            return []

        current_path = [(x, y)]
        grid[x][y] = 0  # Marcando a célula como visitada

        # Verificando todas as direções
        directions = [(0, 1, 'direita'), (1, 0, 'baixo'), (0, -1, 'esquerda'), (-1, 0, 'cima')]
        for dx, dy, move in directions:
            next_x, next_y = x + dx, y + dy
            path = find_path(next_x, next_y)
            if path:
                current_path.extend([(move)] + path)
                break

        return current_path

    rows, cols = len(grid), len(grid[0])

    start_x, start_y = find_starting_point()

    if start_x is not None and start_y is not None:
        path = find_path(start_x, start_y)
        return path
    else:
        return None

# Recolhendo Mapa completo com Prateleira
grid_exemplo = resultado_grid

grid_cleanned = clean_grid(grid_exemplo)

grid_integer = [
    [int(cell) for cell in row]  # Convertendo cada elemento da linha para inteiro
    for row in grid_cleanned  # Iterando sobre cada linha da grade
]

for _ in grid_integer:
    print(_)

movimentos = percorrer_tabuleiro(grid_integer)

final_dirs = []
final_xy = []

if movimentos is not None:
    for movimento in movimentos:
        if (movimento == 'direita' or movimento == 'esquerda' or movimento == 'cima' or movimento == 'baixo'):
            final_dirs.append(movimento)
        else:
            final_xy.append(movimento)
else:
    print("Não foi possível encontrar um caminho.")

print(final_dirs)
print(final_xy)
