import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Partícula:
    """Define um objeto Prtícula a partir de sua posição inicial no espaço e sua direção de emissão."""

    def __init__(self, x_emissão, y_emissão, z_emissão, teta, fi):
        
        self.deposição = 100
        self.velocidade = 3*10**8
        self.x_emissão = x_emissão
        self.y_emissão = y_emissão
        self.z_emissão = z_emissão
        self.teta = teta
        self.fi = fi

    def plotar(self, TPC, ax):
        """Traça a trajetória da partícula em um espaço tridimensional no interior de uma TPC."""

        if TPC.geometria == 'paralel':

            t = np.arange(0, encontrar_limite_paralel(self.teta, self.fi, self.x_emissão, self.y_emissão, self.z_emissão, TPC))

            x = t * np.sin(self.teta) * np.cos(self.fi) + self.x_emissão
            y = t * np.sin(self.teta) * np.sin(self.fi) + self.y_emissão
            z = t * np.cos(self.teta) + self.z_emissão

            ax.plot(x, y, z)


class TPC:
    """Define um objeto Time Projection Chamber (TPC) a partir de sua geometria e dimensões. 
    Para adicionar novas geometrias, o código poderá ser só incrementado."""

    def __init__(self, resolução, **kwargs):
        
        self.resolução = resolução

        for chave, valor in kwargs.items():

            if chave == 'geometria' and valor == 'paralel':

                self.geometria = valor
                self.fotons_por_MeV = 10

                for chave, valor in kwargs.items():

                    if chave == 'comprimento_x':

                        self.comprimento_x = valor

                    elif chave == 'comprimento_y':

                        self.comprimento_y = valor
                        
                    elif chave == 'comprimento_z':

                        self.comprimento_z = valor

                self.grid_x0 = grid(self.comprimento_y, self.comprimento_z, resolução)
                self.grid_x = grid(self.comprimento_y, self.comprimento_z, resolução)
                self.grid_y0 = grid(self.comprimento_x, self.comprimento_z, resolução)
                self.grid_y = grid(self.comprimento_x, self.comprimento_z, resolução)
                self.grid_z0 = grid(self.comprimento_x, self.comprimento_y, resolução)
                self.grid_z = grid(self.comprimento_x, self.comprimento_y, resolução)

    def plotar(self, ax):
        """Traça os limites da TPC em um espaço tridimensional."""
        
        if self.geometria == 'paralel':

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
        """Simula a coleção de fótons em uma parede da TPC.
        Pode ser traçada em um gráfico como um scatter ou um histograma."""

        if self.geometria == 'paralel':
            
            x_plano, y_plano, z_plano = None, None, None

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
                
                medio = [(x_antigo + x) / 2, (y_antigo + y) / 2, (z_antigo + z) / 2]
                
                if not (0 <= medio[0] <= self.comprimento_x and 0 <= medio[1] <= self.comprimento_y and 0 <= medio[2] <= self.comprimento_z):
                    
                    break      

                qtd_de_fotons = delta * Particula.deposição * self.fotons_por_MeV
            
                intersecção_plano_x, intersecção_plano_y, intersecção_plano_z = intersecção_foton_limites(self, medio, round(qtd_de_fotons), x_plano, y_plano, z_plano)

                intersecção_plano_x_geral += intersecção_plano_x
                intersecção_plano_y_geral += intersecção_plano_y
                intersecção_plano_z_geral += intersecção_plano_z

            for chave, valor in kwargs.items():
        
                if chave == 'tipo' and valor == 'Scatter':
            
                    if x_plano == None and y_plano == None:
            
                        ax.scatter(intersecção_plano_x_geral, intersecção_plano_y_geral, s=0.1)
            
                    elif x_plano == None  and z_plano == None:
            
                        ax.scatter(intersecção_plano_x_geral, intersecção_plano_z_geral, s=0.1)
            
                    elif y_plano == None and z_plano == None:
            
                        ax.scatter(intersecção_plano_y_geral, intersecção_plano_z_geral, s=0.1)
            
                elif chave == 'tipo' and valor == 'Hist':
            
                    if x_plano == None and y_plano == None:
            
                        ax.hist2d(intersecção_plano_x_geral, intersecção_plano_y_geral, bins=self.resolução)
            
                    elif x_plano == None and z_plano == None:
            
                        ax.hist2d(intersecção_plano_x_geral, intersecção_plano_z_geral, bins=self.resolução)
                        
                    elif y_plano == None and z_plano == None:
            
                        ax.hist2d(intersecção_plano_y_geral, intersecção_plano_z_geral, bins=self.resolução)        


