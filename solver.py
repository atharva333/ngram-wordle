import random
import time
from typing import List, Set
from game import LetterState, WordGuess, WordleMatch
from util import read_word_file

class RandomSolver:
    def __init__(self, word_list: Set[str]) -> None:
        self.word_list = word_list
        self.guess_list = []

    def create_guess(self) -> str:
        """Create random guess from word list"""
        return random.choice(list(self.word_list))

    def add_guess(self, guess: WordGuess) -> None:
        """Add guess to list of guesses"""
        self.guess_list.append(guess)

class LetterMatchedSolver:
    def __init__(self, word_list: Set[str]) -> None:
        self.word_list = word_list
        self.guess_list = []

    def create_guess(self) -> str:
        """Create guess from word list"""
        if self.guess_list:
            last_guess = self.guess_list[-1]
            letter_positions = [(letter, position) for position, (letter, state) in enumerate(zip(last_guess.guess_letters, last_guess.guess_state)) if state == LetterState.CORRECT]
            print(f"{letter_positions}")
            
            letter_matched_list = []
            for word in self.word_list:
                
                # Add error check for if word is too short
                if len(word) != 5:
                    continue

                # Check all letter in current word
                is_word_matched = True
                for letter, position in letter_positions:
                    if word[position] != letter:
                        is_word_matched = False
                
                # Append if check passed
                if is_word_matched:
                    letter_matched_list.append(word)

            return random.choice(letter_matched_list)
        else:
            return random.choice(list(self.word_list))

    def add_guess(self, guess: WordGuess) -> None:
        """Add guess to list of guesses"""
        self.guess_list.append(guess)

if __name__ == "__main__":

    filepath = "data/words_2315.txt"
    # Remove newline char and convert to set
    words = set([word[:-1] for word in read_word_file(filepath=filepath)])
    print(len(words))

    # Create new match
    match = WordleMatch(max_guesses=6, word_list=words)

    # Create guesser
    guesser = LetterMatchedSolver(words)

    start_time = time.time()
    print(f"Start time: {start_time}")

    # Play game
    while not match.is_game_over():
        guess_str = guesser.create_guess()
        print(guess_str)
        guess = match.make_guess(guess_str)[-1]
        #print(f"{guess}")
        
        if guess is not None:
            guesser.add_guess(guess)

    print(match.guess_list[-1]._get_score())
    print(match)

    print(f"Time taken: {time.time() - start_time}")