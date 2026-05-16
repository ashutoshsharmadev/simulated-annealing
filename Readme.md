# Simulated Annealing — Bitwise Matrix Optimizer

A high-performance simulated annealing implementation in Python, optimized for competitive programming constraints. Maximizes the number of set bits in a random 30×30 binary matrix within a strict time budget.

---
## Motivation

This project was built while learning metaheuristic optimization techniques for a load/dump packing problem during an Larsen & Toubro Technology Services hackathon.

The goal was to understand how simulated annealing behaves under practical constraints and how low-level optimizations can dramatically improve search performance.  
  

## What it does

Given a randomly initialized N×N binary matrix, the solver searches for a configuration that maximizes the count of `1`s — up to the theoretical maximum of N² = 900. Because the search space is enormous (2^900 possible states), exhaustive search is impossible; simulated annealing explores it probabilistically, escaping local optima by occasionally accepting worse solutions early in the run.

The implementation is built around a core insight: **represent the matrix as a single integer and use bitwise XOR flips** instead of list mutations. This makes neighbor generation and state transitions orders of magnitude faster than a naive array-based approach.

---

## How it works

### The algorithm

Simulated annealing mimics the physical process of slowly cooling a material to reach a low-energy state.

1. Start with an initial solution and a high **temperature** T
2. Generate a neighboring solution by flipping one (or a few) bits
3. If the neighbor is better, accept it. If worse, accept it with probability `e^(Δ/T)` — higher temperature means more willingness to accept bad moves
4. Gradually **cool** T by multiplying by `alpha` each iteration
5. If progress stagnates, **reheat** to escape the local optimum

```
T = 10.0  →  T *= 0.99 each step  →  T_min = 0.001
```

### Performance tricks

| Technique | Why |
|---|---|
| **Bitwise matrix** (single `int`) | 30×30 matrix fits in one 900-bit integer; XOR flips a bit in O(1) |
| **Pre-generated random pool** | Avoids repeated `random.random()` call overhead in the hot loop |
| **Exponential cache** | `math.exp` is expensive; results are cached keyed to 3 decimal precision |
| **Single + multi-flip alternation** | Every 10th iteration does 1–3 flips for broader neighborhood exploration |
| **Stagnation reheating** | If best score doesn't improve for 100 cycles, T resets to 10.0 |
| **Hard time limit** | Loop exits after 5 seconds — safe for judge time limits |

---

## Usage

No external dependencies. Runs on standard Python 3.

```bash
git clone https://github.com/ashutoshsharmadev/simulated-annealing.git
cd simulated-annealing
python anneal.py
```

### Example output

```
Best score: 900
Iterations: 85485
Time: 0.236s
Final matrix ones: 900/900
Cache hits: 1102
```

---

## Configuration

All tunable parameters are at the top of `anneal.py`:

| Parameter | Default | Description |
|---|---|---|
| `N` | `30` | Matrix size (N×N) |
| `T` | `10.0` | Starting temperature |
| `T_min` | `0.001` | Minimum temperature floor |
| `alpha` | `0.99` | Cooling rate per outer iteration |
| `time_limit` | `5.0` | Wall-clock time budget (seconds) |
| `RAND_SIZE` | `100000` | Size of pre-generated random pool |

---

## Visualization

A matplotlib visualization is included but commented out for performance reasons. To enable it:

```python
# At the bottom of anneal.py, uncomment:
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.imshow(bitwise_to_matrix(best), cmap="gray")
plt.show()
```

Install matplotlib if needed:
```bash
pip install matplotlib
```

---

## Adapting to other problems

The core loop is problem-agnostic. To apply this to a different optimization problem:

1. **Change `score_bitwise()`** — replace bit counting with your objective function
2. **Change `neighbour_bitwise()`** — define what a "neighboring solution" means for your problem
3. **Change the initial state** — replace `matrix` with your starting configuration

Common applications: Travelling Salesman Problem, graph coloring, job scheduling, N-Queens.

---

## License

MIT
