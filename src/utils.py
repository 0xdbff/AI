import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


def visualize_warehouse(warehouse, path=None):
    fig, ax = plt.subplots(figsize=(20, 20))

    fig.patch.set_facecolor("#212121")
    ax.set_facecolor("#212121")

    # Convert the warehouse matrix into a numpy array
    warehouse_np = np.array(warehouse)

    cmap = mcolors.ListedColormap(["#000000", "#282828"])
    ax.imshow(warehouse_np, cmap=cmap, aspect="equal")

    if path:
        # Unzip the path into x and y coordinates
        ys, xs = zip(*path)
        # A scatter plot for visualiation
        dimx, dimy = warehouse_np.shape

        if dimx * dimy < 20000:
            ax.plot(
                xs, ys, "o-", color="#61afef", markersize=4, markeredgecolor="#61afef"
            )
        else:
            ax.plot(
                xs, ys, "o-", color="#61afef", markersize=0, markeredgecolor="#61afef"
            )

        # Start point
        ax.text(xs[0], ys[0], "S", ha="center", va="center", color="white", fontsize=12)
        # End point
        ax.text(
            xs[-1], ys[-1], "E", ha="center", va="center", color="white", fontsize=12
        )

    ax.grid(which="both", color="#212121", linestyle="-", linewidth=1)

    plt.show()
