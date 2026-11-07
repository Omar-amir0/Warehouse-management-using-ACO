# Warehouse Management Using Ant Colony Optimization

A Streamlit app that searches for low-cost warehouse layouts with Ant Colony Optimization (ACO). It also includes an exact-search option for small grids.

## How the algorithm works

A warehouse is an `N × N` grid containing one packing area (`P`), one shipping area (`H`), and a chosen number of storage areas (`S`). The cost function sums each storage cell's Manhattan distance from packing and to shipping, multiplies total travel distance by the travel-time factor, and adds a congestion penalty for adjacent storage cells.

ACO generates candidate layouts over repeated iterations. Packing and shipping are placed near the center. Storage cells are sampled using weights that combine each cell's pheromone level with a heuristic favoring locations nearer the doors. Each iteration retains the best 20% of candidates, reduces pheromone according to the evaporation rate, and reinforces the cells used by those elite layouts according to their costs. This makes promising locations more likely to be selected in later iterations. The app fixes the random seed for repeatable runs with the same settings.

The **Exact Search (max 5×5)** option enumerates packing, shipping, and storage placements and returns the lowest-cost layout found. It is limited to small grids because the number of combinations grows quickly. Symmetry breaking reduces duplicate work by considering packing positions in the top-left half of the grid.

## Run the app in VS Code

1. Open the repository folder in VS Code.
2. Choose **Terminal → New Terminal**.
3. Create and activate a virtual environment (recommended):

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install the app dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

5. Start the app from the repository root:

   ```powershell
   py -m streamlit run app.py
   ```

Streamlit prints a local URL, usually `http://localhost:8501`. In the app sidebar, select the warehouse size, storage count, algorithm, and evaporation rate, then click **Run Optimization**.

If PowerShell blocks virtual-environment activation, use Command Prompt and run `.venv\Scripts\activate.bat`, or skip activation and use your normal Python environment.

## Files

- `app.py` — Streamlit user interface and algorithm runner.
- `aco.py` — ACO search, pheromone updates, and exact-search implementation.
- `warehouse.py` — Layout generation and pheromone initialization.
- `evaluation.py` — Travel distance, congestion, and layout cost calculations.
- `test.py` — Interactive command-line experiment runner.
- `experiments.py` — Batch experiment code; runs can take a long time.
- `graphs.py` — Graphing helpers.
- `requirements.txt` — Python packages required by the app.
