import numpy as np
import matplotlib.pyplot as plt


def generate_heatmap(e, mat, title, save_path, color="blue"):
    if color == "green" or color == "red":
        x_labels = list(e.type_map.keys())
    else:
        x_labels = ["HP", "ATK", "DEF", "SPATK", "SPDEF", "SPEED"]
    y_labels = e.team.mem_names()
    fig, axis = plt.subplots()

    if color == "blue":
        clr_map = plt.cm.Blues
    if color == "green":
        clr_map = plt.cm.Greens
    if color == "red":
        clr_map = plt.cm.Reds

    axis.pcolor(mat, cmap=clr_map)

    axis.set_yticks(np.arange(mat.shape[0]) + 0.5, minor=False)
    axis.set_xticks(np.arange(mat.shape[1]) + 0.5, minor=False)
    for i in range(len(x_labels)):
        for j in range(len(y_labels)):
            axis.text(i, j, mat[j, i], ha="left", va="top", color="black")
    axis.invert_yaxis()
    axis.set_yticklabels(y_labels, minor=False)
    axis.set_xticklabels(x_labels, minor=False)

    # fig.set_size_inches(11.03, 3.5)
    # fig.set_size_inches(8, 3)
    fig.set_size_inches(6, 2)

    plt.title(title)
    plt.setp(axis.get_xticklabels(), rotation=24, ha="right", rotation_mode="anchor")
    plt.savefig(save_path, dpi=100, bbox_inches="tight")
