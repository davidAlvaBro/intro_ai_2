import sympy  
import random

class Belief_Revisor():
    def to_cnf(expression): 
        """
        # Takes in a sympy expression and returns it in CNF form (with removed tautology disjunctions)
        """
        # Make the set of clauses
        cnf = sympy.to_cnf(sympy.simplify(expression))
        disjunctions = set(cnf.args)
        
        # Remove trivial clauses 
        to_remove = set()
        for clause in disjunctions: 
            if sympy.simplify(clause) == True: 
                to_remove.add(clause)
        disjunctions = disjunctions - to_remove
        
        disjunctions = set(set(disjunction.args) for disjunction in disjunctions)

        return disjunctions
    
    def full_resolution(clause1, clause2,literal):
       """# slide 29 of lecture 10 slides    """
       reso = clause1.union(clause2)
       reso -= {literal, ~literal}
       for literals in clause1:
            if ~literals in clause2 or (~literals in clause1 and literals in clause2): 
                return True
       return reso

    
    def __init__(self, initial_state) -> None:
        """
        Take in initial sentences and assign them weights and add them to KB
        Use belief revision to check that it is consistent
        """
        # the knowledge base
        # implemented as a dictionary with elements:
        # clause: probability
        # Initialization 
        self.KB = {}
        
        # Setup initial state
        for sentence in initial_state:
            self.expansion(sentence)

        # Contract with nothing to check if the initial KB is satisfiable
        if not self.contract(None): 
            print("You have given an unsatisfiable initial state. Please try again.") 
        
        
        # TODO: KB should initially be to_cnf(initial state).
        # maybe assert that initial state is consistent
        
    
    def expansion(self, new_sentence):
        """Adds the new sentence to KB (and assigns the prior)"""
        self.KB[new_sentence] = random.random() # TODO make this something that makes sense 
    
        
    def contract(self, new_sentence):
        """
        Builds the KB from 
        
        # Add new sentence to new_KB
        # List of weighed (sorted) clauses a, b, c, d 
        # CNF all sentences 
        # # Use resolution (to completion) on new_KB and a -> if contradiction remove a, otherwise add a to new_KB 
        # proceed to do it again with the rest.
        """
  

        # sort clauses
        sorted_KB = sorted(self.KB.keys(), key=lambda x: self.KB[x], reverse=True) 

        # Add new_sentence to new KB
        new_KB = set(new_sentence) 
        new_KB_cnf = Belief_Revisor.to_cnf(new_sentence)

        for sentence in sorted_KB:
            cnf = Belief_Revisor.to_cnf(sentence)
            temp = new_KB_cnf.union(cnf)
            reso = self.resolution_alg(temp)
            if reso == True: 
                new_KB.add(sentence)
                new_KB_cnf.union(cnf)

        # Remove sentences in KB that are not in new_KB
        self.KB = {key: value for key, value in self.KB.items() if key in new_KB}
        


    
    def resolution_alg(self, clauses):
        """
        Runs the resolution algorithm on the given clauses.
        
        Args:
            clauses (set): set of clauses to be resolved
        
        Returns: 
            valid (boolean): True if the clauses are satisfiable, False if a contradiction is found.
        """
        # Map of instances of each atomic variable 
        clauses_map = {} 
        atomic_clauses = []
        for clause in clauses: 
            for literal in clause.args: 
                if literal in clauses_map: 
                    clauses_map[literal] = clauses_map[literal].add(clause)
                else: 
                    clauses_map[literal] = set(clause)
            if clause == clause.args:
                atomic_clauses.append(clause)
                    
        while True: 
            # First atomic clauses are removed 
            for literal in atomic_clauses: 
                # All clauses containing the literal are true and hence removed
                for clause in clauses_map[literal]:
                    clauses.remove(clause) # TODO update the clauses_map 
                del clauses_map[literal]
                for clause in clauses_map[~literal]:
                    clauses.remove(clause) # TODO update the clauses_map 
                    clauses.add(clause - ~literal)
                
            
            next_literal = None 
            # Find a pair where both the literal and its negation are in the set
            for key in clauses_map.keys():
                if ~key in clauses_map.keys(): 
                    next_literal = key
                    break 
            
            # If there is such a pair use resolution to remove it 
            if next_literal: 
                for clause1 in clauses_map[next_literal]:
                    for clause2 in clauses_map[~next_literal]:
                        # Make the new clause 
                        reso = self.full_resolution(clause1, clause2)
                        
                        # Check if it is a trivial clause or empty clause 
                        
                        # TODO add this new clause to the clause set 
                        clauses.add(reso)
                        # TODO add this new clause to the count dictionary 
                        
                # TODO remove the clause from the count dictionary 
                        
                        else: 
                            clauses.add(reso)
                            for literal in reso.args: 
                                if literal in clauses_map: 
                                    clauses_map[literal] = clauses_map[literal].add(reso)
                                else: 
                                    clauses_map[literal] = set(reso)
        
        

    def revision(self, new_sentence):
        """
        Modifies the KB to include the new sentence: 
        Use contraction on "-new_sentence" 
        Use expansion on "new_sentence"
        """
        # Contract 
        self.contract(~new_sentence)
        
        # Expand
        self.expansion(new_sentence)
        
    
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
        