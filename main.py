import sympy  

class Clause:
    # This datastructure is used to represent a clause in the resolution algorithm 
    def __init__(self, literals) -> None:
        self.literals = literals
    
class Resolution_Alg:
    # This class implements the resolution algorithm
    def full_resolution(clause1, clause2, literal):
        """
        Implementation of full resolution. 
        Combines two clauses and removes the literal and its negation that they share (literal).
        If there are more than one pair of literals that are negations of each other, the resoluting clause will be a tautology, hence return True

        Args:
            clause1 (set): The first clause (set of sympy.Symbols)
            clause2 (set): The second clause
            literal (sympy.Symbol): The literal to remove 
        
        Returns:
            set: The resulting clause (set of sympy.Symbols) or True if the resulting clause is a tautology
        """
        # Create new clause and remove the literal and its negation
        reso = clause1.union(clause2)
        reso -= {literal, ~literal}
        
        # Check if this new clause is a tautology 
        for literals in clause1:
                if ~literals in clause2 or (~literals in clause1 and literals in clause2): 
                    return True
        return reso
    
    def __init__(self, initial_clauses) -> None:
        # This datastructure is used to represent the set of clauses in the resolution algorithm
        self.literals = {} # This dictionary maps each literal to the set of clauses it is in to have easy access
        self.clauses = set()
        self.contradiction = False
        
        # Add all the initial clauses to the datastructure
        for clause in initial_clauses:
            self.add_clause(clause)
            
    def add_clause(self, clause): 
        """
        Function that adds a clause to the datastructure.

        Args:
            clause (set): set of literals (sympy.Symbols)
        """
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
        """
        Function that removes a clause from the datastructure.

        Args:
            clause (Clause): The clause to remove
        """
        # Check if the clause is in the resolution algorithm, otherwise an error has occured
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
        """
        Function that finds all atomic clauses and removes them from the datastructure, one after another. 
        """
        # Find all atomic clauses, but only removes them one by one to deal with new atomic clauses aswell
        atomic_found = True
        while atomic_found:
            atomic_found = False 
            for clause in self.clauses: 
                if len(clause.literals) == 1: 
                    atomic_found = True 
                    # Remove the atomic clause
                    self.remove_atomic(list(clause.literals)[0])
                    break
                    
    def remove_atomic(self, literal):
        """
        Function that removes an atomic clause from the datastructure by requirering it to be true,
        hence all other clauses containing it are trivially true and removed, 
        while formulas containing the negation of the atomic are updated. 
        
        Args: 
            literal (sympy.Symbol): The atomic clause to remove
        """
        # Removing all true clauses containing the atomic
        true_clauses = self.literals[literal]
        for clause in true_clauses: 
            self.remove_clause(clause)
            
        # Next all clauses containing the negation of the atomic are updated 
        if ~literal in self.literals:
            clauses = self.literals[~literal]
            for clause in clauses:
                # Remove the negation of the atomic from the clause
                clause.literals = clause.literals - {~literal}
                # If the clause is then empty, there is a contradiction
                if clause.literals == set():
                    self.contradiction = True 
            del self.literals[~literal]
    
    def pop_literal(self):
        """
        The main resolution algorithm. 
        This function finds a pair of literals where both the literal and its negation is in at least one clause.
        Then full resolution is applied to all pairs containing opposite versions of said literal. 
        If the resulting clause is empty, there is a contradiction and the algorithm terminates.
        Otherwise the resulting clause is added to the datastructure, and the old clauses are removed.
        
        Returns: 
            bool: True if the algorithm is done, False if it has modified the clauses and hence needs to run again 
        """
        # Find a pair where both the literal and its negation are in the set
        next_literal = None
        for literal in self.literals.keys():
            if ~literal in self.literals.keys(): 
                next_literal = literal
                break 
        
        # If there isn't such a pair the algorithm terminates
        if next_literal == None: 
            return True 
        
        # Full resolution is applied on all pairs containing opposite versions of the literal
        to_remove = set()
        for clause1 in self.literals[next_literal]:
            for clause2 in self.literals[~next_literal]:
                # Make the new clause 
                resolution = Resolution_Alg.full_resolution(clause1.literals, clause2.literals, next_literal)
                # Check if the resulting clause is an empty set, hence a contradiction
                if resolution == set(): 
                    self.contradiction = True 
                # Otherwise add the resulting clause to the datastructure
                elif resolution != True: 
                    self.add_clause(resolution)
                
                # remove the old clauses, but only after the loop is done, as other pairs still needs to be generated
                to_remove.add(clause2)
            # remove the old clauses, but only after the loop is done
            to_remove.add(clause1)
        
        # Remove old clauses 
        for clause in to_remove: 
            self.remove_clause(clause)
        
        # The algorithm is not done yet, hence return False
        return False
        
    def check_for_contradictions(self): 
        """
        The resolution algorithm. 
        When a contradiction happens the algorithm terminates and returns True. 
        First the algorithm removes atomic clauses, then full resolution is applied to clauses with pairs of opposite literals.
        This repeats itself until there are no more atomic clauses or such pairs exists. 
        
        Returns:
            bool: True if there is a contradiction, False otherwise
        """
        while not self.contradiction: 
            self.unit_resolution() 
            
            if self.pop_literal(): 
                break 
        
        return self.contradiction # TODO Fuck with not everywhere -> on it

