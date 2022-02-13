import random
from typing import List, Set
from game import LetterState, WordGuess, WordleMatch
from util import read_word_file

class RandomSolver:
    def __init__(self, word_list: Set[str]) -> None:
        self.word_list = word_list

    def create_guess(self) -> str:
        """Create random guess from word list"""
        return random.choice(list(self.word_list))

if __name__ == "__main__":

    filepath = "data/words_2315.txt"
    # Remove newline char and convert to set
    words = set([word[:-1] for word in read_word_file(filepath=filepath)])
    print(len(words))

    # Create new match
    match = WordleMatch(max_guesses=6, word_list=words)

    # Create guesser
    guesser = RandomSolver(words)

    while not match.is_game_over():
        guess_str = guesser.create_guess()
        print(guess_str)
        print(match.make_guess(guess_str)[-1]._get_score())

    print(match.guess_list[-1]._get_score())
    print(match)