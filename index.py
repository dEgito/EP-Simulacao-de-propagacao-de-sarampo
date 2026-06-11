import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap
from matplotlib import animation


n = 20                       # tamanho da grade (NxN)
beta = 0.4                   # probabilidade de transmissão por vizinho infectado
gama = 0.125                 # probabilidade de recuperação (1/8 dias)
iteracoes = 200

S, I, R = 0, 1, 2

movimentos = [
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1)
]

# geração da grade NxN

grade = np.zeros((n, n), dtype=int)

# infectado numa posição aleatória
linha = np.random.randint(0, n)
coluna = np.random.randint(0, n)
grade[linha, coluna] = I

# contagem de infectados

def contar_infectados(grade, i, j):
    contagem = 0
    for di, dj in movimentos:
        ni, nj = i + di, j + dj
        if 0 <= ni < n and 0 <= nj < n:
            if grade[ni, nj] == I:
                contagem += 1
    return contagem

# registro do histórico

historico_S = []
historico_I = []
historico_R = []
historico_grades = []

total_infectados = 0
historico_total_infectados = []
individuos_infectados = set()
historico_individuos_unicos = []

# loop de iterações e transições de estados

for t in range(iteracoes):
    nova_grade = grade.copy()

    for i in range(n):
        for j in range(n):
            estado = grade[i, j]

            # Regra S -> I (suscetível -> infectado)
            if estado == S:
                k = contar_infectados(grade, i, j)
                prob = 1 - (1 - beta) ** k
                if np.random.random() < prob:
                    nova_grade[i, j] = I

            # Regra I -> R (infectado -> recuperado)
            # período infeccioso médio de 8 dias → γ = 0.125
            elif estado == I:
                if np.random.random() < gama:
                    nova_grade[i, j] = R

            # R permanece R (sarampo confere imunidade permanente)

    grade_anterior = grade.copy()
    grade = nova_grade
    historico_grades.append(grade.copy())

    # contagem de infecções totais
    novos_infectados = np.sum((grade == I) & (grade_anterior == S))
    total_infectados += novos_infectados
    historico_total_infectados.append(total_infectados / (n * n))

    # contagem de indivíduos únicos
    for i in range(n):
        for j in range(n):
            if grade[i, j] == I and grade_anterior[i, j] == S:
                individuos_infectados.add((i, j))
    historico_individuos_unicos.append(len(individuos_infectados) / (n * n))

    total = n * n
    historico_S.append(np.sum(grade == S) / total)
    historico_I.append(np.sum(grade == I) / total)
    historico_R.append(np.sum(grade == R) / total)

    if np.sum(grade == I) == 0:
        print(f"Epidemia encerrada na {t + 1}ª iteração.")
        break


print("Última iteração:")
print(f"Saudáveis: {historico_S[-1]*100:.1f}%")
print(f"Infectados: {historico_I[-1]*100:.1f}%")
print(f"Recuperados: {historico_R[-1]*100:.1f}%")

pico_t = int(np.argmax(historico_I))
taxa_reproducao = beta / gama

print(f"\nR₀ = β/γ = {taxa_reproducao:.2f}")
print(f"Pico de infectados: {historico_I[pico_t]*100:.1f}% na {pico_t}ª iteração")
print(f"Taxa de ataque final: {historico_R[-1]*100:.1f}% da população")
print(f"Total de infecções ao longo da epidemia: {historico_total_infectados[-1]*100:.1f}% da população")
print(f"Indivíduos únicos infectados: {historico_individuos_unicos[-1]*100:.1f}% da população")


# visualização

cmap = ListedColormap(['steelblue', 'tomato', 'seagreen'])

plt.figure(figsize=(6, 6))
plt.imshow(historico_grades[-1], cmap=cmap, vmin=0, vmax=2)
plt.title(f"Sarampo — estado final (β={beta}, γ={gama}, R₀={taxa_reproducao:.1f})")
plt.axis('off')
cbar = plt.colorbar(ticks=[0, 1, 2], shrink=0.7)
cbar.ax.set_yticklabels(['Suscetível', 'Infectado', 'Recuperado'])
plt.tight_layout()
plt.show()


