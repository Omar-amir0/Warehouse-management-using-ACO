import pandas as pd
import matplotlib.pyplot as plt

# load data
df = pd.read_csv("summary_table_heuristics.csv")

#Evaporation vs Avg Cost
plt.figure()
for ants in sorted(df["ants"].unique()):
    subset = df[df["ants"] == ants]
    plt.plot(subset["evaporation"], subset["avg_cost"], marker='o', label=f"Ants={ants}")

plt.xlabel("Evaporation Rate")
plt.ylabel("Average Cost")
plt.title("Evaporation Rate vs Average Cost")
plt.legend()
plt.grid()
plt.savefig("graph_evap_vs_cost.png")
plt.show()


#Ants vs Avg Cost
plt.figure()
for evap in sorted(df["evaporation"].unique()):
    subset = df[df["evaporation"] == evap]
    plt.plot(subset["ants"], subset["avg_cost"], marker='o', label=f"Evap={evap}")

plt.xlabel("Number of Ants")
plt.ylabel("Average Cost")
plt.title("Number of Ants vs Average Cost")
plt.legend()
plt.grid()
plt.savefig("graph_ants_vs_cost.png")
plt.show()



#Stability (standard deviation comparison)
plt.figure()
for ants in sorted(df["ants"].unique()):
    subset = df[df["ants"] == ants]
    plt.plot(subset["evaporation"], subset["std_dev"], marker='o', label=f"Ants={ants}")

plt.xlabel("Evaporation Rate")
plt.ylabel("Standard Deviation")
plt.title("Stability Analysis (Lower means more Stable)")
plt.legend()
plt.grid()
plt.savefig("graph_stability.png")
plt.show()


#Best Cost Comparison
plt.figure()
for ants in sorted(df["ants"].unique()):
    subset = df[df["ants"] == ants]
    plt.plot(subset["evaporation"], subset["best_cost"], marker='o', label=f"Ants={ants}")

plt.xlabel("Evaporation Rate")
plt.ylabel("Best Cost")
plt.title("Best Cost Achieved")
plt.legend()
plt.grid()
plt.savefig("graph_best_cost.png")
plt.show()