import random
from math import ceil, floor

#little changes 
#FIXED SEED FUNCTION
def set_seed(seed=42):
    random.seed(seed)


# Zone symbols
STORAGE = "S"
PACKING = "P"
SHIPPING = "H"
EMPTY = " "



#MODIFIED SIZE IS NOW (NxN) USER INPUT
def create_empty_warehouse(size):
    warehouse = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(EMPTY)
        warehouse.append(row)
    return warehouse


def initial_pheromone(size):
    pheromone = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(1.0)
        pheromone.append(row)
    return pheromone


#this is the old layout that we were using
#you can use it be editing its name to generate_layout 
#and edit the one down to a different name
def generate_random_layout(pheromone, size, number_of_storage):
    warehouse = create_empty_warehouse(size)

    # PACKING
    px = random.randint(0, size - 1)
    py = random.randint(0, size - 1)
    warehouse[px][py] = PACKING

    # SHIPPING
    while True:
        hx = random.randint(0, size - 1)
        hy = random.randint(0, size - 1)
        if warehouse[hx][hy] == EMPTY:
            warehouse[hx][hy] = SHIPPING
            break

    # STORAGE PLACEMENT
    placed = 0
    while placed < number_of_storage:

        empty_spots = []
        weights = []

        for i in range(size):
            for j in range(size):
                if warehouse[i][j] == EMPTY:
                    empty_spots.append((i, j))
                    weights.append(pheromone[i][j])

        if empty_spots:
            chosen = random.choices(empty_spots, weights=weights, k=1)[0]
            x, y = chosen
            warehouse[x][y] = STORAGE
            placed += 1

    return warehouse


#the new function that uses heuritics ( made by :)
def generate_layout(pheromone, size, number_of_storage):
    """
    Places Packing (P) and Shipping (H) in the center.
    Storage (S) is placed using a combination of pheromones AND the distance heuristic.
    """
    warehouse = create_empty_warehouse(size)

    # Center placement for doors
    px = ceil(size / 2) - 1 # Adjusted for 0-indexing
    py = floor(size / 2)
    hx = floor(size / 2)
    hy = ceil(size / 2) - 1

    warehouse[px][py] = PACKING
    
    # Failsafe in case P and H overlap on very small/even grids
    if warehouse[hx][hy] != EMPTY:
        for i in range(size):
            if warehouse[i][hy] == EMPTY:
                hx = i
                break
    warehouse[hx][hy] = SHIPPING

    # STORAGE PLACEMENT
    placed = 0
    while placed < number_of_storage:
        empty_spots = []
        weights = []

        for i in range(size):
            for j in range(size):
                if warehouse[i][j] == EMPTY:
                    empty_spots.append((i, j))
                    
                    # Heuristic: Closer to doors = higher starting weight
                    dist_to_doors = abs(i - px) + abs(j - py) + abs(i - hx) + abs(j - hy)
                    heuristic = 10.0 / (dist_to_doors + 1)
                    
                    # Final weight is Pheromone * Heuristic
                    weights.append(pheromone[i][j] * heuristic)

        if empty_spots:
            chosen = random.choices(empty_spots, weights=weights, k=1)[0]
            x, y = chosen
            warehouse[x][y] = STORAGE
            placed += 1

    return warehouse

def print_layout(layout):
    for row in layout:
        print(" | ".join(row))
    print()