def grid(limite_1, limite_2, resolução):
    """Define uma grade na forma de uma lista para determinado plano e resolução."""

    grid_1 = []
    grid_2 = []
    grid = []

    i = 0 
    while i < limite_1:

        grid_1 += [[i, i + (limite_1/resolução)]]

        i = i + (limite_1/resolução)

    i = 0
    while i < limite_2:

        grid_2 += [[i, i + (limite_2/resolução)]]

        i = i + (limite_2/resolução)

    for i in range(len(grid_1)):
        
        for j in range(len(grid_2)):

            grid += [[grid_1[i][0], grid_1[i][1], grid_2[j][0], grid_2[j][1]]]

    return grid

def ângulo_sólido(a,b,d):
    """Calcula o ângulo sólido para uma placa retangular centralizada no ponto de observação.
    Utiliza a referência "Solid Angle of a Rectangular Plate", Richard J. Mathar."""

    alfa = a/(2*d)

    beta = b/(2*d)

    ângulo_sólido = 4*np.arccos(np.sqrt((1+alfa**2+beta**2)/((1+alfa**2)*(1+beta**2))))

    return ângulo_sólido

def ângulo_sólido_off(a,A,b,B,d):
    """Calcula o ângulo sólido para uma placa retangular que não contêm o ponto de observação em nenhuma de suas dimensões.
    Utiliza a referência "Solid Angle of a Rectangular Plate", Richard J. Mathar."""

    ângulo_sólido_off = (ângulo_sólido(2*(A+a),2*(B+b),d)-ângulo_sólido(2*A,2*(B+b),d)-ângulo_sólido(2*(A+a),2*B,d)+ângulo_sólido(2*A,2*B,d))/4

    return ângulo_sólido_off

def ângulo_sólido_alin(a,A,b,B,d):
    """Calcula o ângulo sólido para uma placa retangular que contêm o ponto de observação em uma de suas dimensões.
    Utiliza a referência "Solid Angle of a Rectangular Plate", Richard J. Mathar."""

    ângulo_sólido_alin = (ângulo_sólido(2*(A+a),2*(b-B),d)-ângulo_sólido(2*A,2*(b-B),d)+ângulo_sólido(2*(A+a),2*B,d)-ângulo_sólido(2*A,2*B,d))/4

    return ângulo_sólido_alin

def ângulo_sólido_in(a,A,b,B,d):
    """Calcula o ângulo sólido para uma placa retangular que contêm o ponto de observação em ambas de suas dimensões.
    Utiliza a referência "Solid Angle of a Rectangular Plate", Richard J. Mathar."""

    ângulo_sólido_in = (ângulo_sólido(2*(a-A),2*(b-B),d)+ângulo_sólido(2*A,2*(b-B),d)+ângulo_sólido(2*(a-A),2*B,d)+ângulo_sólido(2*A,2*B,d))/4

    return ângulo_sólido_in

