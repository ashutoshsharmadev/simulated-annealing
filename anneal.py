import random
import math
import time

N = 30
random.seed(69)

# Pre-generate random numbers to avoid function call overhead
RAND_SIZE = 100000
rand_pool = [random.random() for _ in range(RAND_SIZE)]
rand_idx = 0

# Bitwise matrix representation for ultra-fast operations
matrix = 0
for i in range(N):
    for j in range(N):
        if random.randint(0, 1):
            matrix |= (1 << (i * N + j))

# Precomputed bit positions
bit_positions = [1 << (i * N + j) for i in range(N) for j in range(N)]
pos_to_coord = {1 << (i * N + j): (i, j) for i in range(N) for j in range(N)}

def score_bitwise(mat):
    # Ultra-fast bit counting
    return bin(mat).count('1')

def fast_random():
    global rand_idx
    rand_idx = (rand_idx + 1) % RAND_SIZE
    return rand_pool[rand_idx]

def neighbour_bitwise(mat):
    # XOR flip - fastest possible
    pos = random.choice(bit_positions)
    return mat ^ pos

def multi_neighbour_bitwise(mat):
    # Multiple flips with bitwise operations
    new_mat = mat
    flips = random.randint(1, 3)
    for _ in range(flips):
        pos = random.choice(bit_positions)
        new_mat ^= pos
    return new_mat

# Precomputed exponentials for common temperature ranges
EXP_CACHE = {}
def fast_exp(delta_over_t):
    key = round(delta_over_t * 1000)  # Cache with 3 decimal precision
    if key not in EXP_CACHE:
        EXP_CACHE[key] = math.exp(delta_over_t)
    return EXP_CACHE[key]

# Optimized parameters for speed
start_time = time.time()
time_limit = 5.0  # 2 second time limit
T = 10.0
T_min = 0.001
alpha = 0.99

current = matrix
current_score = score_bitwise(current)
best = current
best_score = current_score

max_achieved = False
stagnant_count = 0
last_best = best_score

iterations = 0
while time.time() - start_time < time_limit and max_achieved == False:
    # More iterations per temperature for better exploration
    for _ in range(200):  # Increased since operations are much faster
        # Alternate between single and multi-flip for diversity
        if iterations % 10 < 7:
            candidate = neighbour_bitwise(current)
        else:
            candidate = multi_neighbour_bitwise(current)
            
        # Incremental scoring (only calculate difference)
        candidate_score = score_bitwise(candidate)
        
        delta = candidate_score - current_score
        
        # Use cached exponential and fast random
        if delta > 0 or (delta < 0 and fast_random() < fast_exp(delta/T)):
            current = candidate
            current_score = candidate_score
            
            # Track best solution found
            if current_score > best_score:
                best = current
                best_score = current_score

            if best_score == last_best:
                stagnant_count += 1
                if stagnant_count > 100:
                    T = 10.0
                    print("hello")
                    stagnant_count = 0
                else:
                    stagnant_count = 0
                    last_best = best_score
                    
        iterations += 1
        
        # MAX score (for N=30, max is 900)
        if best_score >= N*N:
            max_achieved = True
            break
        
        # Time check to avoid TLE
        if time.time() - start_time > time_limit:
            break
            
    T *= alpha
    if T < T_min:
        T = T_min
print(f"Best score: {best_score}")
print(f"Iterations: {iterations}")
print(f"Time: {time.time() - start_time:.3f}s")

# Convert bitwise back to matrix for visualization
def bitwise_to_matrix(mat):
    result = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if mat & (1 << (i * N + j)):
                result[i][j] = 1
    return result

# Optional visualization (comment out for max speed)
# import matplotlib.pyplot as plt
# fig,ax = plt.subplots()
# ax.imshow(bitwise_to_matrix(best), cmap="gray")
# plt.show()

print(f"Final matrix ones: {best_score}/{N*N}")
print(f"Cache hits: {len(EXP_CACHE)}")