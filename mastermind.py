from main import *
import sympy
import random 


class Mastermind:
    def __init__(self, colors, answer, code_length):
        self.colors = colors
        self.code_length = code_length
        self.Mind = Belief_Revisor([])
        self.answer = answer 
        self.literals = {color: [sympy.symbols(f"{color}{i}") for i in range(self.code_length)] for color in colors}
    
    def check_guess(self, guess):
        # Check guess and return new information
        to_update = []
        # TODO Change for loop to elif logic to test if any are correct colors and positions
        '''
        for i in range(self.code_length):
            if guess[i] == self.answer[i]:
                # If this part of the guess is correct, the color and position is added to KB, 
                # and the negation of all other colors in that position is added aswell.
                to_update.append(self.literals[guess[i]][i] & sympy.And(*set([~self.literals[color][i] for color in self.colors if color != guess[i]])) )
            elif guess[i] in answer:
                # That the color exists is added to the KB (but not in this position)
                to_update.append(sympy.Or(*set([self.literals[guess[i]][j] for j in range(self.code_length) if j != i])) & ~self.literals[guess[i]][i])
            else:
                # That the color does not exists is added to the KB 
                to_update.append(sympy.And(*set([~self.literals[guess[i]][j] for j in range(self.code_length)])))
        '''
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

        # If no correct colors were guessed
        if correct_color + correct_position == 0:
            for i in range(self.code_length):
                to_update.append(sympy.And(*set([~self.literals[guess[i]][j] for j in range(self.code_length)])))
        if correct_position == 0:
            for i in range(self.code_length):
                to_update.append(sympy.And(*set([~self.literals[color][i] for color in self.colors if color == guess[i]])))
        if correct_color == 4:
            for i in range(self.code_length):
                to_update.append(sympy.Or(*set([self.literals[guess[i]][j] for j in range(self.code_length) if j != i])) & ~self.literals[guess[i]][i])
        if correct_color + correct_position == 4:
            for i in range(self.code_length):
                to_update.append(sympy.Or(*set([self.literals[guess[i]][j] for j in range(self.code_length)])))

        # Get information from number of colors
        if correct_color == 1 and correct_position == 0:
            pass
        elif correct_color == 2 and correct_position == 0:
            pass
        elif correct_color == 3 and correct_position == 0:
            pass

        # Never repeat the same sequence if it isn't correct.
        # TODO Might not work completely. Sometimes it is unable to generate a new guess after this
        if correct_position != 4:
            to_update.append(sympy.Not(sympy.And(*set([self.literals[guess[i]][i] for i in range(self.code_length)]))))


        return to_update

    def generate_guess(self):
        # Generate feasible guess (w.r.t. KB)
        guess = []
        
        for i in range(self.code_length): 
            found_color = False 
            colors_to_try = set(self.colors)
            while not found_color:
                # Try a new color until we have one where KB does not entail the negation.
                color = random.choice(list(colors_to_try))
                colors_to_try -= {color}
                found_color = not self.Mind.entails(~self.literals[color][i])
            guess.append(color)
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
            to_update = self.check_guess(guess)
            # put new information i KB
            for sentence in to_update:
                self.Mind.revision(sentence)

# Setup

for i in range(1):
    colors = ["red", "blue", "green", "yellow", "orange", "purple"] 
    code_length = 4

    answer = [random.choice(colors) for i in range(code_length)] 

    print(f"Answer: {answer}")
    mastermind = Mastermind(colors, answer, code_length)
    mastermind.solve()


# TODO Store earlier guesses, and check if previously have had a guess with same x correct colors/positions, with x identical placed pins and all other different, then those x must be correct