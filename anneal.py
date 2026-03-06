import numpy as np
import matplotlib.pyplot as plt
import random
import math

N = 30
random.seed(69)
matrix = np.random.randint(0,2,(N,N))

def score(mat):
    # maximize this
    # make the biggest matrix with same number have highest score
    sum = np.sum(mat == 1) #sum of all places where value is 1
    # sum = sum of submatrix with max
    return sum

def neighbour(mat):
    #Flips 1s and 0s
    new = mat.copy()
    i = random.randint(0, N-1)
    j = random.randint(0, N-1)
    if(new[i,j] == 0):
        new[i,j] = 1- new[i,j] #flip the cell
    return new

#parameters
T=5.0
T_min=0.01
alpha=0.995

current=matrix
current_score=score(current)

#visualise
plt.ion()
fig,ax=plt.subplots()

while T > T_min:
    for _ in range(10):
        candidate = neighbour(current)
        candidate_score = score(candidate)
        
        delta = candidate_score - current_score
        
        if delta > 0 or random.random() < math.exp(delta/T):
            current = candidate
            current_score = candidate_score
            
        ax.clear()
        ax.imshow(current, cmap="gray")
        ax.set_title(f"Score: {current_score} Temp: {T:.3f}")
        plt.pause(0.01)
        
    T*=alpha
    
plt.ioff()
plt.show()