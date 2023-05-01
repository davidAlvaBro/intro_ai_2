from matplotlib import pyplot as plt
import numpy as np
import pickle
from generate_dataset import *
from collections import defaultdict


if __name__ == "__main__":

    paths = os.listdir("stats")
    paths = [os.path.join("stats", path) for path in paths]
    paths = [path for path in paths if os.path.isdir(path)]



    n_sentences = 40

    experiments = defaultdict(lambda: defaultdict(list))

    max_experiments = 0





    for path in paths:

        threshold = float(os.path.basename(path).split("_")[0])
        ground_truth_KB = np.load(os.path.join(path, "ground_truth_KBs.npy"), allow_pickle=True)[0]
        KB_worlds_ratios = np.load(os.path.join(path, "KB_worlds_ratios.npy"), )
        KB_and_ground_truth_worlds_ratios = np.load(os.path.join(path, "KB_and_ground_truth_worlds_ratios.npy"), )
        KB_sizes = np.load(os.path.join(path, "count_removeds.npy"), )

            
        experiments[threshold]["ground_truth_KB"].append(ground_truth_KB)
        experiments[threshold]["KB_worlds_ratios"].append(KB_worlds_ratios[:n_sentences])
        experiments[threshold]["KB_and_ground_truth_worlds_ratios"].append(KB_and_ground_truth_worlds_ratios[:n_sentences])
        experiments[threshold]["KB_sizes"].append(KB_sizes[:n_sentences])

    # for threshold, data in experiments.items():
    #         data["KB_worlds_ratios"] = np.array(data["KB_worlds_ratios"])
    #         data["KB_and_ground_truth_worlds_ratios"] = np.array(data["KB_and_ground_truth_worlds_ratios"])
    #         data["KB_sizes"] = np.array(data["KB_sizes"])
    #         max_experiments = max(max_experiments, len(data["KB_worlds_ratios"]))


    KB_worlds_ratios = experiments[0.95]["KB_worlds_ratios"][6]
    for i, alpha, thickness in zip(range(3), [0.2, 0.5, 1], [5,3,1]):
        plt.plot(KB_worlds_ratios[:, i], label=f"weight_type {i}", alpha=alpha, linewidth=thickness)
    
    plt.xlabel("Sentence number")
    plt.ylabel("Satisfiability ratio")
    plt.legend()

    plt.suptitle("Ground truth, threshold 0.95")

    plt.savefig("KB_worlds_ratios_example.png")
    plt.show()


    KB_and_ground_truth_worlds_ratios = experiments[0.95]["KB_and_ground_truth_worlds_ratios"][6]
    for i, alpha, thickness in zip(range(3), [0.2, 0.5, 1], [5,3,1]):
        plt.plot(KB_and_ground_truth_worlds_ratios[:, i], label=f"weight_type {i}", alpha=alpha, linewidth=thickness)
    
    plt.xlabel("Sentence number")
    plt.ylabel("Satisfiability ratio")
    plt.legend()

    plt.suptitle("Ground truth $\wedge$ belief base, threshold 0.95")
    plt.savefig("KB_and_ground_truth_worlds_ratios_example.png")
    plt.show()


    fig = plt.figure(figsize=(10,10))

    for thr_idx, (threshold, data) in enumerate(sorted(experiments.items(), key=lambda x: x[0])):
        KB_worlds_ratios = data["KB_worlds_ratios"]
        # KB_and_ground_truth_worlds_ratios = data["KB_and_ground_truth_worlds_ratios"]
        # KB_sizes = data["KB_sizes"]

        for j, exp in enumerate(KB_worlds_ratios):
            if len(exp) < n_sentences: continue
            fig.add_subplot(len(KB_worlds_ratios), len(experiments), len(experiments)*j+thr_idx+1)
            for i, alpha, thickness in zip(range(3), [0.2, 0.5, 1], [5,3,1]):
                plt.plot(exp[:, i], label=f"weight_type {i}", alpha=alpha, linewidth=thickness)

            
            ground_truth_KB = data["ground_truth_KB"][j]
            w = Belief_Revisor.generate_weight(ground_truth_KB, 0)
            plt.plot([0, n_sentences], [w, w], label="ground_truth", alpha=0.5, linewidth=1, linestyle="--", color="black")

            plt.ylim(0,0.6)
            
            if j == 0:
                plt.title(f"threshold {threshold}")
            
            if j == 0 and thr_idx == 0:
                plt.legend()
            else:
                plt.yticks([])
            
            if j == len(KB_worlds_ratios) - 1 and thr_idx == 0:
                pass
            else:
                plt.xticks([])
    
    plt.tight_layout()
    plt.show()
    plt.savefig("KB_worlds_ratios.png")


    fig = plt.figure(figsize=(10,10))

    for thr_idx, (threshold, data) in enumerate(sorted(experiments.items(), key=lambda x: x[0])):
        KB_and_ground_truth_worlds_ratios = data["KB_and_ground_truth_worlds_ratios"]

        for j, exp in enumerate(KB_and_ground_truth_worlds_ratios):
            if len(exp) < n_sentences: continue
            fig.add_subplot(len(KB_and_ground_truth_worlds_ratios), len(experiments), len(experiments)*j+thr_idx+1)
            for i, alpha, thickness in zip(range(3), [0.2, 0.5, 1], [5,3,1]):
                plt.plot(exp[:, i], label=f"weight_type {i}", alpha=alpha, linewidth=thickness)

            
            ground_truth_KB = data["ground_truth_KB"][j]
            w = Belief_Revisor.generate_weight(ground_truth_KB, 0)
            plt.plot([0, n_sentences], [w, w], label="ground_truth", alpha=0.5, linewidth=1, linestyle="--", color="black")

            plt.ylim(0,0.3)
            
            if j == 0:
                plt.title(f"threshold {threshold}")
            
            if j == 0 and thr_idx == 0:
                plt.legend()
            else:
                plt.yticks([])
            
            if j == len(KB_and_ground_truth_worlds_ratios) - 1 and thr_idx == 0:
                pass
            else:
                plt.xticks([])
    
    plt.tight_layout()
    plt.savefig("KB_and_ground_truth_worlds_ratios.png")
    plt.show()



    fig = plt.figure(figsize=(10,10))

    for thr_idx, (threshold, data) in enumerate(sorted(experiments.items(), key=lambda x: x[0])):
        KB_worlds_ratios = data["KB_worlds_ratios"]
        # KB_and_ground_truth_worlds_ratios = data["KB_and_ground_truth_worlds_ratios"]
        # KB_sizes = data["KB_sizes"]

        for j, exp in enumerate(KB_worlds_ratios):
            if len(exp) < n_sentences: continue
            fig.add_subplot(len(KB_worlds_ratios), len(experiments), len(experiments)*j+thr_idx+1)
            for i, alpha, thickness in zip(range(3), [0.2, 0.5, 1], [5,3,1]):
                plt.plot(exp[:, i], label=f"weight_type {i}", alpha=alpha, linewidth=thickness)

            
            ground_truth_KB = data["ground_truth_KB"][j]
            w = Belief_Revisor.generate_weight(ground_truth_KB, 0)
            plt.plot([0, n_sentences], [w, w], label="ground_truth", alpha=0.5, linewidth=1, linestyle="--", color="black")

            plt.ylim(0,0.6)
            
            if j == 0:
                plt.title(f"threshold {threshold}")
            
            if j == 0 and thr_idx == 0:
                plt.legend()
            else:
                plt.yticks([])
            
            if j == len(KB_worlds_ratios) - 1 and thr_idx == 0:
                pass
            else:
                plt.xticks([])
    
    plt.tight_layout()
    plt.savefig("KB_worlds_ratios.png")
    plt.show()



    fig = plt.figure(figsize=(10,10))

    max_KB_size = max((data["KB_sizes"]) for data in experiments.values())

    for thr_idx, (threshold, data) in enumerate(sorted(experiments.items(), key=lambda x: x[0])):
        KB_sizes = data["KB_sizes"]

        for j, exp in enumerate(KB_sizes):
            if len(exp) < n_sentences: continue
            fig.add_subplot(len(KB_sizes), len(experiments), len(experiments)*j+thr_idx+1)
            for i, alpha, thickness in zip(range(3), [0.2, 0.5, 1], [5,3,1]):
                plt.plot(exp[:, i], label=f"weight_type {i}", alpha=alpha, linewidth=thickness)

            # ground_truth_KB = data["ground_truth_KB"][j]
            # w = Belief_Revisor.generate_weight(ground_truth_KB, 0)
            # plt.plot([0, n_sentences], [w, w], label="ground_truth", alpha=0.5, linewidth=1, linestyle="--", color="black")

            plt.ylim(0,30)
            
            if j == 0:
                plt.title(f"threshold {threshold}")
            
            if j == 0 and thr_idx == 0:
                plt.legend()
            else:
                plt.yticks([])
            
            if j == len(KB_sizes) - 1 and thr_idx == 0:
                pass
            else:
                plt.xticks([])
    
    plt.tight_layout()
    plt.show()
    plt.savefig("KB_sizes.png")


