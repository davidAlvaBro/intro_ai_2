from matplotlib import pyplot as plt
import numpy as np
import pickle
from generate_dataset import *

def plotter(scores, ground_truth_KB, name):

    w = Belief_Revisor.generate_weight(ground_truth_KB, 0)

    # plt.plot(scores[:,0,0], label="weight_type=0, KB$\wedge$ground_truth_KB", linewidth=4)
    # plt.plot(scores[:,1,0], label="weight_type=1, KB$\wedge$ground_truth_KB", linewidth=3)
    plt.plot(scores[:,0,1], label="weight_type=0, KB", linewidth=2)
    plt.plot(scores[:,1,1], label="weight_type=1, KB", linewidth=1)
    plt.plot([0, len(scores)], [w, w], label="ground_truth_KB")
    # plt.yscale("log")
    plt.legend()
    plt.ylim(0,0.4)
    plt.suptitle(name)

    plt.show()

def load_stats(path):
    scores = np.load(os.path.join(path, "scores.npy"))
    try: count_removedss = np.load(os.path.join(path, "count_removedss.npy"))
    except: count_removedss = np.zeros(scores.shape[:-1])

    with open(os.path.join(path, "generated.pkl"), "rb") as f:
        generated = pickle.load(f)
    with open(os.path.join(path, "ground_truth_KB.pkl"), "rb") as f:
        ground_truth_KB = pickle.load(f)

    return scores, generated, ground_truth_KB, count_removedss

def plot_stats(path, name=None):
    scores, generated, ground_truth_KB, _ = load_stats(path)
    plotter(scores, ground_truth_KB, name or os.path.basename(path))

if __name__ == "__main__":
    paths = os.listdir("stats")
    paths = [os.path.join("stats", path) for path in paths]
    for path in paths:
        scores, generated, ground_truth_KB, count_removedss = load_stats(path)
        name = os.path.basename(path)
        print(name)
        print(sum(count_removedss))
        plotter(scores, ground_truth_KB, name)