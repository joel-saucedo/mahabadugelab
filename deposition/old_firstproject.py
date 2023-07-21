import numpy as np
import matplotlib.pyplot as plt
plt.style.use(['science', 'notebook'])

# Create 2D Geometry of the substrate
class substrate():

    def __init__(self, x, y, N):
        self.x = x
        self.y = y
        self.N = N
    def coor(self):
        _ = np.arange(self.N)
        self.x, self.y = np.meshgrid(_,_)
        return self.x , self.y
    
    

class rparticles(substrate):
    """
    This object will generate purely random iterations 
    of particles on each inherited coordinate of the substrate
    
    rparticles() class will have attributes that easily descibe random
    multidimensional matricies for each coordinate of the substrate
    
    """
    def __init__(self, x, y, N, E, A, t):
        self.E = E
        self.A = A
        self.t = t
        super(rparticles, self).__init__(x, y, N)
  
    def energies(self):
        """
        energies() attribute generates NxN particles and returns two separate
        3-dimensional arrays.
        
        The more time thats ellapsed, the more
        particles will deposit.
        
        The energies generated at each iteration t, and the successfully 
        deposited particles are returned.
        
        """
        self.E = np.random.rand(self.t,self.N,self.N)
        self.A = (self.E>.99).astype(int)
        return self.E, self.A
    
    def sumA(self, i):
        """
        sumA() attribute recursively sums all of the particles 
        with the sufficient energy levels to sucessfully deposit. 
        
        returns particles accumlulated on each coordinate.
        
        """
        def _findSum(A,i):
            if i <= 0:
                return 0
            else:
                return _findSum(A,i - 1) + A[i - 1]
            
        A = self.A
        ans = _findSum(A,i)
        return ans  
    
    def sumE(self, i):
        """
        Recursively sums energies of all particles, 
        regardless of successful deposit.
        
        returns energy accumulated one each coordinate.
        
        """
        def _findSum(E, i):
            if i <= 0:
                return 0
            else:
                return _findSum(E,i - 1) + E[i - 1]
        E = self.E
        ans = _findSum(E,i)
        return ans


"""resolution of substrate area"""
N = 100
sN = substrate(0,0,N)
x, y = sN.coor()

"""if we leave on for a longer time, more particles will deposit
total particles simulated would be the dimensions N x N x d"""

d = 1000
total_particles = N*N*d

print(total_particles)

r = rparticles(0,0,N,0,0,d)
energy_index = r.energies()

#r.sumE(i)    #index gives the ith recursive energy sum
#r.sumA(1)    #index gives the ith recursive boolean sum

#plot the maxtrix

plt.contourf(x,y,r.sumA(1000),levels=30, cmap='plasma')
plt.colorbar(label='Number of Particles')

fig, axes = plt.subplots(1,2, figsize=(10,3.5))

ax = axes[0]
ax.hist(energy_index[0].ravel(), bins=50)
ax.set_ylabel('Number of Particles')


ax = axes[1]
ax.hist(energy_index[1].ravel(), density=True)
ax.set_ylabel('Density')


fig.text(0.5, -0.04, 'Energy Level', ha='center', fontsize = 18 )
plt.show()
