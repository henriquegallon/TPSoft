import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Partícula:
    def __init__(self, x_emissão, y_emissão, z_emissão, teta, fi):
        self.deposição = 10
        self.velocidade = 3*10**8
        self.x_emissão = x_emissão
        self.y_emissão = y_emissão
        self.z_emissão = z_emissão
        self.teta = teta
        self.fi = fi

    def plotar(self, TPC, ax):
        """Essa função plota a trajetória do Muon."""
        t = np.arange(0, encontrar_limite(self.teta, self.fi, self.x_emissão, self.y_emissão,
                                          self.z_emissão, TPC))
        x = t * np.sin(self.teta) * np.cos(self.fi) + self.x_emissão
        y = t * np.sin(self.teta) * np.sin(self.fi) + self.y_emissão
        z = t * np.cos(self.teta) + self.z_emissão
        ax.plot(x, y, z)

class TPC:
    def __init__(self, comprimento_x, comprimento_y, comprimento_z):
        self.comprimento_x = comprimento_x
        self.comprimento_y = comprimento_y
        self.comprimento_z = comprimento_z
        self.fotons_por_MeV = 10

    def plotar(self, ax):
        """Essa função plota TPCs em forma de paralelepipedos."""
        arrays_definição = [np.array(list(item)) for item in
                            [(0, 0, 0), (0, 0, self.comprimento_z),
                             (self.comprimento_x, 0, 0),
                             (0, self.comprimento_y, 0)]]
        vetores = [arrays_definição[1] - arrays_definição[0],
                   arrays_definição[2] - arrays_definição[0],
                   arrays_definição[3] - arrays_definição[0]]
        vertices = []
        vertices += arrays_definição
        vertices += [arrays_definição[0] + vetores[0] + vetores[1]]
        vertices += [arrays_definição[0] + vetores[0] + vetores[2]]
        vertices += [arrays_definição[0] + vetores[1] + vetores[2]]
        vertices += [arrays_definição[0] + vetores[0] + vetores[1] + vetores[2]]
        vertices = np.array(vertices)
        arestas = [[vertices[0], vertices[3], vertices[5], vertices[1]],
                   [vertices[1], vertices[5], vertices[7], vertices[4]],
                   [vertices[4], vertices[2], vertices[6], vertices[7]],
                   [vertices[2], vertices[6], vertices[3], vertices[0]],
                   [vertices[0], vertices[2], vertices[4], vertices[1]],
                   [vertices[3], vertices[6], vertices[7], vertices[5]]]
        faces = Poly3DCollection(arestas, linewidths=1, edgecolors='k')
        faces.set_facecolor((1, 1, 1, 0.1))
        ax.add_collection3d(faces)
        ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], s=0)
        pass

    def coleção_de_luz(self, Particula, delta, ax, **kwargs):
        """Essa função plota a coleção de fótons em uma parede da TPC na forma de um scatter."""
        x_plano, y_plano, z_plano = 0, 0, 0
        for chave, valor in kwargs.items():
            if chave == 'x':
                x_plano = valor
            elif chave == 'y':
                y_plano = valor
            elif chave == 'z':
                z_plano = valor
        x = Particula.x_emissão
        y = Particula.y_emissão
        z = Particula.z_emissão
        intersecção_plano_x_geral = []
        intersecção_plano_y_geral = []
        intersecção_plano_z_geral = []
        while 0 <= x <= self.comprimento_x and 0 <= y <= self.comprimento_y and 0 <= z <= self.comprimento_z:
            intersecção_plano_x, intersecção_plano_y, intersecção_plano_z = [], [], []
            x_antigo = x
            y_antigo = y
            z_antigo = z
            x += delta * np.sin(Particula.teta) * np.cos(Particula.fi)
            y += delta * np.sin(Particula.teta) * np.sin(Particula.fi)
            z += delta * np.cos(Particula.teta)
            medio = [(x_antigo + x) / 2,
                     (y_antigo + y) / 2,
                     (z_antigo + z) / 2]
            if not 0 <= medio[0] <= self.comprimento_x and 0 <= medio[1] <= self.comprimento_y \
                    and 0 <= medio[2] <= self.comprimento_z:
                break
            qtd_de_fotons = delta * Particula.deposição * self.fotons_por_MeV
            intersecção_limites = intersecção_foton_limites(medio, qtd_de_fotons, self)
            intersecção_plano_x, intersecção_plano_y, intersecção_plano_z = \
                intersecção_foton_plano(intersecção_limites, x_plano, y_plano, z_plano)
            intersecção_plano_x_geral += intersecção_plano_x
            intersecção_plano_y_geral += intersecção_plano_y
            intersecção_plano_z_geral += intersecção_plano_z
        for chave, valor in kwargs.items():
            if chave == 'tipo' and valor == 'Scatter':
                if x_plano == 0 and y_plano == 0:
                    ax.scatter(intersecção_plano_x_geral, intersecção_plano_y_geral, s=0.1)
                elif x_plano == 0 and z_plano == 0:
                    ax.scatter(intersecção_plano_x_geral, intersecção_plano_z_geral, s=0.1)
                elif y_plano == 0 and z_plano == 0:
                    ax.scatter(intersecção_plano_y_geral, intersecção_plano_z_geral, s=0.1)
            elif chave == 'tipo' and valor == 'Hist':
                if x_plano == 0 and y_plano == 0:
                    ax.hist2d(intersecção_plano_x_geral, intersecção_plano_y_geral, bins=100)
                elif x_plano == 0 and z_plano == 0:
                    ax.hist2d(intersecção_plano_x_geral, intersecção_plano_z_geral, bins=100)
                elif y_plano == 0 and z_plano == 0:
                    ax.hist2d(intersecção_plano_y_geral, intersecção_plano_z_geral, bins=100)

