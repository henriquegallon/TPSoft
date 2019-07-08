from TPSoft import TPSoft
import numpy as np
import matplotlib.pyplot as plt

"""Exemplo de código para traçar um histograma da coleção de luz 
de três placas de uma partícula em uma TPC de geometria paralel."""

TPC = TPSoft.TPC(20, geometria='paralel', comprimento_x=1000, comprimento_y=1000, comprimento_z=1000)
Muon = TPSoft.Partícula(TPC.comprimento_x/2, 0, TPC.comprimento_z/2, np.pi/2, np.pi/2)

fig = plt.figure('Coleção de Luz (três placas) - Histograma')

ax1 = fig.add_subplot(221, projection='3d')

ax1.set_xlim(0, TPC.comprimento_x)
ax1.set_ylim(0, TPC.comprimento_y)
ax1.set_zlim(0, TPC.comprimento_z)

ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('z')

TPC.plotar(ax1)
Muon.plotar(TPC,ax1)

ax2 = fig.add_subplot(222)
TPC.coleção_de_luz(Muon, 1, ax2, x=0, tipo='Hist')
ax2.set_xlim(0, 1000)
ax2.set_ylim(0, 1000)

ax3 = fig.add_subplot(223)
TPC.coleção_de_luz(Muon, 1, ax3, y=0, tipo='Hist')
ax3.set_xlim(0, 1000)
ax3.set_ylim(0, 1000)

ax4 = fig.add_subplot(224)
TPC.coleção_de_luz(Muon, 1, ax4, z=0, tipo='Hist')
ax4.set_xlim(0, 1000)
ax4.set_ylim(0, 1000)

plt.show()