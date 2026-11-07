import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from warehouse import set_seed, initial_pheromone, print_layout
from aco import aco_algo, iterative_algo

# ======================
# UI CONFIG
# ======================
st.set_page_config(page_title="ACO Warehouse Optimizer", layout="wide")

st.title(" Ant Colony Optimization - Warehouse")

# SIDEBAR user input
# ======================
st.sidebar.header(" settings")

size = st.sidebar.slider("Warehouse Size (NxN)", 2, 20, 10)
storage = st.sidebar.slider("Storage Units", 1, size*size - 2, 2)
algorithm = st.sidebar.selectbox(
    "Choose Algorithm",
    ["ACO", "Exact Search (max 5x5)"]
)

ants = 150
iterations = 18 #changed

evap = st.sidebar.slider("Evaporation Rate", 0.1, 0.9, 0.5)

run = st.sidebar.button("Run Optimization")

# ======================
# MAIN
# ======================
if run:
    st.subheader("Running Optimization...")

    set_seed(42)
    pheromone = initial_pheromone(size)

    # ======================
    # ACO
    # ======================
    if algorithm == "ACO":

        best_layout, pheromone, history , aco_time= aco_algo(
            number_of_layout=ants,
            iteration=iterations,
            pheromone=pheromone,
            size=size,
            number_of_storage=storage,
            evaporation_rate=evap
        )

        col1, col2 = st.columns(2)

        # GRAPH
        with col1:
            st.subheader("Convergence")

            fig, ax = plt.subplots()
            ax.plot(range(1, len(history)+1), history)
            ax.set_xlabel("Iteration")
            ax.set_ylabel("Best Cost")
            ax.set_xticks(range(1, len(history)+1))
            ax.grid()

            st.pyplot(fig)

        # LAYOUT
        with col2:
            st.subheader("Best Layout")

            color_map = {" ": 0, "S": 1, "P": 2, "H": 3}
            grid = np.array([[color_map[cell] for cell in row] for row in best_layout])

            fig2, ax2 = plt.subplots()
            ax2.imshow(grid)
            st.pyplot(fig2)

        st.success(f"Best Cost: {min(history)}")
        st.info(f"ACO time: {aco_time:.2f} seconds")

    # ===================================================================
    # iterative
    
    else:


            best_layout, _, history, iter_time, iter_eval = iterative_algo(
                size=size,
                number_of_storage=storage
            )

            col1, col2 = st.columns(2)

            # LAYOUT ONLY
            with col1:
                st.subheader("Optimal Layout")

                color_map = {" ": 0, "S": 1, "P": 2, "H": 3}
                grid = np.array([[color_map[cell] for cell in row] for row in best_layout])

                fig, ax = plt.subplots()
                ax.imshow(grid)
                st.pyplot(fig)

            # COST
            with col2:
                st.subheader("Optimal Cost")
                st.success(f"{history[0]}")
                st.info(f"Algorithm time: {iter_time:.2f} seconds")
                st.metric("Evaluations:", iter_eval)