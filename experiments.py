import csv
import statistics
from warehouse import set_seed, initial_pheromone
from aco import aco_algo
#DO NOT RUN IT TAKES 45MINS TO COMPILE
#DO NOT RUN
#DO NOT RUN
#DO NOT RUN

# RUN ONE CONFIG (30 times)
def run_single_setting(
    num_ants,
    iterations,
    evaporation_rate,
    size,
    storage_count,
    seeds
):

    results = []

    for i, seed in enumerate(seeds):

        # FIX RANDOMNESS PER RUN
        set_seed(seed)

        pheromone = initial_pheromone(size)

        best_layout, pheromone, history = aco_algo(
            number_of_layout=num_ants,
            iteration=iterations,
            pheromone=pheromone,
            size=size,
            number_of_storage=storage_count,
            evaporation_rate=evaporation_rate
        )

        final_cost = history[-1]

        results.append({
            "run": i + 1,
            "seed": seed,
            "ants": num_ants,
            "iterations": iterations,
            "evaporation": evaporation_rate,
            "size": size,
            "storage": storage_count,
            "final_cost": final_cost
        })

    return results



# ANALYZE RESULTS (IF CODE RAN ALL)
def analyze(results):

    costs = [r["final_cost"] for r in results]

    summary = {
        "avg_cost": statistics.mean(costs),
        "best_cost": min(costs),
        "worst_cost": max(costs),
        "std_dev": statistics.stdev(costs) if len(costs) > 1 else 0
    }

    return summary


# SAVE CSV (important data excel sheets already given )
def save_csv(filename, data):

    keys = data[0].keys()

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)



# MAIN TESTING LOOP
def run_experiments():

    size = 10
    storage = 15
    iterations = 18

    ant_settings = [50,100,150, 300]
    evap_settings = [ 0.3,0.5,0.7, 0.9] #example run: 50 ants tested with evap of 0.3 18 generations for 30 runs each run different seed
    #long loop DO NOT RUN
    base_seed = 42
    seeds = [base_seed + i for i in range(30)]  #30 RUNS

    all_results = []

    for ants in ant_settings:
        for evap in evap_settings:

            print(f"\nRunning: ants={ants}, evap={evap}")

            results = run_single_setting(
                num_ants=ants,
                iterations=iterations,
                evaporation_rate=evap,
                size=size,
                storage_count=storage,
                seeds=seeds
            )

            summary = analyze(results)

            print("SUMMARY:", summary)

            # save per configuration
            filename = f"results_ants{ants}_evap{evap}.csv"
            save_csv(filename, results)

            all_results.append({
                "ants": ants,
                "evaporation": evap,
                **summary
            })

    # save summary table (only if all done DONT DO IT)
    save_csv("summary_table.csv", all_results)


# -----------------------------
if __name__ == "__main__":
    run_experiments()