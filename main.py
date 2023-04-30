import sympy  

# TODO do not input contradictions 
# TODO do not input tautologies

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
        self.clauses = set()
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
                self.literals[literal].add(new_clause) 
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
                    self.remove_atomic(list(clause.literals)[0])
                    break
                    
    def remove_atomic(self, literal):
        # The atomic must be true, hence all clauses containing it are removed
        true_clauses = self.literals[literal]
        for clause in true_clauses: 
            # We must remove all references to the clause that is removed 
            self.remove_clause(clause)
        # try: # TODO remove this ALSO MAYBE DONT DO THIS! 
        #     del self.literals[literal]
        # except: 
        #     print(f"These are the keys {self.literals.keys()}")
        #     print(f"THIS IS WHERE THE DEATH COMMENCES {self.literals}, {self.literals[literal]}")
        
        # Next all clauses containing the negation of the atomic are updated 
        if ~literal in self.literals:
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
        to_remove = set()
        for clause1 in self.literals[next_literal]:
            for clause2 in self.literals[~next_literal]:
                # Make the new clause 
                resolution = Resolution_Alg.full_resolution(clause1.literals, clause2.literals, next_literal)
                if resolution == set(): 
                    self.contradiction = True 
                elif resolution != True: 
                    self.add_clause(resolution)
                
                # remove the old clauses
                to_remove.add(clause2)
            to_remove.add(clause1)
        
        for clause in to_remove: 
            self.remove_clause(clause)
        
        return False # To indicate that we have modified the clauses 
        
    def check_for_contradictions(self): 
        # Check if any of the clauses are empty 
        while not self.contradiction: 
            self.unit_resolution() 
            
            if self.pop_literal(): 
                break 
        
        return not self.contradiction

class Belief_Revisor():
    def to_cnf(expression): 
        """
        # Takes in a sympy expression and returns it in CNF form (with removed tautology disjunctions)
        """
        # Make the set of clauses
        cnf = sympy.to_cnf(sympy.simplify(expression))
        if isinstance(cnf, sympy.And):
            disjunctions = set(cnf.args)
        else: 
            disjunctions = {cnf}
        
        # Remove trivial clauses # TODO deal with this a better way 
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

    def generate_weight(sentence): 
        """
        Put into CNF format, then take the smallest clause and set the weight to the number of litterals in this.
        This is to ensure that entrenchment postulates are satisfied. 

        Args:
            sentence (sympy.Symbol): the sentence for which a weight is to be generated
        
        Return: 
            weight (int): The weight of the sentence
        """
        cnf = Belief_Revisor.to_cnf(sentence)
        weight = min([len(clause) for clause in cnf])
        return weight
    
    # TODO do not deal with tautologies and contradictions this way     
    def check_if_tautology(sentence):
        """
        Args:
            sentence (sympy.Symbol): the sentence to be checked
        
        Return:
            bool: True if the sentence is a tautology, False otherwise
        """
        cnf = Belief_Revisor.to_cnf(sentence)
        # If the sentence is a tautology, and because the cnf removes all trivial clauses, then the set of claueses is empty
        if cnf == set():  
            return True 
        else: return False 

    def check_if_contradiction(sentence): 
        """
        Args:
            sentence (sympy.Symbol): the sentence to be checked
        
        Return:
            bool: True if the sentence is a contradiction, False otherwise
        """
        # Use resolution to check for contradictions
        list_of_clauses = Belief_Revisor.to_cnf(sentence)
        resolution = Resolution_Alg(list_of_clauses)
        reso = resolution.check_for_contradictions()
        return reso
        
    def check_contradiction_and_tautology(sentence):
        """
        Provide the user with feedback about their sentence. 
        """
        if Belief_Revisor.check_if_tautology(sentence):
            print(f"The sentence {sentence} is a tautology, hence it does not provide any information.")
            return True
        elif Belief_Revisor.check_if_contradiction(sentence):
            print(f"The sentence {sentence} is a contradiction, hence it can never be true.")
            return True
        return False
    
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
        self.counter = 0
        
        # Setup initial state
        for sentence in initial_state:
            # if Belief_Revisor.check_contradiction_and_tautology(sentence): # TODO maybe do this
            #     pass
            self.expansion(sentence)

        # Contract with nothing to check if the initial KB is satisfiable (that it is the same after contraction)
        if not self.contract(None): 
            print("You have given an unsatisfiable initial state. The knowledge base is reduced to:")
            print(self.KB)
        
    
    def expansion(self, new_sentence):
        """Adds the new sentence to KB (and assigns the prior)"""
        self.KB[new_sentence] = (Belief_Revisor.generate_weight(new_sentence), self.counter)
        self.counter += 1 
    
        
    def contract(self, new_sentence):
        """
        Builds the KB from 
        
        # Add new sentence to new_KB
        # List of weighed (sorted) clauses a, b, c, d 
        # CNF all sentences 
        # # Use resolution (to completion) on new_KB and a -> if contradiction remove a, otherwise add a to new_KB 
        # proceed to do it again with the rest.
        """
        # When contracting, one must add the negeted sentence to the KB
        if new_sentence != None:
            new_sentence = ~new_sentence
            # Add new_sentence to new KB
            new_KB = {new_sentence} 
            new_KB_cnf = Belief_Revisor.to_cnf(new_sentence) 
        else:
            new_KB = set()
            new_KB_cnf = []
        
        # sort clauses
        # sorted_KB = sorted(self.KB.keys(), key=lambda x: self.KB[x], reverse=True) 
        sorted_KB = sorted(self.KB.keys(), key=lambda x: (self.KB[x][0], -self.KB[x][1]), reverse=True)

        for sentence in sorted_KB:
            cnf = Belief_Revisor.to_cnf(sentence)
            temp = new_KB_cnf + cnf
            resolution = Resolution_Alg(temp)
            reso = resolution.check_for_contradictions()
            if reso == True: 
                new_KB.add(sentence)
                new_KB_cnf = temp
                
        # Check if the KB has changed
        changed = not (new_KB - {new_sentence}) == set(self.KB.keys())

        # Remove sentences in KB that are not in new_KB
        if changed:
            self.KB = {key: value for key, value in self.KB.items() if key in new_KB}

        return not changed 
        

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
   
    def entails(self, new_sentence):
        """
        See if KB entails "new_sentence"

        Args:
            new_sentence (sympy.Symbol): The sentence to check for entailment
        
        Returns:
            bool: True if KB entails "new_sentence", False otherwise
        """
        # Use resolution to see if KB and -new_sentence is unsatisfiable
        # Generate the CNF of -new_sentence and KB
        list_of_clauses = Belief_Revisor.to_cnf(~new_sentence)
        for sentence in self.KB.keys():
            cnf = Belief_Revisor.to_cnf(sentence)
            list_of_clauses += cnf
        
        # Use resolution to check for contradictions
        resolution = Resolution_Alg(list_of_clauses)
        reso = resolution.check_for_contradictions()
        
        return not reso # If there is a contradiction, then KB entails new_sentence, and we return True
   