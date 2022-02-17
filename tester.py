import time
import random
from rich.progress import track
from rich.console import Console

from solver import LetterMatchedRandomSolver
from game import WordleMatch
from util import read_word_file

NUMBER_OF_GAMES = 5000

if __name__ == "__main__":

    filepath = "data/words_2315.txt"
    # Remove newline char and convert to set
    words = set([word[:-1] for word in read_word_file(filepath=filepath)])
    print(len(words))

    start_time = time.time()
    print(f"Start time: {start_time}")

    # Track number of guesses for win
    match_guesses = []

    for match_num in track(range(NUMBER_OF_GAMES), description="Playing matches..."):

        # Create new match
        match = WordleMatch(max_guesses=6, word_list=words)
        guesser = LetterMatchedRandomSolver(words)

        try:
            # Play game
            while not match.is_game_over():
                guess_str = guesser.create_guess()
                #print(guess_str)
                guess = match.make_guess(guess_str)[-1]
                #print(f"{guess}")
                
                if guess is not None:
                    guesser.add_guess(guess)
        except Exception as e:
            print(e)

        if match.guess_list[-1]._get_score() == 10:
            # print(f"You won in {len(match.guess_list)} guesses")
            match_guesses.append(len(match.guess_list))


    print(f"Won {len(match_guesses)} out of {NUMBER_OF_GAMES} matches")
    print(f"Average number of guesse for win: {sum(match_guesses) / len(match_guesses)}")
    print(f"Time taken: {time.time() - start_time}")