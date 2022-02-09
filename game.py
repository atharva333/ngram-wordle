from enum import Enum
import random
import time
from typing import List, Set
from rich import print

class LetterState(Enum):
    UNKNOWN = 0
    MISPOSITIONED = 1
    CORRECT = 2

class WordGuess:
    def __init__(self, letters: List[LetterState]) -> None:
        self.guess_letters = letters
    
    def is_all_correct(self) -> bool:
        """Return True if guess is all correct"""
        return all(letter == LetterState.CORRECT for letter in self.guess_letters)

class WordleMatch:
    """Class for playing one match"""
    def __init__(self, max_guesses: int, word_list: Set[str]) -> None:
        
        self.max_guesses = max_guesses
        self.word_list = word_list

        self.guesses = 0 # Initialise guess counter
    
    def is_game_over(self) -> bool:
        """Check if game is over"""
        raise NotImplementedError
    
    def make_guess(self, guess: str) -> None:
        """Register new guess, if word is in list"""
        self.guesses += 1
        raise NotImplementedError
    
    def _check_word_exists(self, word:str) -> bool:
        """Check if word is in word list"""
        raise NotImplementedError

    def _compare_guess_to_target(self, guess:str, target:str) -> WordGuess:
        """Return list of each guessed letter"""
        raise NotImplementedError

    def __str__(self) -> str:
        return f"Game over: {self.is_game_over()}, guess {self.guesses} out of {self.max_guesses}"

if __name__ == "__main__":
    
    new_match = WordleMatch(max_guesses=4, word_list={"b"})
    print(new_match)
