from warehouse import generate_layout
from evaluation import evaluate_the_cost
import time

# added size + storage as parameters (in the code in general)
def compute_reward(price, size): #passed to be global reward
    return max(0.1,(size*size) / price)


def aco_algo(number_of_layout, iteration, pheromone, size, number_of_storage,evaporation_rate):
    start_time=time.time()
    history = []

    #MODIFICATION now takes size + storage
    best_layout = generate_layout(pheromone, size, number_of_storage)
    best_cost = evaluate_the_cost(best_layout)

    for ite in range(iteration):

        best_iter_cost = float("inf")
        lay = None
        layouts = []

        for _ in range(number_of_layout):

            #modified to take variable of warehouse and number storage
            one_layout = generate_layout(pheromone, size, number_of_storage)
            per_cost = evaluate_the_cost(one_layout)

            layouts.append((one_layout, per_cost))

            if per_cost < best_iter_cost:
                lay = one_layout
                best_iter_cost = per_cost

        # ADDED tracks best and puts in array
        history.append(best_iter_cost)

        layouts.sort(key=lambda x: x[1])

        elite_count = max(1, int(number_of_layout * 0.2))
        elite_layouts = layouts[:elite_count]

        pheromone = update_matrix(elite_layouts, pheromone,evaporation_rate,size) #now takes size

        print(f"In Iteration {ite + 1} the best Cost is {best_iter_cost}")

        # keep global best
        if best_iter_cost < best_cost:
            best_layout = lay
            best_cost = best_iter_cost
    end_time = time.time()
    total_time = end_time - start_time
    return best_layout, pheromone, history, total_time


def update_matrix(layouts, pheromone,evaporation_rate,size): #now takes size

    #reward moved to be global (look at start of code up caused issues)

    # evaporation
    for i in range(len(pheromone)):
        for j in range(len(pheromone[i])):
            pheromone[i][j] *= evaporation_rate

    # reinforcement
    for layout, price in layouts:

        reward = compute_reward(price, size)

        for k in range(len(pheromone)):
            for j in range(len(pheromone[k])):

                if layout[k][j] != " ":
                    pheromone[k][j] += reward

    return pheromone

import math
from itertools import combinations
from warehouse import create_empty_warehouse, PACKING, SHIPPING, STORAGE

# new algo that uses the dfs ( DON'T run it on more that 5X5 )
# the code takes teh same parameters adn return the same types as teh aco for teh sake of swapping them
# but it only uses the size and number_of_storage
def iterative_algo(number_of_layout = 0, iteration = 0, pheromone = 0, size = 5, number_of_storage = 8, evaporation_rate = 0):

    best_cost = float('inf')
    best_layout = None
    evaluations = 0
    start_time = time.time()

    # SYMMETRY BREAKING: Only place P in the top-left quadrant
    # For a 4x4, it only checks (0,0), (0,1), (1,0), (1,1)
    p_max_row = math.ceil(size / 2)
    p_max_col = math.ceil(size / 2)


    # Step 1: Place PACKING
    for px in range(p_max_row):
        for py in range(p_max_col):
            p_loc = (px, py)

            # Step 2: Place SHIPPING anywhere else
            for hx in range(size):
                for hy in range(size):
                    h_loc = (hx, hy)
                    if h_loc == p_loc: 
                        continue

                    # Step 3: Find all remaining empty spots
                    empty_cells = []
                    for r in range(size):
                        for c in range(size):
                            if (r, c) != p_loc and (r, c) != h_loc:
                                empty_cells.append((r, c))

                    # Step 4: Generate all possible STORAGE combinations instantly
                    for s_locs in combinations(empty_cells, number_of_storage):
                        evaluations += 1

                        # Build the layout
                        layout = create_empty_warehouse(size)
                        layout[p_loc[0]][p_loc[1]] = PACKING
                        layout[h_loc[0]][h_loc[1]] = SHIPPING
                        for sx, sy in s_locs:
                            layout[sx][sy] = STORAGE
                        
                        # Evaluate
                        cost = evaluate_the_cost(layout)

                        if cost < best_cost:
                            best_cost = cost
                            best_layout = layout
                            print(f"[{evaluations} Evals] New best: {best_cost} (Time: {round(time.time() - start_time, 2)}s)")

    
    
    # Return formatted to match ACO
    history = [best_cost]
    return best_layout, pheromone, history, (time.time() - start_time), evaluations