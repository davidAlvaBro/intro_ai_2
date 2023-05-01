from main import *
import numpy as np
from typing import Iterable, List, Tuple
from tqdm import tqdm
from matplotlib import pyplot as plt
import pickle
import os



def prepare_raw_data(raw_data, threshold):
    """
        data = dict(ratio_possible_worlds=ratio_possible_worlds,
                  ground_truth_KB=ground_truth_KB,
                  generated=generated, values=values,
                  literals=literals)
    """
    mask = raw_data["values"] >= threshold
    raw_data["generated"] = raw_data["generated"][mask][:,0]
    raw_data["values"] = raw_data["values"][mask]
    raw_data["size"] = sum(mask)


def load_dataset(path, threshold):
    with open(path, "rb") as f:
        data = pickle.load(f)
    prepare_raw_data(data, threshold)
    return data

def load_datasets(paths, threshold):
    datasets = []
    for path in paths:
        datasets.append(load_dataset(path, threshold))
    return datasets

def combine_datasets_sentences(*datasets, max_n_sentences=None):
    max_n_sentences = max_n_sentences or min([dataset["size"] for dataset in datasets])
    max_n_sentences = min(max_n_sentences, min([dataset["size"] for dataset in datasets]))

    sentences = np.concatenate(tuple([dataset["generated"][:max_n_sentences] for dataset in datasets]))
    # ground_truth_KB = np.array([0]*len(dataset1["generated"]) + [1]*len(dataset2["generated"]))
    ground_truth_KBs = np.concatenate(tuple([dataset["ground_truth_KB"]]*max_n_sentences for i, dataset in enumerate(datasets)))
    return sentences, ground_truth_KBs

def run_revision(sentences, ground_truth_KBs, weight_types = (0,1)):
    """
    return KB_worlds_ratios, KB_and_ground_truth_worlds_ratios, count_removeds
        - all 2d arrays of shape (len(sentences), len(weight_types)) 

    """
    BRs = []
    KB_worlds_ratios = []
    KB_and_ground_truth_worlds_ratios = []
    count_removeds = []

    # instantiate Belief Revisors
    for weight_type in weight_types:
        BRs.append(Belief_Revisor(initial_state=[], weight_type=weight_type))

    # revise KBs
    # loop over senteces and corresponding ground truths
    for i in tqdm(range(len(sentences)), desc=f"Revising KBs"):
        sentence = sentences[i]
        ground_truth_KB = ground_truth_KBs[i]

        # prepare data arrays
        KB_worlds_ratio = []
        KB_and_ground_truth_worlds_ratio = []
        count_removed = []

        # loop over Belief Revisors
        for j in range(len(weight_types)):
            count_removed.append(BRs[j].revision(sentence)[1])
            KB_worlds_ratio.append(Belief_Revisor.generate_weight(sympy.And(*BRs[j].KB.keys()), 0))
            KB_and_ground_truth_worlds_ratio.append(Belief_Revisor.generate_weight(sympy.And(*BRs[j].KB.keys(), ground_truth_KB), 0))

        KB_worlds_ratios.append(KB_worlds_ratio)
        KB_and_ground_truth_worlds_ratios.append(KB_and_ground_truth_worlds_ratio)
        count_removeds.append(count_removed)
        
        # print(f"weight_type={weight_type}")
        # print("ratio worlds belief:                   ", Belief_Revisor.generate_weight(sympy.And(*BR.KB.keys()), 0))
        # print("ratio worlds belief and ground truth:  ", Belief_Revisor.generate_weight(sympy.And(*BR.KB.keys(),ground_truth_KB), 0))
    
    # convert to numpy arrays
    KB_worlds_ratios = np.array(KB_worlds_ratios)
    KB_and_ground_truth_worlds_ratios = np.array(KB_and_ground_truth_worlds_ratios)
    count_removeds = np.array(count_removeds)

    return KB_worlds_ratios, KB_and_ground_truth_worlds_ratios, count_removeds, BRs

