from TPSoft import TPSoft
import numpy as np
import matplotlib.pyplot as plt

TPC = TPSoft.TPC(1000, 1000, 1000)
Muon = TPSoft.Partícula(TPC.comprimento_x/2, 0, TPC.comprimento_z/2, np.pi/2, np.pi/2)

fig = plt.figure('Coleção - Histograma')

ax1 = fig.add_subplot(141, projection='3d')

ax1.set_xlim(0, TPC.comprimento_x)
ax1.set_ylim(0, TPC.comprimento_y)
ax1.set_zlim(0, TPC.comprimento_z)

ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('z')

TPC.plotar(ax1)
Muon.plotar(TPC,ax1)

ax2 = fig.add_subplot(142)
TPC.coleção_de_luz(Muon, 0.05, ax2, x=0, tipo='Hist')
ax2.set_xlim(0, 1000)
ax2.set_ylim(0, 1000)

ax3 = fig.add_subplot(143)
TPC.coleção_de_luz(Muon, 0.05, ax3, y=0, tipo='Hist')
ax3.set_xlim(0, 1000)
ax3.set_ylim(0, 1000)

ax4 = fig.add_subplot(144)
TPC.coleção_de_luz(Muon, 0.05, ax4, z=0, tipo='Hist')
ax4.set_xlim(0, 1000)
ax4.set_ylim(0, 1000)

plt.show()
