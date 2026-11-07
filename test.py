from warehouse import set_seed, initial_pheromone
from aco import aco_algo, iterative_algo
from warehouse import print_layout
import matplotlib.pyplot as plt


#CHANGED AND FIXED 
ANT_COUNT = 150
ITERATIONS = 18


def run_experiment():

    print("\n WAREHOUSE aco ---\n")

    #INPUTS (UI later will replace this)
    size = int(input("Enter warehouse size (NxN): "))
    storage_count = int(input("Enter number of storage units: "))
    evaporation_rate = float(input("Enter evaporation rate (the lower the faster the system will forget): "))


    # INPUT VALIDATION
    # -----------------------
    max_storage = size * size - 2

    if storage_count > max_storage:
        print(f"Error: storage cannot exceed {max_storage}")
        return

    if evaporation_rate <= 0 or evaporation_rate >= 1:
        print("Error: evaporation must be between 0 and 1 (exclusive)")
        return
    

    set_seed(42) #seed 


    pheromone = initial_pheromone(size)

    
    # RUN ACO
    # RUN Iterative
    best_layout, pheromone, history = aco_algo(
        number_of_layout=ANT_COUNT,
        iteration=ITERATIONS,
        pheromone=pheromone,
        size=size,
        number_of_storage=storage_count,
        evaporation_rate=evaporation_rate
        
    )

    # RESULTS
    # -----------------------
    print("\n--- OPTIMIZATION COMPLETE ---\n")

    print("Best Layout Found:\n")
    print_layout(best_layout)

    print(f"Final Best Cost: {min(history)}")

    print("\nConvergence History:")
    print(history)

    plt.plot(range(1, len(history) + 1), history)

    plt.title("ACO Convergence")
    plt.xlabel("Generation (Iteration)")
    plt.ylabel("Best Cost")

    plt.grid()
    plt.show()


if __name__ == "__main__":
    run_experiment()