def run_experiment(threshold, datasets, experiment_id, weight_types = (0,1), wrong_sentence_index=None, max_n_sentences=None):

    sentences, ground_truth_KBs = combine_datasets_sentences(*datasets, max_n_sentences=max_n_sentences)
    if wrong_sentence_index is not None:
        sentences[wrong_sentence_index] = sympy.Not(sentences[wrong_sentence_index])

    KB_worlds_ratios, KB_and_ground_truth_worlds_ratios, count_removeds, BRs = run_revision(sentences, ground_truth_KBs, weight_types)

    path = os.path.join("stats", f"{threshold}_id={experiment_id}")
    try: os.makedirs(path, exist_ok=False)
    except:
        print(f"folder {path} already exists")
        return
    
    np.save(os.path.join(path, "KB_worlds_ratios.npy"), KB_worlds_ratios)
    np.save(os.path.join(path, "KB_and_ground_truth_worlds_ratios.npy"), KB_and_ground_truth_worlds_ratios)
    np.save(os.path.join(path, "count_removeds.npy"), count_removeds)
    np.save(os.path.join(path, "ground_truth_KBs.npy"), ground_truth_KBs)
    np.save(os.path.join(path, "sentences.npy"), sentences)



def run_experiments(threshold, paths, n_experiments, weight_types = (0,1)):
    datasets = load_datasets(paths, threshold)
    for i in range(min(n_experiments, len(paths))):
        run_experiment(threshold, [datasets[i]], i, weight_types, max_n_sentences=80, wrong_sentence_index=20)

if __name__ == "__main__":

    paths = os.listdir("datasets")
    paths = [os.path.join("datasets", path) for path in paths]
    for threshold in [0.8, 0.9, 0.95, 0.98]:
        run_experiments(threshold, paths, 10, weight_types=(0,1))


    # a, b, c, d, e, f, g, h, i, j, k, l, m, n, o = sympy.symbols('a b c d e f g h i j k l m n o')
    # literals = (a, b, c, d, e, f, g, h, i, j, k, l, m, n, o)
    # literals = literals[:8]

    # threshold = 0.98

    # ground_truth_KB, tries = generate_random_sentence(literals, 6, 2)
    # ground_truth_worlds = np.array([x[1] for x in Belief_Revisor._compute_truth_tables(ground_truth_KB) if x[0] == True])

    # literals = tuple(ground_truth_KB.atoms(sympy.Symbol))


    # print("Ground Truth KB:")
    # print("sentence:        ", ground_truth_KB)
    # print("possible worlds: ", Belief_Revisor.generate_weight(ground_truth_KB, 0))

    # print("\n")
    # generated = np.array([generate_random_sentence(literals, np.random.randint(1,3),np.random.randint(2,4)) for _ in tqdm(range(1000), desc="Generating sentences")])
    # value = np.array([compute_sentence_value(sentence, ground_truth_worlds) for sentence, _ in tqdm(generated, desc="Generating values")])
    # generated = generated[value >= threshold]

    # print(len(generated), "sentences generated")
    # print("Average value:    ", np.mean(value))
    # print("consistent: ", np.sum(value >= threshold))
    # sentences, triess = map(list, zip(*generated))
    # initial_KB = [sentences.pop(0)]

    # weight_types = (0,1)

    # scores = []
    # count_removedss = []

    # BRs = []
    # for weight_type in weight_types:
    #     BRs.append(Belief_Revisor(initial_state=initial_KB, weight_type=weight_type))
    # for sentence in tqdm(sentences, desc=f"Revising KBs"):
    #     score = []
    #     count_removeds = []
    #     for i in range(len(weight_types)):
    #         changed, count_removed = BRs[i].revision(sentence)
    #         count_removeds.append(count_removed)
    #         score.append([Belief_Revisor.generate_weight(sympy.And(*BRs[i].KB.keys(),ground_truth_KB), 0), Belief_Revisor.generate_weight(sympy.And(*BRs[i].KB.keys()), 0)])
    #     scores.append(score)
    #     count_removedss.append(count_removeds)
        
    #     # print(f"weight_type={weight_type}")
    #     # print("ratio worlds belief:                   ", Belief_Revisor.generate_weight(sympy.And(*BR.KB.keys()), 0))
    #     # print("ratio worlds belief and ground truth:  ", Belief_Revisor.generate_weight(sympy.And(*BR.KB.keys(),ground_truth_KB), 0))

    # path = os.path.join("stats", f"threshold={threshold}_-_n_generated={len(generated)}")
    # os.makedirs(path, exist_ok=True)
    
    # scores = np.array(scores)
    # np.save(os.path.join(path, "scores.npy"), scores)
    # count_removedss = np.array(count_removedss)
    # np.save(os.path.join(path, "count_removedss.npy"), count_removedss)

    # with open(os.path.join(path, "ground_truth_KB.pkl"), "wb") as f:
    #     pickle.dump(ground_truth_KB, f)
    # with open(os.path.join(path, "generated.pkl"), "wb") as f:
    #     pickle.dump(generated, f)


    