n_passos = len(historico_grades)
instantes = {
    "Início (t=0)": 0,
    f"Pico (t={pico_t})": pico_t,
    f"Final (t={n_passos-1})": n_passos - 1,
}

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
for ax, (titulo, t) in zip(axes, instantes.items()):
    ax.imshow(historico_grades[t], cmap=cmap, vmin=0, vmax=2)
    ax.set_title(titulo)
    ax.axis('off')
fig.suptitle(f"Propagação do Sarampo — β={beta}, γ={gama}, R₀={taxa_reproducao:.1f}", fontsize=13)
plt.tight_layout()
plt.show()


plt.figure(figsize=(9, 5))
plt.plot(historico_S, label='Suscetíveis (S)', color='steelblue')
plt.plot(historico_I, label='Infectados (I)',  color='tomato')
plt.plot(historico_R, label='Recuperados (R)', color='seagreen')
plt.axvline(pico_t, color='tomato', linestyle='--', alpha=0.5, label=f'Pico (t={pico_t})')
plt.xlabel("Passo temporal (dias)")
plt.ylabel("Proporção da população")
plt.title(f"Evolução do Sarampo — β={beta}, γ={gama}, R₀={taxa_reproducao:.1f}")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


betas = [0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50]
gama_fixo = gama
resultados = []

print("\nAnálise paramétrica — Sarampo (γ fixo = {:.3f}):".format(gama_fixo))
print(f"{'β':>6}  {'R₀':>6}  {'Pico I (%)':>10}  {'Ataque final (%)':>16}")

for b in betas:
    g_tmp = np.zeros((n, n), dtype=int)
    g_tmp[n // 2, n // 2] = I
    hist_i = []

    for _ in range(iteracoes):
        nova = g_tmp.copy()
        infectados_mapa = (g_tmp == I).astype(np.int8)

        viz_I = sum(
            np.roll(np.roll(infectados_mapa, dr, axis=0), dc, axis=1)
            for dr in (-1, 0, 1) for dc in (-1, 0, 1)
            if not (dr == 0 and dc == 0)
        )

        mask_S = g_tmp == S
        prob = 1 - (1 - b) ** viz_I
        nova[mask_S] = np.where(np.random.random((n, n))[mask_S] < prob[mask_S], I, S)

        mask_I = g_tmp == I
        nova[mask_I] = np.where(np.random.random((n, n))[mask_I] < gama_fixo, R, I)

        g_tmp = nova
        hist_i.append(np.sum(g_tmp == I) / (n * n))
        if np.sum(g_tmp == I) == 0:
            break

    pico = max(hist_i) * 100
    ataque = np.sum(g_tmp == R) / (n * n) * 100
    R0_val = b / gama_fixo
    resultados.append((b, R0_val, hist_i, pico, ataque))
    print(f"{b:>6.2f}  {R0_val:>6.2f}  {pico:>10.1f}  {ataque:>16.1f}")

plt.figure(figsize=(9, 5))
for b, R0_val, hist_i, pico, ataque in resultados:
    plt.plot(hist_i, label=f"β={b:.2f}  R₀={R0_val:.1f}")
plt.axhline(0, color='gray', linewidth=0.5)
plt.xlabel("Passo temporal (dias)")
plt.ylabel("Proporção de infectados I(t)")
plt.title(f"Sarampo — análise paramétrica (γ={gama_fixo})")
plt.legend(fontsize=8)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


# animação

fig, ax = plt.subplots(figsize=(6, 6))
img = ax.imshow(historico_grades[0], cmap=cmap, vmin=0, vmax=2)
ponto_inicial = ax.plot(coluna, linha, 'o', color='yellow', markersize=8)[0]
ax.axis('off')
titulo = ax.set_title("Dia 0")

def atualizar(frame):
    img.set_array(historico_grades[frame])
    titulo.set_text(f"Dia {frame}  |  I={historico_I[frame]*100:.1f}%")
    return img, titulo, ponto_inicial

ani = animation.FuncAnimation(
    fig,
    atualizar,
    frames=len(historico_grades),
    interval=80,
    repeat=False
)

plt.tight_layout()
plt.show()