def calcular_ângulo_sólido(x, y, x0, y0, a, b, d):
    """A partir de um ponto qualquer (x,y) calcula o ângulo sólido de uma placa a x b localizada à uma distância d ortogonal ao ponto.
    Usa das expressões definidas até aqui para obter esse resultado dividindo o plano de coleção em nove regiões."""
    
    if x <= x0 and y >= y0 + b:

        A = x0 - x
        B = y - y0 - b

        return ângulo_sólido_off(a, A, b, B, d)

    elif x0 <= x <= x0 + a and y >= y0 + b:

        A = y - y0 - b
        B = x - x0
        a_i = b
        b_i = a

        return ângulo_sólido_alin(a_i, A, b_i, B, d)

    elif x >= x0 + a and y >= y0 + b:

        A = x - x0 - a
        B = y - y0 - b

        return ângulo_sólido_off(a, A, b, B, d)

    elif x <= x0 and y0 <= y <= y0 + b:

        A = x0 - x
        B = y - y0

        return ângulo_sólido_alin(a, A, b, B, d)

    elif x0 <= x <= x0 + a and y0 <= y <= y0 + b:

        A = x - x0
        B = y - y0

        return ângulo_sólido_in(a, A, b, B, d)

    elif x >= x0 + a and y0 <= y <= y0 + b:

        A = x - x0 - a
        B = y - y0

        return ângulo_sólido_alin(a, A, b, B, d)

    elif x <= x0 and y <= y0:

        A = x0 - x
        B = y0 - y

        return ângulo_sólido_off(a, A, b, B, d)

    elif x0 <= x <= x0 + a and y <= y0:

        A = y0 - y
        B = b - x + x0
        a_i = b
        b_i = a

        return ângulo_sólido_alin(a, A, b, B, d)

    elif x >= x0 + a and y <= y0:

        A = x - x0 - a
        B = y0 - y

        return ângulo_sólido_off(a, A, b, B, d)

def intersecção_foton_limites(TPC, medio, quantidade, x_plano, y_plano, z_plano):
    """Usa de um grid de ângulos sólidos para simular a quantidade de fótons coletados em cada divisão do plano."""

    ângulos_sólidos_grid = []
    prob_grid = []
    soma = 0
    antigo = 0
    intersecção_plano_x = []
    intersecção_plano_y = []
    intersecção_plano_z = []

    if x_plano != None and x_plano == 0:

        grid = TPC.grid_x0

    elif x_plano != None:

        grid = TPC.grid_x

    if y_plano != None and y_plano == 0:

        grid = TPC.grid_y0

    elif y_plano != None:

        grid = TPC.grid_y
    
    if z_plano != None and z_plano == 0:

        grid = TPC.grid_z0

    elif z_plano != None:

        grid = TPC.grid_z

    for i in range(len(grid)):

        if x_plano == 0:

            ângulos_sólidos_grid += [[i, calcular_ângulo_sólido(medio[1],
                                                                medio[2],
                                                                grid[i][0],
                                                                grid[i][2],
                                                                grid[i][1]-grid[i][0],
                                                                grid[i][3]-grid[i][2],
                                                                medio[0])]]

        elif x_plano != None:
                                                            
            ângulos_sólidos_grid += [[i, calcular_ângulo_sólido(medio[1],
                                                                medio[2],
                                                                grid[i][0],
                                                                grid[i][2],
                                                                grid[i][1]-grid[i][0],
                                                                grid[i][3]-grid[i][2],
                                                                TPC.comprimento_x - medio[0])]]

        elif y_plano == 0:
            
            ângulos_sólidos_grid += [[i, calcular_ângulo_sólido(medio[0],
                                                                medio[2],
                                                                grid[i][0],
                                                                grid[i][2],
                                                                grid[i][1]-grid[i][0],
                                                                grid[i][3]-grid[i][2],
                                                                medio[1])]]

        elif y_plano != None:

            ângulos_sólidos_grid += [[i, calcular_ângulo_sólido(medio[0],
                                                                medio[2],
                                                                grid[i][0],
                                                                grid[i][2],
                                                                grid[i][1]-grid[i][0],
                                                                grid[i][3]-grid[i][2],
                                                                TPC.comprimento_y - medio[1])]]

        elif z_plano == 0:

            ângulos_sólidos_grid += [[i, calcular_ângulo_sólido(medio[0],
                                                                medio[1],
                                                                grid[i][0],
                                                                grid[i][2],
                                                                grid[i][1]-grid[i][0],
                                                                grid[i][3]-grid[i][2],
                                                                medio[2])]]

        elif z_plano != None:

            ângulos_sólidos_grid += [[i, calcular_ângulo_sólido(medio[0],
                                                                medio[1],
                                                                grid[i][0],
                                                                grid[i][2],
                                                                grid[i][1]-grid[i][0],
                                                                grid[i][3]-grid[i][2],
                                                                TPC.comprimento_z - medio[2])]]

    soma = (ângulo_sólido_in(TPC.comprimento_x, medio[0], TPC.comprimento_y, medio[1], medio[2]) +
            ângulo_sólido_in(TPC.comprimento_x, medio[0], TPC.comprimento_y, medio[1], TPC.comprimento_z - medio[2]) +
            ângulo_sólido_in(TPC.comprimento_x, medio[0], TPC.comprimento_z, medio[2], medio[1]) +
            ângulo_sólido_in(TPC.comprimento_x, medio[0], TPC.comprimento_z, medio[2], TPC.comprimento_y - medio[1]) +
            ângulo_sólido_in(TPC.comprimento_y, medio[1], TPC.comprimento_z, medio[2], medio[0]) +
            ângulo_sólido_in(TPC.comprimento_y, medio[1], TPC.comprimento_z, medio[2], TPC.comprimento_x - medio[0]))

    for i in range(len(ângulos_sólidos_grid)):

        prob_grid += [[ângulos_sólidos_grid[i][0], antigo, antigo + (ângulos_sólidos_grid[i][1]/soma)]]

        antigo = antigo + (ângulos_sólidos_grid[i][1]/soma)
    
    for i in range(quantidade):

        sorteio = np.random.random()

        for j in range(len(prob_grid)):

            if prob_grid[j][1] <= sorteio <= prob_grid[j][2]:

                if x_plano != None:
                    
                    intersecção_plano_x += [x_plano]
                    intersecção_plano_y += [(grid[j][1]-grid[j][0])*np.random.random()+grid[j][0]]
                    intersecção_plano_z += [(grid[j][3]-grid[j][2])*np.random.random()+grid[j][2]]

                elif y_plano != None:
                    
                    intersecção_plano_x += [(grid[j][1]-grid[j][0])*np.random.random()+grid[j][0]]
                    intersecção_plano_y += [y_plano]
                    intersecção_plano_z += [(grid[j][3]-grid[j][2])*np.random.random()+grid[j][2]]


                elif z_plano != None: 

                    intersecção_plano_x += [(grid[j][1]-grid[j][0])*np.random.random()+grid[j][0]]
                    intersecção_plano_y += [(grid[j][3]-grid[j][2])*np.random.random()+grid[j][2]]
                    intersecção_plano_z += [z_plano]

    return intersecção_plano_x, intersecção_plano_y, intersecção_plano_z

