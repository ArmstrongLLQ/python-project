import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-1, 1, 0.02)
y1 = x**2
y2 = 2*x+1

#plt.figure()
#plt.plot(x, y1)

plt.figure()
plt.plot(x, y2)
plt.plot(x, y1, color = 'red', linewidth = 1, linestyle = '--')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(0,1)
plt.ylim(-1, 1)

plt.show()