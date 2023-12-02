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


def visualize_data(absolute_data, relative_data):
    fig, ax = plt.subplots(figsize=(20, 20))
    absolute_averages = {alg: np.mean(times) for alg, times in absolute_data.items()}
    relative_averages = {alg: np.mean(times) for alg, times in relative_data.items()}

    labels = list(absolute_data.keys())
    x = np.arange(len(labels))
    absolute_averages_list = [absolute_averages[alg] for alg in labels]

    bars = ax.bar(x, absolute_averages_list, color=["blue", "green", "red", "purple"])

    ax.set_xlabel("Algorithm")
    ax.set_ylabel("Average Total Search Time (Seconds)")
    ax.set_title("Average Performance of Algorithms Over Iterations")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    # Adding both absolute and relative values on top of the bars
    for bar in bars:
        absolute_height = bar.get_height()
        alg = labels[bars.index(bar)]
        relative_height = relative_averages[alg]
        ax.annotate(f'{absolute_height:.2f}s\n({relative_height:.2f}%)',
                    xy=(bar.get_x() + bar.get_width() / 2, absolute_height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.show()
