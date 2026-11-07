# Warehouse Management Using Ant Colony Optimization

A Streamlit app for finding low-cost warehouse layouts with Ant Colony Optimization (ACO). The repository also contains a small exact-search option and saved experiment results.

## How the algorithm works

A layout is an N × N grid with one packing area (P), one shipping area (H), and a configurable number of storage areas (S). The objective function adds the Manhattan travel distance from packing to each storage location and from each storage location to shipping, multiplied by the travel-time factor, plus a congestion penalty for adjacent storage locations.

The ACO implementation generates candidate layouts each iteration. It places packing and shipping near the center, then chooses storage cells using a weighted random draw. Each cell's draw weight combines its pheromone level with a distance heuristic that favors cells nearer the two doors. The algorithm keeps the best 20% of layouts, evaporates pheromone across the grid using the selected evaporation rate, and reinforces cells occupied in elite layouts in proportion to their cost-based reward. Repeating this process biases later layouts toward promising cells. The random seed is fixed in the app so runs are reproducible for the same settings.

The **Exact Search (max 5×5)** option enumerates placements of packing, shipping, and storage and returns the lowest-cost layout it finds. It is intended only for grids up to 5×5 because the number of combinations grows rapidly. It uses symmetry breaking by considering packing positions in the top-left half of the grid.

## Start the app in VS Code

1. Open this repository folder in VS Code.
2. Open **Terminal → New Terminal** at the repository root.
3. (Recommended) Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

5. Start the app:

   ```powershell
   py -m streamlit run "codes and excel/app.py"
   ```

Streamlit will print a local URL (usually http://localhost:8501) to open in your browser. In the app sidebar, choose the warehouse size, number of storage units, algorithm, and evaporation rate, then click **Run Optimization**.

If PowerShell blocks virtual-environment activation, use Command Prompt in VS Code for activation with .venv\Scripts\activate.bat, or skip activation and run the install and launch commands with your normal Python environment.

## Repository layout

- codes and excel/app.py — Streamlit user interface and algorithm runner.
- codes and excel/aco.py — ACO search, pheromone updates, and exact-search implementation.
- codes and excel/warehouse.py — Warehouse layout generation and pheromone initialization.
- codes and excel/evaluation.py — Travel distance, congestion, and layout cost calculation.
- codes and excel/test.py — Interactive command-line experiment runner.
- codes and excel/experiments.py — Batch experiment code (can take a long time to run).
- codes and excel/Random generation Excel Sheets/ — Saved random-generation result tables and charts.
- codes and excel/Heuristic Excel Sheets/ — Saved heuristic result tables and charts.

The experiment CSV files and plots are retained in their original folders as recorded outputs; they are not required to run the Streamlit app.
