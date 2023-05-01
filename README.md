# The Belief Revision Agent and the Resolution Algorithm
In this repository you will find an implementation of a Belief Revision Agent that is based upon the Resolution algorithm, made by Group 78 in the course 02180 Introduction to Artificial Intelligence F23.

# How to use an agent 
To make a new agent, simply import `Belief_Revisor` from `main.py`, then create an instance and give it an initial state that is a list of `sympy` sentences and the type of weight used when contracting. Here there are three choice that you can read about in our report (0: Least Informative, 1: Most Informative, 3: Entrenchment). 

Now you will be able to use `expansion`, `contract`, `revision` and `entails` on sentences you wish to do these operations with. 

# AGM postulates - How to test the implementation
Test the AGM postulates in `agm_contraction.py` and `agm_revision.py` by running `pytest agm_contraction.py` or  `pytest agm_revision.py`.

# Mastermind
Try out the game mastermind by importing `Mastermind` from `mastermind.py`. This agent only needs to be given the colors you want to use (any text will do), the code length and the answer. Then you can use `solve` for the agent to crack the code (with the belief base implementation). 