import legume
import numpy as np
import matplotlib.pyplot as plt

print("✓ Legume imported successfully")
print("✓ NumPy version:", np.__version__)

# Create a simple square lattice
lattice = legume.Lattice([1.0, 0], [0, 1.0])
print("✓ Lattice created")

# Create a photonic crystal structure
phc = legume.PhotCryst(lattice)
print("✓ Photonic crystal object created")

# Add a layer
phc.add_layer(d=0.5, eps_b=12.0)
print("✓ Layer added")

# Add a circular hole
phc.layers[-1].add_shape(legume.Circle(r=0.3, eps=1.0))
print("✓ Shape added")

print("\n✓✓✓ All tests passed! Ready for photonic crystal simulations!")