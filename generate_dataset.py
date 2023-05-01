from main import *
import numpy as np
from typing import Iterable, List, Tuple
from tqdm import tqdm
from matplotlib import pyplot as plt
import pickle
import os

def generate_random_clause_list(literals: Tuple[sympy.Symbol], n_literals: int = None):
    """
    literals: list of literals
    n_literals: number of literals in the clause
    """
    n_literals = n_literals if n_literals else np.random.randint(1, len(literals))
    assert n_literals <= len(literals), "n_literals must be less than or equal to the number of literals"
    clause = []
    idx = np.random.choice(len(literals), n_literals, replace=False)
    for literal in np.random.choice(literals, n_literals, replace=False):
        true = np.random.choice([True, False])
        if true: clause.append(literal)
        else: clause.append(sympy.Not(literal))
    return clause

def generate_random_sentence(literals: Tuple[sympy.Symbol], n_clauses=2, n_literals_pr_clause=3):
    """
    literals: list of literals
    ground_truth_KB: list of clauses
    consistent: whether the sentence should be consistent with the KB
    n_clauses: number of clauses in the sentence
    """

    def helper(literals, n_clauses, n_literals_pr_clause):

        n_literals_pr_clause = min(n_literals_pr_clause, len(literals))

        clauses = []
        for _ in range(n_clauses):
            clause = generate_random_clause_list(literals, n_literals_pr_clause)
            clauses.append(sympy.Or(*clause))
        
        sentence = sympy.And(*clauses)
        return sentence
    
    for tries in range(100):
        sentence = helper(literals, n_clauses, n_literals_pr_clause)
        if check_satisfiability(sentence):
            return sentence, tries+1
    
    raise Exception("Could not generate a consistent sentence")

def check_satisfiability(sentence, ground_truth_KB=sympy.true):
    """returns True if the sentence is consistent with the KB, False otherwise"""
    # return not Belief_Revisor.check_if_contradiction(sympy.And(sentence, ground_truth_KB))
    return sympy.satisfiable(sympy.And(sentence, ground_truth_KB)) is not False


def compute_sentence_value(sentence: sympy.Basic, ground_truth_worlds):
    func = np.vectorize(lambda x: sentence.subs(x) == True)
    return np.mean(func(ground_truth_worlds))


def generate_random_sentences(ground_truth_KB: sympy.Basic, min_clauses, max_clauses, min_literals, max_literals, n_sentences):
    literals = tuple(ground_truth_KB.atoms(sympy.Symbol))
    ground_truth_worlds = np.array([x[1] for x in Belief_Revisor._compute_truth_tables(ground_truth_KB) if x[0] == True])
    
    generate_func = lambda: generate_random_sentence(literals, np.random.randint(min_clauses,max_clauses+1), np.random.randint(min_literals,max_literals+1))
    generated = np.array([generate_func() for _ in tqdm(range(n_sentences), desc="Generating sentences")])

    # compute_values_func = np.vectorize(lambda x: compute_sentence_value(x, ground_truth_worlds))
    values = np.array([compute_sentence_value(sentence, ground_truth_worlds) for sentence, _ in tqdm(generated, desc="Generating values")])
    # values = compute_values_func(generated[:,0])

    return generated, values



def generate_dataset(ground_truth_params=dict(n_clauses=6, n_literals_pr_clause=2),
                     random_sentences_params=dict(min_clauses=1, max_clauses=3, min_literals=2, max_literals=3, n_sentences=1000),
                     max_n_literals=8):
    
    literals = (a, b, c, d, e, f, g, h, i, j, k, l, m, n, o) = sympy.symbols('a b c d e f g h i j k l m n o')
    max_n_literals = max(max_n_literals, len(literals))
    literals = literals[:max_n_literals]

    ground_truth_KB, tries = generate_random_sentence(literals, **ground_truth_params)

    literals = tuple(ground_truth_KB.atoms(sympy.Symbol))

    ratio_possible_worlds = Belief_Revisor.generate_weight(ground_truth_KB, 0)
    generated, values = generate_random_sentences(ground_truth_KB, **random_sentences_params)
    output = dict(ratio_possible_worlds=ratio_possible_worlds,
                  ground_truth_KB=ground_truth_KB,
                  generated=generated,
                  values=values,
                  literals=literals)
    n_above_90pct = np.sum(values >= 0.9)

    # name = f"ratio_possible_worlds={ratio_possible_worlds}_ground_truth_KB={ground_truth_KB}.pickle".replace("|", "or")
    name = f"ratio_possible_worlds={ratio_possible_worlds}_n_above_90pct={n_above_90pct}_ground_truth_KB={ground_truth_KB}.pickle".replace("|", "or")
    path = os.path.join("datasets", name)
    with open(path, "wb") as f:
        pickle.dump(output, f)

    return output

if __name__ == "__main__":

    for i in range(10):
        print(f"Generating dataset {i+1}")
        ratio_possible_worlds, ground_truth_KB, generated, values, literals = generate_dataset().values()
