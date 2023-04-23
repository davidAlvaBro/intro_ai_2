import sympy  
import random

class Clause: 
        def __init__(self, literals) -> None:
            self.literals = literals
    
class Resolution_Alg:
    def full_resolution(clause1, clause2, literal):
       """# slide 29 of lecture 10 slides    """
       reso = clause1.union(clause2)
       reso -= {literal, ~literal}
       for literals in clause1:
            if ~literals in clause2 or (~literals in clause1 and literals in clause2): 
                return True
       return reso
    
    def __init__(self, initial_clauses) -> None:
        self.literals = {} 
        self.clauses = {} 
        self.contradiction = False
        
        # Add all the initial clauses to the datastructure
        for clause in initial_clauses:
            self.add_clause(clause)
        
        
    def add_clause(self, clause): 
        # Make and add the new clause 
        new_clause = Clause(clause)
        self.clauses.add(new_clause)
        
        # Add the clause to the literals dictionary
        for literal in clause: 
            if literal in self.literals: 
                self.literals[literal] = self.literals[literal].add(new_clause)
            else: 
                self.literals[literal] = {new_clause}
    
    def remove_clause(self, clause): 
        if not clause in self.clauses: 
            print("Trying to remove a clause that is not in the set of clauses") 
            pass
        
        # Remove the reference to the clause from the literals dictionary
        for literal in clause.literals: 
            self.literals[literal] = self.literals[literal] - {clause}
            if self.literals[literal] == set(): 
                del self.literals[literal] 
                
        # Remove the clause form the set of clauses 
        self.clauses = self.clauses - {clause}
    
    def unit_resolution(self): 
        # Deal with the atomic clauses 
        atomic_found = True
        while atomic_found: # As removing an atomic literal can introduce new, we must do this until there are no more
            atomic_found = False 
            for clause in self.clauses: 
                if len(clause.literals) == 1: 
                    atomic_found = True 
                    self.remove_atomic(clause.literals[0])
                    
    def remove_atomic(self, literal):
        # The atomic must be true, hence all clauses containing it are removed
        true_clauses = self.literals[literal]
        for clause in true_clauses: 
            # We must remove all references to the clause that is removed 
            self.remove_clause(clause)
        del self.literals[literal]
        
        # Next all clauses containing the negation of the atomic are updated 
        clauses = self.literals[~literal]
        for clause in clauses:
            clause.literals = clause.literals - {~literal}
            if clause.literals == set():
                self.contradiction = True # If we get an empty clause, we have a contradiction and the clauses are unsatisfiable
        del self.literals[~literal]
    
    def pop_literal(self):
        # Find a pair where both the literal and its negation are in the set
        next_literal = None
        for literal in self.literals.keys():
            if ~literal in self.literals.keys(): 
                next_literal = literal
                break 
        
        # If there is such a pair we are done
        if next_literal == None: 
            return True 
        
        # Else we must use resolution to remove it
        to_remove = {}
        for clause1 in self.literals[next_literal]:
            for clause2 in self.literals[~next_literal]:
                # Make the new clause 
                resolution = Resolution_Alg.full_resolution(clause1, clause2)
                if resolution == set(): 
                    self.contradiction = True 
                elif resolution != True: 
                    self.add_clause(resolution)
                
                # remove the old clauses
                to_remove = to_remove.add(clause2)
            to_remove = to_remove.add(clause1)
        
        for clause in to_remove: 
            self.remove_clause(clause)
        
        return False # To indicate that we have modified the clauses 
        
    def check_for_contradictions(self): 
        # Check if any of the clauses are empty 
        while not self.contradiction: 
            self.unit_resolution() 
            
            if self.pop_literal(): 
                break 
        
        return self.contradiction




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

        # disjunctions = [set(disjunction.args) for disjunction in disjunctions]
        disjunction_sets = []
        for disjunction in disjunctions:
            # If disjunction is a single literal, wrap it in a set
            if isinstance(disjunction, sympy.Symbol) or isinstance(disjunction, sympy.Not):
                disjunction_sets.append({disjunction})
            # If disjunction is a disjunction of literals, split it at "|" operators and convert to a set
            else:
                disjunction_sets.append(set(disjunction.args))

        return disjunction_sets

    
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
            temp = new_KB_cnf + cnf
            reso = self.resolution_alg(temp)
            if reso == True: 
                new_KB.add(sentence)
                new_KB_cnf = temp

        # Remove sentences in KB that are not in new_KB
        self.KB = {key: value for key, value in self.KB.items() if key in new_KB}
    
        

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
   
   
   