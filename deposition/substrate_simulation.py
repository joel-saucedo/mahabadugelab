import numpy as np
import matplotlib.pyplot as plt

class Atom:
    def __init__(self, element, x, y, time_dependent=True, random_behavior=True):
        self.element = element
        self.x = x
        self.y = y
        self.time_dependent = time_dependent
        self.random_behavior = random_behavior

    def __str__(self):
        return f"{self.element} atom at ({self.x}, {self.y})"

    def update_position(self):
        if self.time_dependent and self.random_behavior:
            self.x += np.random.normal(scale=0.1)  # Random movement in x-direction
            self.y += np.random.normal(scale=0.1)  # Random movement in y-direction


class Substrate:
    def __init__(self, N):
        self.N = N
        self.atoms = []
        self.x = None
        self.y = None

    def add_atom(self, element, x, y, time_dependent=True, random_behavior=True):
        atom = Atom(element, x, y, time_dependent, random_behavior)
        self.atoms.append(atom)
        self.x = np.array([atom.x for atom in self.atoms])
        self.y = np.array([atom.y for atom in self.atoms])

    def coor(self):
        _ = np.arange(self.N)
        x, y = np.meshgrid(_, _)
        return x, y

    def plot_atoms(self):
        if not self.atoms:
            print("No atoms on the substrate.")
            return

        fig, ax = plt.subplots()
        x_coords = [atom.x for atom in self.atoms]
        y_coords = [atom.y for atom in self.atoms]
        elements = [atom.element for atom in self.atoms]
        ax.scatter(x_coords, y_coords, c='b', s=100, marker='o')

        for i, txt in enumerate(elements):
            ax.annotate(txt, (x_coords[i], y_coords[i]), textcoords="offset points", xytext=(0, 5), ha='center')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Substrate Geometry')
        ax.grid(True)
        plt.show()


    """
    This object will generate purely random iterations 
    of particles on each inherited coordinate of the substrate
    """

class RParticles(Substrate):
    
    def __init__(self, N, t):
        self.t = t
        super().__init__(N)
        self.E = np.random.rand(self.t, self.N, self.N)
        self.A = (self.E > 0.99).astype(int)

    def update_atoms(self):
        for atom in self.atoms:
            atom.update_position()

    def get_energies_and_particles(self):
        self.E = np.random.rand(self.t, self.N, self.N)
        self.A = (self.E > 0.99).astype(int)
        return self.E, self.A

    def sum_particles(self, i):
        if i < 0 or i >= self.t:
            raise ValueError("Invalid time iteration index.")
        return np.sum(self.A[:i + 1], axis=0)

    def sum_energy_deposition(self, i):
        if i < 0 or i >= self.t:
            raise ValueError("Invalid time iteration index.")
        return np.sum(self.E[:i + 1], axis=0)

    def get_particle_at_t(self, i):
        if i < 0 or i >= self.t:
            raise ValueError("Invalid time iteration index.")
        return self.A[i]

    def get_energy_at_t(self, i):
        if i < 0 or i >= self.t:
            raise ValueError("Invalid time iteration index.")
        return self.E[i]

    # Additional method for boolean success where particles hit and attach to the substrate
    def sum_success_particles(self, i):
        if i < 0 or i >= self.t:
            raise ValueError("Invalid time iteration index.")
        return np.logical_and.reduce(self.A[:i + 1], axis=0)

    # Rest of the RParticles class...


# Example usage with RParticles
substrate = Substrate(N=5)
substrate.add_atom('Si', 0, 0, time_dependent=True, random_behavior=True)
substrate.add_atom('O', 1, 1, time_dependent=True, random_behavior=True)
substrate.add_atom('H', 4, 3, time_dependent=True, random_behavior=True)

substrate.plot_atoms()

# Create an instance of RParticles with N and t arguments
r_particles = RParticles(N=substrate.N, t=10)

# Update atom positions for t=10 iterations
for _ in range(r_particles.t):
    r_particles.update_atoms()

# Get random energies and particles for each time iteration
energies, particles = r_particles.get_energies_and_particles()

# Print random energies for each time iteration
print("Random Energies:")
print(energies)

# Print random particles for each time iteration
print("Random Particles:")
print(particles)

# Sum energy deposition on each coordinate at iteration t=5
accumulated_energy = r_particles.sum_energy_deposition(i=5)
print("Accumulated Energy Deposition:")
print(accumulated_energy)

# Get particles at iteration t=5
particles_at_t5 = r_particles.get_particle_at_t(i=5)
print("Particles at iteration t=5:")
print(particles_at_t5)

# Get energy at iteration t=5
energy_at_t5 = r_particles.get_energy_at_t(i=5)
print("Energy at iteration t=5:")
print(energy_at_t5)

# Sum success where particles hit and attach to the substrate at iteration t=5
success_particles_at_t5 = r_particles.sum_success_particles(i=5)
print("Success Particles at iteration t=5:")
print(success_particles_at_t5)

# Plot normalized total energy distribution
total_energy = r_particles.sum_energy_deposition(i=r_particles.t - 1)
plt.hist(total_energy.flatten(), bins=20, density=True, alpha=0.7, color='blue')
plt.xlabel("Total Energy")
plt.ylabel("Normalized Frequency")
plt.title("Normalized Total Energy Distribution")
plt.grid(True)
plt.show()

# Plot boolean success where particles hit and attach to the substrate at iteration t=5
plt.imshow(success_particles_at_t5, cmap='binary', origin='lower', extent=[0, substrate.N, 0, substrate.N])
plt.colorbar(label='Success (1) / Failure (0)')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Boolean Success of Particle Deposition on Substrate')
plt.grid(True)
plt.show()