class Belief_Revisor():
    def to_cnf(sentence): 
        """
        Takes in an sentence and returns the CNF version (with trivial clauses removed).
        The CNF is represented as a list of sets, where each entry in the list represent a clause,
        and each set contains all literals in said clause.
        
        Args: 
            sentence (sympy.Symbol): The sentence to be turned into CNF form 
        
        Returns: 
            disjunction_sets (list): Sentence in CNF form (list of disjunctions represented as sets)
        """
        # Make the set of clauses
        cnf = sympy.to_cnf(sentence)
        # cnf = sympy.to_cnf(sympy.simplify(sentence))
        if isinstance(cnf, sympy.And):
            disjunctions = set(cnf.args)
        else: 
            disjunctions = {cnf}
        
        # Remove trivial clauses
        to_remove = set()
        for clause in disjunctions: 
            for literals in clause.args:
                if ~literals in clause.args: 
                    to_remove.add(clause)
        disjunctions = disjunctions - to_remove

        # Make all clauses into sets (they are easier to work with)
        disjunction_sets = []
        for disjunction in disjunctions:
            # If disjunction is a single literal, wrap it in a set
            if isinstance(disjunction, sympy.Symbol) or isinstance(disjunction, sympy.Not):
                disjunction_sets.append({disjunction})
            # If disjunction is a disjunction of literals, split it at "|" operators and convert to a set
            else:
                disjunction_sets.append(set(disjunction.args))

        return disjunction_sets

    def generate_weight(sentence:sympy.Basic, weight_type): # TODO change this function to use different weights dependent on user input 
        """
        Put into CNF format, then take the smallest clause and set the weight to the number of litterals in this.
        This is to ensure that entrenchment postulates are satisfied. 

        Args:
            sentence (sympy.Symbol): the sentence for which a weight is to be generated
            weight_type (int): the type of weight to be generated:
                0: The weight is the fraction of possible worlds in which the sentence is true
                1: The weight is the fraction of possible worlds in which the sentence is false
                2: The weight is the estimated probability of the sentence being true
                        - This is done by using the approximated probabilities of the literals in the sentence.
        
        Return: 
            weight (int): The weight of the sentence
        """
        if weight_type == 0:
            worlds = list(Belief_Revisor._compute_truth_tables(sentence))
            return sum([x==True for x in worlds])/len(worlds)
        if weight_type == 1:
            worlds = list(Belief_Revisor._compute_truth_tables(sentence))
            return 1 - sum([x==True for x in worlds])/len(worlds)
        if weight_type == 2:
            raise NotImplementedError("Weight type 2 is not implemented yet")

    def _compute_truth_tables(sentence: sympy.Basic):
        """
        Compute the truth table for a sentence. 
        This is done by first converting the sentence to CNF form, then computing the truth table for each clause.
        The truth table for the sentence is then the conjunction of all these truth tables. 

        Args:
            sentence (sympy.Symbol): the sentence for which a truth table is to be generated
        
        Return: 
            truth_table (sympy.Symbol): the truth table for the sentence
        """

        def get_table(numvars):
            if numvars == 1:
                yield [True]
                yield [False]
            else:
                for i in get_table(numvars-1):
                    yield i + [True]
                    yield i + [False]

        literals = list(sentence.atoms(sympy.Symbol))

        for truth_values in get_table(len(literals)):
            values = dict(zip(literals,truth_values))
            yield sentence.subs(values)  

    def check_if_contradiction(sentence): 
        """
        Determine if a sentence is a contradiction with resolution
        
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
        Check for contradictions and tautologies, and provide the user with feedback if either is the case.
        
        Args: 
            sentence (sympy.Symbol): the sentence to be checked (given by user)
        
        Returns: 
            bool: True if the sentence is a tautology or contradiction, False otherwise        
        """
        # Check if the sentence is a tautology
        if Belief_Revisor.check_if_contradiction(~sentence):
            print(f"The sentence {sentence} is a tautology, hence it does not provide any information.")
            return True
        # Check if the sentence is a contradiction
        elif Belief_Revisor.check_if_contradiction(sentence):
            print(f"The sentence {sentence} is a contradiction, hence it can never be true.")
            return True
        return False
    
    def __init__(self, initial_state, weight_type) -> None:
        """
        Creates an instance of the Belief_Revisor class.
        The belief base is initialized with an initial assignment of sentences.
        Each are checked if they are a tautology or contradiction, and if not they are added to the KB.
        At last the KB is checked for satisfiability, and if it is not satisfiable the KB is reduced to one that is with contraction.
        
        Args: 
            initial_state (list): A list of sentences to be added to the KB
            weight_type_str (str): A string describing the type of weight to be used - see Belief_Revisor.generate_weight for more information
        """
        self.KB = {}
        self.counter = 0
        self.weight_type = weight_type
        
        # Setup initial state (remove tautologies and contradictions)
        for sentence in initial_state:
            self.expansion(sentence)

        # Contract with nothing to check if the initial KB is satisfiable (that it is the same after contraction)
        if self.contract(None): 
            print("You have given an unsatisfiable initial state. The knowledge base is reduced to:")
            print(self.KB)
        
    def expansion(self, new_sentence):
        """Adds the new sentence to KB and assigns the prior (if not a tautology or contradiction)"""
        if Belief_Revisor.check_contradiction_and_tautology(new_sentence):
            pass
        else: 
            self.KB[new_sentence] = (Belief_Revisor.generate_weight(new_sentence, self.weight_type), self.counter)
            self.counter += 1 
        
    def contract(self, new_sentence):
        """
        Contract the KB with the new sentence, which means remove sentences that entails the new sentence. 
        Which is equivalent to checking if the negated new sentence creates a contradiction with the KB.
        If it doesn't then the KB does not entail the new sentence, and nothing is to be removed. 
        
        To be able to remove only the part of KB that entails the new sentence,
        this process is done iteratively with each sentence in KB with the highest weighted one first. 
        If a sentence is alright it is added to the "new_KB" along with the negation of the new sentence.
        Then the process is repeated with the next sentence in KB and the new_KB, until there are no more sentences in KB. 
        
        Args: 
            new_sentence (sympy.Symbol): the sentence to be contracted with the KB
        
        Returns: 
            bool: True if the KB is changed by the contraction, False otherwise
        """
        # Check if the new sentence is a tautology or a contradiction,
        # In case of tautology we would check if a contradiction was in the KB, which it can never be
        # Or in the case of a contraction we would check if a tautology was in the KB, which it always is, hence trivial 
        # In either case it does not make sense to contract, hence we print that and end the contraction 
        if new_sentence != None and Belief_Revisor.check_contradiction_and_tautology(new_sentence):
            return False
        
        # Add the negated new sentence to new_KB 
        if new_sentence != None:
            new_sentence = ~new_sentence
            # Add new_sentence to new KB
            new_KB = {new_sentence} 
            new_KB_cnf = Belief_Revisor.to_cnf(new_sentence) 
        else:
            new_KB = set()
            new_KB_cnf = []
        
        # sort clauses
        sorted_KB = sorted(self.KB.keys(), key=lambda x: (self.KB[x][0], -self.KB[x][1]), reverse=True)

        # Iterate over KB and check if the current sentence from KB entails 
        # the new sentence (cause contradiction with the negation of new sentence)
        for sentence in sorted_KB:
            cnf = Belief_Revisor.to_cnf(sentence)
            temp = new_KB_cnf + cnf
            resolution = Resolution_Alg(temp)
            reso = resolution.check_for_contradictions()
            # If resolution does not yield any contradictions, the new_KB does not entail the new sentence
            if reso == False: 
                new_KB.add(sentence)
                new_KB_cnf = temp
                
        # Check if the KB has changed
        changed = not (new_KB - {new_sentence}) == set(self.KB.keys())

        # Remove sentences in KB that are not in new_KB
        if changed:
            self.KB = {key: value for key, value in self.KB.items() if key in new_KB}

        return changed 

    def revision(self, new_sentence):
        """
        Modifies the KB to include the new sentence: 
        Use contraction on "-new_sentence" 
        Use expansion on "new_sentence"
        
        Args: 
            new_sentence (sympy.Symbol): the sentence to be added to the KB
        """
        # Contract 
        self.contract(~new_sentence)
        
        # Expand
        self.expansion(new_sentence)
   
    def entails(self, new_sentence):
        """
        Check if KB entails "new_sentence".
        This is done with the resolution algorithm, as it is equivalent to checking if KB and -new_sentence is unsatisfiable.

        Args:
            new_sentence (sympy.Symbol): The sentence to check for entailment
        
        Returns:
            bool: True if KB entails "new_sentence", False otherwise
        """
        # Make one big CNF with all the sentences in KB and the negation of new_sentence
        list_of_clauses = Belief_Revisor.to_cnf(~new_sentence)
        for sentence in self.KB.keys():
            cnf = Belief_Revisor.to_cnf(sentence)
            list_of_clauses += cnf
        
        # Use resolution to check for contradictions
        resolution = Resolution_Alg(list_of_clauses)
        reso = resolution.check_for_contradictions()
        
        # If there is a contradiction, then KB entails new_sentence
        return reso 




if __name__ == "__main__":
            
    # p,q,r = sympy.symbols('p q r')
    # expressions = {(p >> r), (~r >> q) & (q >> ~r)}

    # # expressions
    # expressions = [(p | ~p), (p >> r), (~r >> q) & (q >> ~r), (~p >> r), (r & ~r)]
    # for sentence in expressions:
    #     print(Belief_Revisor.generate_weight(sentence, 0))

    a, b, c, d, e, f, g, h, i, j, k, l, m, n = sympy.symbols('a b c d e f g h i j k l m n')
    true_rule = (c >> (a & b)) & (d >> c)

    print(Belief_Revisor.generate_weight(true_rule, 0))

    # BR = Belief_Revisor(expressions)

    # # print(BR.KB, BR.entails(p))
    # # print(BR.KB, BR.entails(~p))


    # BR.revision((p | ~p))
    # BR.revision((p & ~p))
    # # print(BR.KB, BR.entails(p), BR.entails(~p))

    # # BR.revision(p)
    # # print(BR.KB, BR.entails(p), BR.entails(~p))

    # # print(BR.KB, BR.entails(p))
    # # print(BR.KB, BR.entails(~p))
