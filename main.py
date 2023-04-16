from sympy import symbol 

class Belief_Revisor():
    def __init__(self, initial_state) -> None:
        """
        # Take in initial sentences
        # Make them into clauses with sympy
        # run recalculate prior
        # ?Use belief revision to check that it is consistent?
        """
        
        
        self.atomic_priors = {}

        # the knowledge base
        # implemented as a dictionary with elements:
        # clause: probability
        # TODO: KB should initially be to_cnf(initial state).
        # maybe assert that initial state is consistent
        
        self.KB = {}
        
        
    def update(self, new_sentences):
        """
        # Take in new sentences 
        # Make it CNF 
        
        # TODO maybe not? run contraction 
        # TODO maybe not? run addition 
        
        # Just do this :
        # new_KB = {new_clause}
        # temp_clause = new_clause
        # Sort the clauses in the KB by probability
        # for clauses in the KB (sorted highest first): 
            # resolution = Belief_Revisor.full_resolution(temp_clause, clause) 
            # if resolution fails: continue 
            # else: 
                # temp_clause = resolution
                # new_KB.add(clause)
        # KB = new_KB
        # recalculate_prior()
        """
        
    def full_resolution(clause1, clause2):
       """# slide 29 of lecture 10 slides    """
    
    # def contract(self, new_clause):
        # TODO Do we need this? 
        
    # def expansion(self):
        # TODO do we need this?

    def resolution(self, new_clause): 
        """
        # Check if new_clause can be inferred from the KB 
        # This is done like slide 41 of lecture 10 slides
        # Convert new_clause to CNF
        # resolution = not new_clause
        # for clause in KB: 
            # resolution = Belief_Revisor.full_resolution(clause, resolution)
            # if resolution fails: return false 
        # return true 
        """
        

    def recalculate_prior(self):
        """
        # Count all the atomic variables in the KB (multiplied with inverse of length) (and same for negation)
        # Store counts in priors dictionary
        # Take sigmoid of difference of the two counts
        # Store this in the KB dictionary as values. 
        """
        
        # dictionary that stores the weighted counts of appearances for each atomic variable.
        atomic_counters = {}
        