def encontrar_limite_paralel(teta, fi, x_emissão, y_emissão, z_emissão, TPC):
    """Calcula a intersecção entre uma TPC de geometria paralel e uma trajetória de certa partícula.
    Não deve ser utilizada para simular a coleção."""

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

        if fi < fis[0] or fi >= fis[3]:
        
            limites_escolhidos = [limites_x_y_z[2],limites_x_y_z[0]]

        elif fis[0] <= fi < fis[1]:
            
            limites_escolhidos = [limites_x_y_z[2],limites_x_y_z[1]]

        elif fis[1] <= fi < fis[2]:

            limites_escolhidos = [limites_x_y_z[2],limites_x_y_z[3]]

        elif fis[2] <= fi < fis[3]:

            limites_escolhidos = [limites_x_y_z[2],limites_x_y_z[4]]

    elif teta > np.pi/2:

        if fi < fis[0] or fi >= fis[3]:

            limites_escolhidos = [limites_x_y_z[5],limites_x_y_z[0]]

        elif fis[0] <= fi < fis[1]:

            limites_escolhidos = [limites_x_y_z[5],limites_x_y_z[1]]

        elif fis[1] <= fi < fis[2]:

            limites_escolhidos = [limites_x_y_z[5],limites_x_y_z[3]]
            
        elif fis[2] <= fi < fis[3]:

            limites_escolhidos = [limites_x_y_z[5],limites_x_y_z[4]]

    else:

        if fi < fis[0] or fi >= fis[3]:

            limites_escolhidos = [limites_x_y_z[0]]

        elif fis[0] <= fi < fis[1]:

            limites_escolhidos = [limites_x_y_z[1]]

        elif fis[1] <= fi < fis[2]:

            limites_escolhidos = [limites_x_y_z[3]]

        elif fis[2] <= fi < fis[3]:

            limites_escolhidos = [limites_x_y_z[4]]

    limites_escolhidos.sort()

    return limites_escolhidos[0]
