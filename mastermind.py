from main import *
import sympy
import random 


class Mastermind:
    def __init__(self, colors, answer, code_length):
        self.colors = colors
        self.code_length = code_length
        self.Mind = Belief_Revisor({})
        self.answer = answer 
        self.literals = {color: [sympy.symbols(f"{color}{i}") for i in range(self.code_length)] for color in colors}
    
    def check_guess(self, guess):
        # Check guess and return new information
        to_update = []
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
            guess = self.generate_guess()
            
            counter += 1
            print(f"Guess {counter}: {guess}")
            
            # Goal test 
            if self.won(guess):
                print(f"Mastermind won with guess {guess} in {counter} tries.")
                break
                
            # Test guess  
            to_update = self.check_guess(guess)
            # put new information i KB
            for sentence in to_update:
                self.Mind.revision(sentence)

# Setup
colors = ["red", "blue", "green", "yellow", "orange", "purple", "white", "black"] 
code_length = 6

answer = [random.choice(colors) for i in range(code_length)] 

print(f"Answer: {answer}")
mastermind = Mastermind(colors, answer, code_length)
mastermind.solve()




           




    
 
