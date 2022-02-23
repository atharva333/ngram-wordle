import random
import time
import numpy as np
from typing import List, Set
from abc import ABC, abstractmethod
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer

from rich import print

from util import read_word_file
from game import LetterState, WordGuess, WordleMatch


class Solver(ABC):
    """Abstract class for solver"""

    def __init__(self, word_list: Set[str]) -> None:
        pass

    @abstractmethod
    def create_guess(self) -> str:
        """Create guess"""
        raise NotImplementedError

    def add_guess(self, guess: WordGuess) -> None:
        """Add guess to list of guesses"""
        self.guess_list.append(guess)


class RandomSolver(Solver):
    def __init__(self, word_list: Set[str]) -> None:
        self.word_list = word_list
        self.guess_list = []

    def create_guess(self) -> str:
        """Create random guess from word list"""
        return random.choice(list(self.word_list))


class LetterMatchedRandomSolver(Solver):
    def __init__(self, word_list: Set[str]) -> None:
        self.remaining_word_list = list(word_list)
        self.guess_list = []

        self.correct_letters = defaultdict(set)
        self.mispositioned_letters = defaultdict(list)
        self.incorrect_letters = set()

    def create_guess(self) -> str:
        """Create guess from word list"""
        if self.guess_list:
            last_guess = self.guess_list[-1]

            # Update letter state dicts
            self.update_letter_state_dicts(last_guess)

            # Prune word list based on filter criteria
            self.remaining_word_list = self.filter_word_list(last_guess)

        # Return random word from filtered list
        return random.choice(list(self.remaining_word_list))

    def update_letter_state_dicts(self, last_guess: WordGuess) -> None:
        """Update correct, mispositioned, incorrect letter collections"""

        # Loop through guess
        for position, (letter, state) in enumerate(zip(last_guess.guess_letters, last_guess.guess_state)):

            if state == LetterState.CORRECT:
                # Add to correct letters dict
                self.correct_letters[letter].add(position)

            elif state == LetterState.MISPOSITIONED:
                # Add to mispositioned letters dict
                self.mispositioned_letters[letter].append(position)

        correct_letters = self.correct_letters.keys() | self.mispositioned_letters.keys()

        incorrect_letters = {
            letter
            for letter, state in zip(last_guess.guess_letters, last_guess.guess_state)
            if (state == LetterState.UNKNOWN) and (letter not in correct_letters)
        }
        self.incorrect_letters = self.incorrect_letters | incorrect_letters

    def filter_word_list(self, last_guess: WordGuess) -> List[str]:
        """Filter word list based on last guess"""

        letter_matched_list = []
        for word in self.remaining_word_list:

            # Add error check for if word is too short
            if len(word) != 5:
                continue

            # Check if word is same as the last guess
            if word == last_guess.guess_letters:
                continue

            # Check all letter in current word
            if not self._check_correct_letters(word):
                continue

            # Check all mispositioned letters
            if not self._check_mispositioned_letters(word):
                continue

            # Check all incorrect letters
            if not self._check_incorrect_letters(word):
                continue

            # Add word to list
            letter_matched_list.append(word)

        # print(f"Remaining possible words: {len(letter_matched_list)}")
        return letter_matched_list

    def _check_correct_letters(self, word: str) -> bool:
        """Check if word contains all correct letters"""
        for letter, positions in self.correct_letters.items():
            if any(word[position] != letter for position in positions):
                return False
        return True

    def _check_mispositioned_letters(self, word: str) -> bool:
        """Check if word contains mispositioned letters in possible positions"""
        for letter, positions in self.mispositioned_letters.items():
            if letter not in word:
                return False
            elif any(word[position] == letter for position in positions):
                return False
        return True

    def _check_incorrect_letters(self, word: str) -> bool:
        """Check if word contains any incorrect letters"""
        if any(letter in word for letter in self.incorrect_letters):
            return False
        return True

class SortedLetterMatchedSolver(LetterMatchedRandomSolver):
    def __init__(self, word_list: Set[str]) -> None:
        self.remaining_word_list = list(word_list)
        self.guess_list = []

        self.correct_letters = defaultdict(set)
        self.mispositioned_letters = defaultdict(list)
        self.incorrect_letters = set()

    def create_guess(self) -> str:
        """Create guess from word list"""
        if self.guess_list:
            last_guess = self.guess_list[-1]

            # Update letter state dicts
            self.update_letter_state_dicts(last_guess)

            # Prune word list based on filter criteria
            self.remaining_word_list = self.filter_word_list(last_guess)
        
        # if len(self.guess_list) > 1:
        
        letter_counts = self.get_letter_counts(self.remaining_word_list)
        word_scores = self.get_word_scores(self.remaining_word_list, letter_counts)
        sorted_words = sorted(list(zip(self.remaining_word_list, word_scores)), key=lambda x: x[1], reverse=True)
        # print(sorted_words[:10])

        # Return random word from filtered list
        return sorted_words[0][0]
        
        # else:
        #     return random.choice(self.remaining_word_list)

    def get_letter_counts(self, words: List[str]) -> defaultdict(int):
        """Get letter counts for all words"""
        # Calculate letter counts
        letter_counts = defaultdict(int)
        for word in words:
            for letter in word:
                letter_counts[letter] += 1

        # Normalise letter counts
        for letter in letter_counts.keys():
            letter_counts[letter] /= len(words)

        return letter_counts

    def get_word_scores(self, words: List[str], letter_counts: defaultdict(int)) -> List[int]:
        """Get word scores for all words based on letter counts"""
        # For each word sum the score of each letter
        word_scores = [sum([letter_counts[letter] for pos, letter in enumerate(word) if pos == word.index(letter)]) for word in words]
        return word_scores

if __name__ == "__main__":

    filepath = "data/words_2315.txt"
    # Remove newline char and convert to set
    words = set([word[:-1] for word in read_word_file(filepath=filepath)])
    print(len(words))

    # Create new match
    match = WordleMatch(max_guesses=6, word_list=words)

    # Create guesser
    guesser = SortedLetterMatchedSolver(words)

    start_time = time.time()
    print(f"Start time: {start_time}")

    # TODO: run games 1000s of times and work out average score and time
    try:
        # Play game
        while not match.is_game_over():
            guess_str = guesser.create_guess()
            # print(guess_str)
            guess = match.make_guess(guess_str)[-1]
            print(f"Remaining possible words: {len(guesser.remaining_word_list)}")

            # print(guesser.correct_letters)
            # print(guesser.mispositioned_letters)
            # print(guesser.incorrect_letters)
            print(f"{guess}")

            if guess is not None:
                guesser.add_guess(guess)
    except Exception as e:
        print(e)
        print(f"Target word was: {match.target_word}")

    if match.guess_list[-1]._get_score() == 10:
        print(f"You won in {len(match.guess_list)} guesses")
    print(f"Target word was: {match.target_word}")

    print(f"Time taken: {time.time() - start_time}")