def encontrar_limite(teta, fi, x_emissão, y_emissão, z_emissão, TPC):
    """"Essa função resolve aquele problema da parametrização da trajetória.
    Em qual t o Muon intercepta alguma parede?"""
    limites = [(TPC.comprimento_x - x_emissão) / (np.sin(teta) * np.cos(fi)),
               (TPC.comprimento_y - y_emissão) / (np.sin(teta) * np.sin(fi)),
               (TPC.comprimento_z - z_emissão) / (np.cos(teta)),
               (- x_emissão) / (np.sin(teta) * np.cos(fi)),
               (- y_emissão) / (np.sin(teta) * np.sin(fi)),
               (- z_emissão) / (np.cos(teta))]
    pontos_limites = [[limites[0] * np.sin(teta) * np.cos(fi) + x_emissão,
                       limites[0] * np.sin(teta) * np.sin(fi) + y_emissão,
                       limites[0] * np.cos(teta) + z_emissão],
                      [limites[1] * np.sin(teta) * np.cos(fi) + x_emissão,
                       limites[1] * np.sin(teta) * np.sin(fi) + y_emissão,
                       limites[1] * np.cos(teta) + z_emissão],
                      [limites[2] * np.sin(teta) * np.cos(fi) + x_emissão,
                       limites[2] * np.sin(teta) * np.sin(fi) + y_emissão,
                       limites[2] * np.cos(teta) + z_emissão],
                      [limites[3] * np.sin(teta) * np.cos(fi) + x_emissão,
                       limites[3] * np.sin(teta) * np.sin(fi) + y_emissão,
                       limites[3] * np.cos(teta) + z_emissão],
                      [limites[4] * np.sin(teta) * np.cos(fi) + x_emissão,
                       limites[4] * np.sin(teta) * np.sin(fi) + y_emissão,
                       limites[4] * np.cos(teta) + z_emissão],
                      [limites[5] * np.sin(teta) * np.cos(fi) + x_emissão,
                       limites[5] * np.sin(teta) * np.sin(fi) + y_emissão,
                       limites[5] * np.cos(teta) + z_emissão]]
    lista = []
    for i in range(6):
        if i in [0, 3] and 0 <= pontos_limites[i][1] <= TPC.comprimento_y \
                and 0 <= pontos_limites[i][2] <= TPC.comprimento_z:
            lista += [i]
        elif i in [1, 4] and 0 <= pontos_limites[i][0] <= TPC.comprimento_x \
                and 0 <= pontos_limites[i][2] <= TPC.comprimento_z:
            lista += [i]
        elif i in [2, 5] and 0 <= pontos_limites[i][0] <= TPC.comprimento_x \
                and 0 <= pontos_limites[i][1] <= TPC.comprimento_y:
            lista += [i]
    vetor_diretor = [np.sin(teta) * np.cos(fi),
                     np.sin(teta) * np.sin(fi),
                     np.cos(teta)]
    vetor_diretor_norm = vetor_diretor / np.linalg.norm(vetor_diretor)
    try:
        direções_possíveis = [[limites[lista[0]] * np.sin(teta) * np.cos(fi),
                               limites[lista[0]] * np.sin(teta) * np.sin(fi),
                               limites[lista[0]] * np.cos(teta)],
                              [limites[lista[1]] * np.sin(teta) * np.cos(fi),
                               limites[lista[1]] * np.sin(teta) * np.sin(fi),
                               limites[lista[1]] * np.cos(teta)]]
        if np.inner(vetor_diretor_norm, direções_possíveis[0]) > 0:
            t = limites[lista[0]]
        else:
            t = limites[lista[1]]
        return abs(t)
    except:
        return 0


def intersecção_foton_limites(ponto, quantidade, TPC):
    """Essa função calcula os pontos em que os fótons cruzam com alguma parede da TPC, dado um ponto de emissão
    e a quantidade de fótons saindo desse ponto."""
    intersecção_limites = []
    for i in range(int(quantidade)):
        teta_fi = np.random.uniform([0,0],[np.pi,np.pi*2],size=2)
        t = encontrar_limite(teta_fi[0], teta_fi[1], ponto[0],ponto[1],ponto[2], TPC)
        intersecção_limites += [[(t*np.sin(teta_fi[0])*np.cos(teta_fi[1])) + ponto[0],
                                 (t*np.sin(teta_fi[0])*np.sin(teta_fi[1])) + ponto[1],
                                 (t*np.cos(teta_fi[0])) + ponto[2]]]
    return intersecção_limites


def intersecção_foton_plano(intersecção_limites, x_plano, y_plano, z_plano):
    """Essa função escolhe apenas as intersecções de fótons com a parede de interesse."""
    intersecção_plano_x = []
    intersecção_plano_y = []
    intersecção_plano_z = []
    for i in range(len(intersecção_limites)):
        if x_plano != 0 and round(intersecção_limites[i][0]) == x_plano:
            intersecção_plano_x += [intersecção_limites[i][0]]
            intersecção_plano_y += [intersecção_limites[i][1]]
            intersecção_plano_z += [intersecção_limites[i][2]]
        elif y_plano != 0 and round(intersecção_limites[i][1]) == y_plano:
            intersecção_plano_x += [intersecção_limites[i][0]]
            intersecção_plano_y += [intersecção_limites[i][1]]
            intersecção_plano_z += [intersecção_limites[i][2]]
        elif z_plano != 0 and round(intersecção_limites[i][2]) == z_plano:
            intersecção_plano_x += [intersecção_limites[i][0]]
            intersecção_plano_y += [intersecção_limites[i][1]]
            intersecção_plano_z += [intersecção_limites[i][2]]
    return intersecção_plano_x, intersecção_plano_y, intersecção_plano_z
