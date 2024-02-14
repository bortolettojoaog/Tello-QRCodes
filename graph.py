import matplotlib.pyplot as plt

# Dados dos pontos fornecidos
timestamps = [
    "18:49:49.909", "18:49:50.660", "18:49:52.162", "18:49:52.917",
    "18:49:54.418", "18:49:55.170", "18:49:56.674", "18:49:57.425",
    "18:50:01.182", "18:50:01.933", "18:50:03.436", "18:50:04.189",
    "18:50:05.692", "18:50:06.443", "18:50:07.945", "18:50:08.697",
    "18:50:10.201", "18:50:10.952", "18:50:12.453", "18:50:13.205",
    "18:50:14.706", "18:50:15.460", "18:50:16.453", "18:50:17.205"
]
positions = [
    (0, 1), (0, 1), (0, 2), (0, 2), (1, 2), (1, 2), (2, 2), (2, 2),
    (3, 2), (3, 2), (4, 2), (4, 2), (4, 3), (4, 3), (4, 4), (4, 4),
    (4, 5), (4, 5), (4, 6), (4, 6), (4, 7), (4, 7), (3, 7), (3, 7)
]

# Preparação dos dados para o gráfico
x = [pos[0] for pos in positions]
y = [pos[1] for pos in positions]

# Criação do callback para exibir texto ao passar o mouse sobre os pontos
def hover(event):
    for point in ax.collections:
        cont, ind = point.contains(event)
        if cont:
            index = ind["ind"][0]
            text.set_text(timestamps[index])
            text.set_position((x[index]+0.1, y[index]+0.1))
            text.set_visible(True)
            fig.canvas.draw_idle()
            return
    text.set_visible(False)
    fig.canvas.draw_idle()

# Criação do gráfico
fig, ax = plt.subplots()
ax.scatter(x, y, color='blue')  # Pontos no grid
ax.plot(x, y, color='red', linestyle='--')  # Linhas conectando os pontos
ax.set_xlim(-0.5, 14.5)  # Limites do eixo x (grid 15x15)
ax.set_ylim(-0.5, 14.5)  # Limites do eixo y (grid 15x15)
ax.set_aspect('equal')  # Mesma escala em ambos os eixos
ax.set_title("Posições do Drone Durante Percurso")  # Título do gráfico

# Criação do texto do timestamp
text = ax.text(0, 0, '', visible=False)

# Conectando evento de hover ao gráfico
fig.canvas.mpl_connect("motion_notify_event", hover)

# Exibição do gráfico
plt.show()