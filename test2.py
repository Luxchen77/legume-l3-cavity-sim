# %%
import legume
import numpy as np
import matplotlib.pyplot as plt

# %%
a = 1.0
lattice = legume.Lattice([a, 0], [a/2, a*np.sqrt(3)/2])
phc = legume.PhotCryst(lattice)
phc.add_layer(d=0.5*a, eps_b=12.0)

# %%
# Add holes with L3 defect
for i in range(-5, 6):
    for j in range(-5, 6):
        x = i*a + (j%2)*a/2
        y = j*a*np.sqrt(3)/2
        if not ((i==0 and j==0) or (i==1 and j==0) or (i==2 and j==0)):
            phc.layers[0].add_shape(legume.Circle(x_cent=x, y_cent=y, r=0.3*a, eps=1.0))

# %%
phc.layers[0].plot_layer()
plt.show()