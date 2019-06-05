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
        x_plano, y_plano, z_plano = np.e, np.e, np.e
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
                if x_plano == np.e and y_plano == np.e:
                    ax.scatter(intersecção_plano_x_geral, intersecção_plano_y_geral, s=0.1)
                elif x_plano == np.e  and z_plano == np.e:
                    ax.scatter(intersecção_plano_x_geral, intersecção_plano_z_geral, s=0.1)
                elif y_plano == np.e and z_plano == np.e:
                    ax.scatter(intersecção_plano_y_geral, intersecção_plano_z_geral, s=0.1)
            elif chave == 'tipo' and valor == 'Hist':
                if x_plano == np.e and y_plano == np.e:
                    ax.hist2d(intersecção_plano_x_geral, intersecção_plano_y_geral, bins=100)
                elif x_plano == np.e and z_plano == np.e:
                    ax.hist2d(intersecção_plano_x_geral, intersecção_plano_z_geral, bins=100)
                elif y_plano == np.e and z_plano == np.e:
                    ax.hist2d(intersecção_plano_y_geral, intersecção_plano_z_geral, bins=100)


def encontrar_limite(teta, fi, x_emissão, y_emissão, z_emissão, TPC):
    """"Essa função resolve aquele problema da parametrização da trajetória.
    Em qual t o Muon intercepta alguma parede?"""
    limites_x_y_z = [(TPC.comprimento_x - x_emissão) / (np.sin(teta) * np.cos(fi)),
                     (TPC.comprimento_y - y_emissão) / (np.sin(teta) * np.sin(fi)),
                     (TPC.comprimento_z - z_emissão) / (np.cos(teta)),
                     (- x_emissão) / (np.sin(teta) * np.cos(fi)),
                     (- y_emissão) / (np.sin(teta) * np.sin(fi)),
                     (- z_emissão) / (np.cos(teta))]
    fis = [np.arctan((TPC.comprimento_y - y_emissão)/(TPC.comprimento_x - x_emissão)),
           np.pi - np.arctan((TPC.comprimento_y - y_emissão)/ (x_emissão)),
           np.pi + np.arctan((y_emissão)/(x_emissão)),
           2*np.pi - np.arctan((y_emissão)/(TPC.comprimento_x - x_emissão))]
    limites_escolhidos = []
    if teta < np.pi/2:
        #Partícula para "cima"
        if fi < fis[0] or fi >= fis[3]:
            #Partícula cruza x_tpc
            limites_escolhidos = [limites_x_y_z[2],limites_x_y_z[0]]
        elif fis[0] <= fi < fis[1]:
            #Partícula cruza y_tpc
            limites_escolhidos = [limites_x_y_z[2],limites_x_y_z[1]]
        elif fis[1] <= fi < fis[2]:
            #Partícula cruza x_zero
            limites_escolhidos = [limites_x_y_z[2],limites_x_y_z[3]]
        elif fis[2] <= fi < fis[3]:
            #Partícula cruza y_zero
            limites_escolhidos = [limites_x_y_z[2],limites_x_y_z[4]]
    elif teta > np.pi/2:
        #Partícula para "baixo"
        if fi < fis[0] or fi >= fis[3]:
            #Partícula cruza x_tpc
            limites_escolhidos = [limites_x_y_z[5],limites_x_y_z[0]]
        elif fis[0] <= fi < fis[1]:
            #Partícula cruza y_tpc
            limites_escolhidos = [limites_x_y_z[5],limites_x_y_z[1]]
        elif fis[1] <= fi < fis[2]:
            #Partícula cruza x_zero
            limites_escolhidos = [limites_x_y_z[5],limites_x_y_z[3]]
        elif fis[2] <= fi < fis[3]:
            #Partícula cruza y_zero
            limites_escolhidos = [limites_x_y_z[5],limites_x_y_z[4]]
    else:
        #Partícula paralela à z
        if fi < fis[0] or fi >= fis[3]:
            #Partícula cruza x_tpc
            limites_escolhidos = [limites_x_y_z[0]]
        elif fis[0] <= fi < fis[1]:
            #Partícula cruza y_tpc
            limites_escolhidos = [limites_x_y_z[1]]
        elif fis[1] <= fi < fis[2]:
            #Partícula cruza x_zero
            limites_escolhidos = [limites_x_y_z[3]]
        elif fis[2] <= fi < fis[3]:
            #Partícula cruza y_zero
            limites_escolhidos = [limites_x_y_z[4]]
    limites_escolhidos.sort()
    if limites_escolhidos[0] > 10**10:
        return 0
    else:
        return limites_escolhidos[0]


def intersecção_foton_limites(ponto, quantidade, TPC):
    """Essa função calcula os pontos em que os fótons cruzam com alguma parede da TPC, dado um ponto de emissão
    e a quantidade de fótons saindo desse ponto."""
    intersecção_limites = []
    for i in range(int(quantidade)):
        x_limite, y_limite, z_limite = 0, 0, 0
        teta = np.random.random()*np.pi
        fi = np.random.random()*2*np.pi
        t = encontrar_limite(teta, fi, ponto[0], ponto[1], ponto[2], TPC)
        x_limite = (t*np.sin(teta)*np.cos(fi)) + ponto[0]
        y_limite = (t*np.sin(teta)*np.sin(fi)) + ponto[1]
        z_limite = (t*np.cos(teta)) + ponto[2]
        if abs(x_limite) < 10**(-10):
            intersecção_limites += [[0, y_limite, z_limite]]
        elif abs(y_limite) < 10**(-10):
            intersecção_limites += [[x_limite, 0, z_limite]]
        elif abs(z_limite) < 10**(-10):
            intersecção_limites += [[x_limite, y_limite, 0]]
        else:
            intersecção_limites += [[x_limite, y_limite, z_limite]]
    return intersecção_limites


def intersecção_foton_plano(intersecção_limites, x_plano, y_plano, z_plano):
    """Essa função escolhe apenas as intersecções de fótons com a parede de interesse."""
    intersecção_plano_x = []
    intersecção_plano_y = []
    intersecção_plano_z = []
    for i in range(len(intersecção_limites)):
        if x_plano != np.e and round(intersecção_limites[i][0]) == x_plano:
            intersecção_plano_x += [intersecção_limites[i][0]]
            intersecção_plano_y += [intersecção_limites[i][1]]
            intersecção_plano_z += [intersecção_limites[i][2]]
        elif y_plano != np.e and round(intersecção_limites[i][1]) == y_plano:
            intersecção_plano_x += [intersecção_limites[i][0]]
            intersecção_plano_y += [intersecção_limites[i][1]]
            intersecção_plano_z += [intersecção_limites[i][2]]
        elif z_plano != np.e and round(intersecção_limites[i][2]) == z_plano:
            intersecção_plano_x += [intersecção_limites[i][0]]
            intersecção_plano_y += [intersecção_limites[i][1]]
            intersecção_plano_z += [intersecção_limites[i][2]]
    return intersecção_plano_x, intersecção_plano_y, intersecção_plano_z
