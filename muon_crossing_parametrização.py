from TPSoft import TPSoft
import numpy as np
import matplotlib.pyplot as plt

TPC = TPSoft.TPC(1000, 1000, 1000)
fig = plt.figure('Parametrização - Múon')
ax1 = fig.add_subplot(111, projection='3d')
ax1.set_xlim(0, TPC.comprimento_x)
ax1.set_ylim(0, TPC.comprimento_y)
ax1.set_zlim(0, TPC.comprimento_z)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('z')
TPC.plotar(ax1)
Muon = TPSoft.Partícula(TPC.comprimento_x/2,  TPC.comprimento_y/2, TPC.comprimento_z/2, np.pi/2, np.pi/2)
Muon.plotar(TPC, ax1)
plt.show()
