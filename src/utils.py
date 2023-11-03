import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


def visualize_warehouse(warehouse, path=None):
    fig, ax = plt.subplots(figsize=(10, 10))

    fig.patch.set_facecolor("#22272e")
    ax.set_facecolor("#22272e")

    # Convert the warehouse matrix into a numpy array
    warehouse_np = np.array(warehouse)

    cmap = mcolors.ListedColormap(["#000000", "#282c34"])
    ax.imshow(warehouse_np, cmap=cmap, aspect="equal")

    if path:
        # Unzip the path into x and y coordinates
        ys, xs = zip(*path)
        # A scatter plot for visualiation
        ax.plot(xs, ys, "o-", color="#61afef", markersize=1, markeredgecolor="#61afef")

        # Start point
        ax.text(xs[0], ys[0], "S", ha="center", va="center", color="white", fontsize=12)
        # End point
        ax.text(
            xs[-1], ys[-1], "E", ha="center", va="center", color="white", fontsize=12
        )

    ax.grid(which="both", color="#22272e", linestyle="-", linewidth=1)

    plt.show()