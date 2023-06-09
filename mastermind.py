from main import *
import sympy
import random 
import itertools

class Mastermind:
    def __init__(self, colors, answer, code_length):
        self.colors = colors
        self.code_length = code_length
        self.answer = answer 
        self.literals = {color: [sympy.symbols(f"{color}{i}") for i in range(self.code_length)] for color in colors}
        # If a color is set in one entry, then other colors can't be in said entry
        initial_expressions = []
        for i in range(self.code_length):
            for color in self.colors:
                # There can never be more than one color in one entry
                consequent1 = sympy.And(*set([~self.literals[second_color][i] for second_color in colors if second_color != color]))
                # Our bonus rule - ther can never be more than on of each color 
                consequent2 = sympy.And(*set([~self.literals[color][j] for j in range(self.code_length) if j != i]))
                # premise -> consequent1 & consequent2
                initial_expressions.append(sympy.Implies(self.literals[color][i], sympy.And(consequent1, consequent2)))
            
            # There must be one color in each entry
            initial_expressions.append(sympy.Or(*set([self.literals[color][i] for color in self.colors])))
            
        self.Mind = Belief_Revisor(initial_expressions)
        
    def logical_sentence(self, position_set, color_set, not_correct_set):
        # Generate propositional sentence for the position
        position_proposition = sympy.And(*set([self.literals[col][place] for col, place in position_set]))
        
        # Generate propositional sentence for the color
        color_proposition = []
        for col, place in color_set:
            # The color is correct, but not in the correct spot, hence one of all other positions must occur
            color_proposition.append(sympy.Or(*set([self.literals[col][i] for i in range(self.code_length) if i != place])))
            color_proposition.append(~self.literals[col][place])
        color_proposition = sympy.And(*set(color_proposition))
        
        # Generate propositional sentence for the not correct set
        wrong_color_proposition = []
        for col, _ in not_correct_set: 
            # Because the color is assumed to be wrong, the negation of ALL positions with this color is added
            for i in range(self.code_length):
                wrong_color_proposition.append(~self.literals[col][i])
        wrong_color_proposition = sympy.And(*set(wrong_color_proposition))
        
        # Make this into one propositional sentence
        propositional_sentence = sympy.And(position_proposition, color_proposition, wrong_color_proposition)
        return propositional_sentence
        
    def check_guess(self, guess):
        """
        Function takes in a guess and outputs the new propositional logic information that was learned
        First it checks how many colors and positions are correct in the guess
        then it constructs all possible sentences that could have given this output in the form of propositional logic
        This is passed logical_sentence() which returns the propositional sentence
        
        Args:
            guess (list): list of colors that is the guess
        
        Returns:
            propositional_sentence (sympy sentence): sentence that encaptures the information from the guess
        """
        correct_color = 0
        correct_position = 0
        temp_answer = self.answer.copy()
        for i in range(self.code_length):
            if guess[i] == temp_answer[i]:
                correct_position += 1
                temp_answer[temp_answer.index(guess[i])] = ''
        for i in range(self.code_length):
            if guess[i] in temp_answer:
                correct_color += 1
                temp_answer[temp_answer.index(guess[i])] = ''

        # Make guess into literals
        # guess_literals = set([self.literals[guess[i]][i] for i in range(self.code_length)])
        guess_literals = set([(guess[i], i) for i in range(self.code_length)])
        
        # Generate propositional sentence that encaptures the information from the guess
        # First get information from correct positions
        correct_position_sets = list(itertools.combinations(guess_literals, correct_position))
        correct_position_sets = [set(x) for x in correct_position_sets]
        
        # Next get information from correct colors
        possible_sentences = []
        for position_set in correct_position_sets:
            # Get all correct color combinations when the correct positions are assumed
            color_sets = list(itertools.combinations(guess_literals - position_set, correct_color))
            for color_set in color_sets:
                # Get the incorrect colors when the correct colors and positions are assumed
                not_correct_set = guess_literals - position_set - set(color_set) 
                
                # Generate propositional logic sentence
                possible_sentences.append(self.logical_sentence(position_set, color_set, not_correct_set))
        
        # Collect all the possible sentences to one big sentence (with OR)
        propositional_sentence = sympy.Or(*set(possible_sentences))
        
        return propositional_sentence
        
        

    def generate_guess(self):
        # Generate feasible guess (w.r.t. KB)
        guess = []
        # Find a guess g, where not g is not entailed by KB
        while guess == []: 
            # temp_guess = random.sample(self.colors, self.code_length) # This is the time consuming way
            
            # This is the fast way that only tries guesses that are feasible, but is not using the agent as much
            KB = sympy.And(*set(self.Mind.KB.keys()))
            possibility = sympy.satisfiable(KB)
            # Get the literals that are true
            true_literals = [literal for literal, value in possibility.items() if value is True]
            # Map the literals to the guess/strings
            temp_guess = self.map_literal_to_guess(true_literals)
            # Only need a list of the colors, hence sort after the index and create guess
            temp_guess = sorted(temp_guess, key=lambda x: x[1])
            temp_guess = [item[0] for item in temp_guess]
            
            if not self.Mind.entails(~sympy.And(*set([self.literals[temp_guess[i]][i] for i in range(self.code_length)]))):
                guess = temp_guess
        
        return guess
    
    def map_literal_to_guess(self, literals):
        """Maps the literals to the guess."""
        guess = []
        for color, color_elements in self.literals.items():
            for index, element in enumerate(color_elements):
                if element in literals:
                    guess.append((color, index))
        return guess

    def won(self, guess):
        return guess == self.answer

    def solve(self):
        counter = 0
        while True:
            # Generate guess 
            print("Processing...")
            guess = self.generate_guess()
            
            counter += 1
            print(f"Guess {counter}: {guess}")
            
            # Goal test 
            if self.won(guess):
                print(f"Mastermind won with guess {guess} in {counter} tries.")
                with open("benchmark.txt", 'a') as benchmark:
                    benchmark.write(f"{counter}\n")
                break
                
            # Test guess  
            sentence = self.check_guess(guess)
            # put new information i KB
            # for sentence in to_update:
            self.Mind.revision(sentence)

# Setup

for i in range(100):
    colors = ["red", "blue", "green", "yellow", "orange", "purple"] 
    code_length = 3

    answer = random.sample(colors, code_length)

    print(f"Answer: {answer}")
    mastermind = Mastermind(colors, answer, code_length)
    mastermind.solve()

