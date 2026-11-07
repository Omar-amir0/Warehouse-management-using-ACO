
STORAGE = "S"
PACKING = "P"
SHIPPING = "H"

TRAVEL_TIME_PER_UNIT = 2
CONGESTION_PENALTY = 8
#only change made is in calculate congestion to punish for any adjacent boxes not just greater than 3
def calculate_manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def calculate_congestion(layout, x, y):
    rows = len(layout)
    cols = len(layout[0])
    adjacent_storage = 0
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if layout[nx][ny] == STORAGE:
                adjacent_storage += 1
                

    return adjacent_storage*CONGESTION_PENALTY*2

def evaluate_the_cost(layout):
    packing_loc = None
    shipping_loc = None
    storage_locs = []
    
    for i in range(len(layout)):
        for j in range(len(layout[i])):
            if layout[i][j] == PACKING:
                packing_loc = (i, j)
            elif layout[i][j] == SHIPPING:
                shipping_loc = (i, j)
            elif layout[i][j] == STORAGE:
                storage_locs.append((i, j))

    total_distance = 0
    total_congestion = 0
    
    for s_loc in storage_locs:
        dist_from_pack = calculate_manhattan_distance(packing_loc, s_loc)
        dist_to_ship = calculate_manhattan_distance(s_loc, shipping_loc)
        total_distance += (dist_from_pack + dist_to_ship)
        
        total_congestion += calculate_congestion(layout, s_loc[0], s_loc[1])

    travel_cost = total_distance * TRAVEL_TIME_PER_UNIT
    
    total_cost = travel_cost + total_congestion
    
    return total_cost

if __name__ == "__main__":
    test_layout = [
        [" ", " ", " ", " ", " "],
        [" ", "S", "S", "S", " "],
        [" ", "S", "P", "S", " "],
        [" ", "S", "H", "S", " "],
        [" ", " ", "S", " ", " "]
    ]
    
    cost = evaluate_the_cost(test_layout)
    print("Validating Cost Calculation System...")
    print(f"Calculated Cost for test layout: {cost}")