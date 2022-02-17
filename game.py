import random
import time
from enum import IntEnum
from util import read_word_file
from typing import List, Set, Optional
from rich import print

class LetterState(IntEnum):
    UNKNOWN = 0
    MISPOSITIONED = 1
    CORRECT = 2

class WordGuess:
    def __init__(self, letters: str, letters_state: List[LetterState]) -> None:
        self.guess_letters = letters
        self.guess_state = letters_state
        self.letter_colours = ["gray", "yellow", "green"]

    def is_all_correct(self) -> bool:
        """Return True if guess is all correct"""
        return all(letter == LetterState.CORRECT for letter in self.guess_state)
    
    def __str__(self) -> str:
        """Show word guess with print colours"""
        guess_str = ""
        for letter, state in zip(self.guess_letters, self.guess_state):
            guess_str += f"[{self.letter_colours[int(state)]}]{letter.upper()}[/{self.letter_colours[int(state)]}] "
        return guess_str

    def _get_score(self) -> int:
        """Return sum of all individual letters"""
        return sum(self.guess_state)

class WordleMatch:
    """Class for playing one match"""
    def __init__(self, max_guesses: int, word_list: Set[str]) -> None:
        # Assign constructor variables
        self.max_guesses = max_guesses
        self.word_list = word_list

        # TODO: just use list to infer number of guesses and current guess
        # Initialise guess counter
        self.guesses = 0
        self.guess_list = []
        self.current_guess = None

        # Choose target word
        self.target_word = random.choice(list(self.word_list))
        #print(self.target_word)
    
    def play_manual(self) -> None:
        """
        Play game, asking for user input
        End when correct word guessed or max guesses reached
        """
        
        while not self.is_game_over():
            guess_str = input()
            self.make_guess(guess_str)
        print(self)
        print(f"Correct word: {self.target_word}")

        if self.current_guess.is_all_correct():
            print(f"[green]Congratulations you won![/green]")
    
    def is_game_over(self) -> bool:
        """Check if game is over"""
        if (self.current_guess is not None
            and self.current_guess.is_all_correct()):
            return True
        elif self.guesses >= self.max_guesses:
            return True
        else:
            return False
    
    def make_guess(self, guess: str) -> Optional[List[WordGuess]]:
        """Register new guess, if word is in list"""
        if self.is_game_over():
            return None

        if guess in self.word_list:
            self.guesses += 1
            self.current_guess = self._compare_guess_to_target(guess, self.target_word)
            self.guess_list.append(self.current_guess)

            for guess in self.guess_list:
                print(f"{guess}")

            return self.guess_list
        else:
            print(f"[red]Word not in list![/red]")
    
    @staticmethod
    def _compare_guess_to_target(guess:str, target:str) -> WordGuess:
        """Return list of each guessed letter"""
        word_guess_state = []
        # Initially go through and check for correct letters
        for char_guess, char_target in zip(guess, target):
            #print(f"{char_guess}, {char_target}")
            if char_guess == char_target:
                word_guess_state.append(LetterState.CORRECT)
            else:
                word_guess_state.append(LetterState.UNKNOWN)
        
        # Second pass to assign check for mispositioned letters
        for idx, (char_guess, char_target) in enumerate(zip(guess, target)):
            
            if char_guess == char_target:
                continue
            elif char_guess in target:
                # Check if there is another occurrence of same char in guess
                guess_occurrences = [idx for idx, char in enumerate(guess) if char == char_guess]
                #print(f"Guess char occurs for {char_guess}: {guess_occurrences}")
                if len(guess_occurrences) == 1:
                    word_guess_state[idx] = LetterState.MISPOSITIONED
                else:
                    # Check if there is another occurrence of same char in target
                    target_occurrences = [idx for idx, char in enumerate(target) if char == char_guess]
                    #print(f"Target char occurs for {char_guess}: {target_occurrences}")
                    
                    # If this is the last idx for given letter and guess has more of same char than target
                    if (len(target_occurrences) < len(guess_occurrences)) and (guess_occurrences[-1] == idx):
                        continue

                    # Assign mispositioned if the other guess isn't correct
                    for targ_idx in target_occurrences:
                        if (targ_idx != idx) and (word_guess_state[targ_idx] != LetterState.CORRECT):
                            word_guess_state[idx] = LetterState.MISPOSITIONED
        
        return WordGuess(guess, word_guess_state)

    def _check_word_exists(self, word:str) -> bool:
        """Check if word is in word list"""
        return word in self.word_list

    def __str__(self) -> str:
        return f"Game over: {self.is_game_over()}, guess {self.guesses} out of {self.max_guesses}"

if __name__ == "__main__":
    
    filepath = "data/words_2315.txt"
    # Remove newline char and convert to set
    words = set([word[:-1] for word in read_word_file(filepath=filepath)])
    print(len(words))

    new_match = WordleMatch(max_guesses=6, word_list=words)
    new_match.play_manual()
