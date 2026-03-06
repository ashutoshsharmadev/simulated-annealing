import random
import math
import time

N = 30
random.seed(69)
# Use native Python lists for better speed in small matrices
matrix = [[random.randint(0,1) for _ in range(N)] for _ in range(N)]

def score(mat):
    # Fast counting with list comprehension
    return sum(mat[i][j] for i in range(N) for j in range(N))

def neighbour(mat):
    # Fast shallow copy and flip
    new = [row[:] for row in mat]  # Faster than deepcopy for 2D lists
    i = random.randint(0, N-1)
    j = random.randint(0, N-1)
    new[i][j] = 1 - new[i][j]
    return new

# Optimized parameters for speed
start_time = time.time()
time_limit = 2.0  # 2 second time limit
T = 10.0
T_min = 0.001
alpha = 0.99

current = matrix
current_score = score(current)
best = [row[:] for row in current]
best_score = current_score

iterations = 0
while time.time() - start_time < time_limit:
    # More iterations per temperature for better exploration
    for _ in range(100):
        candidate = neighbour(current)
        candidate_score = score(candidate)
        
        delta = candidate_score - current_score
        
        if delta > 0 or random.random() < math.exp(delta/T):
            current = candidate
            current_score = candidate_score
            
            # Track best solution found
            if current_score > best_score:
                best = [row[:] for row in current]
                best_score = current_score
        
        iterations += 1
        
        # Time check to avoid TLE
        if time.time() - start_time > time_limit:
            break
            
    T *= alpha
    if T < T_min:
        T = T_min
print(f"Best score: {best_score}")
print(f"Iterations: {iterations}")
print(f"Time: {time.time() - start_time:.3f}s")

#visualize -- eats a lot of time
import matplotlib.pyplot as plt
fig,ax = plt.subplots()
ax.imshow(best, cmap="gray")
plt.show()