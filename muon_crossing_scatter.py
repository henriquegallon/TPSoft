from TPSoft import TPSoft
import numpy as np
import matplotlib.pyplot as plt

"""Exemplo de código para traçar um scatter da coleção 
de luz de uma partícula em uma TPC de geometria paralel."""

TPC = TPSoft.TPC(20, geometria='paralel', comprimento_x=1000, comprimento_y=1000, comprimento_z=1000)
Muon = TPSoft.Partícula(TPC.comprimento_x/2, 0, TPC.comprimento_z/2, np.pi/2, np.pi/2)

fig = plt.figure('Coleção de Luz - Scatter')

ax1 = fig.add_subplot(121, projection='3d')

ax1.set_xlim(0, TPC.comprimento_x)
ax1.set_ylim(0, TPC.comprimento_y)
ax1.set_zlim(0, TPC.comprimento_z)

ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('z')

TPC.plotar(ax1)
Muon.plotar(TPC, ax1)

ax2 = fig.add_subplot(122)

TPC.coleção_de_luz(Muon, 1, ax2, z=0, tipo='Scatter')

ax2.set_xlim(0, TPC.comprimento_x)
ax2.set_ylim(0, TPC.comprimento_y)

plt.show()
