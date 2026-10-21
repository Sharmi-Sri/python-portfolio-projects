"""Hangman - a console word guessing game.

Guess the hidden word one letter at a time. You have 6 wrong guesses
before the hangman is complete. Repeating a letter costs nothing.
"""

import os
import random

MAX_MISTAKES = 6
MIN_WORD_LENGTH = 4
WORDS_FILE = "words.txt"  # optional: one word per line, placed next to hangman.py

DEFAULT_WORDS = [
    "python", "variable", "function", "keyboard", "compiler", "algorithm",
    "database", "internet", "software", "terminal", "network", "program",
    "developer", "elephant", "mountain", "chocolate", "adventure", "umbrella",
    "notebook", "festival", "triangle", "library", "pyramid", "football",
    "universe", "guitar", "rainbow", "treasure", "calendar", "diamond",
]

STAGES = [
    r"""
  +---+
  |   |
      |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
]

WIN_BANNER = r"""
  __   _____  _   _  __        _____ _   _ _
  \ \ / / _ \| | | | \ \      / /_ _| \ | | |
   \ V / | | | | | |  \ \ /\ / / | ||  \| | |
    | || |_| | |_| |   \ V  V /  | || |\  |_|
    |_| \___/ \___/     \_/\_/  |___|_| \_(_)
"""

LOSE_BANNER = r"""
   ____    _    __  __ _____    _____     _______ ____
  / ___|  / \  |  \/  | ____|  / _ \ \   / / ____|  _ \
 | |  _  / _ \ | |\/| |  _|   | | | \ \ / /|  _| | |_) |
 | |_| |/ ___ \| |  | | |___  | |_| |\ V / | |___|  _ <
  \____/_/   \_\_|  |_|_____|  \___/  \_/  |_____|_| \_\
"""


def load_words():
    """Load words from words.txt if it exists, else use the built-in list."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), WORDS_FILE)
    if os.path.isfile(path):
        try:
            with open(path, encoding="utf-8") as f:
                words = [
                    line.strip().lower()
                    for line in f
                    if line.strip().isalpha() and len(line.strip()) >= MIN_WORD_LENGTH
                ]
            if words:
                return words
        except OSError:
            pass
    return DEFAULT_WORDS


def choose_word(words):
    """Pick a random secret word."""
    return random.choice(words).lower()


def mask_word(word, guessed):
    """Return the word with unguessed letters hidden, e.g. 'p _ t h _ n'."""
    return " ".join(letter if letter in guessed else "_" for letter in word)


def is_word_guessed(word, guessed):
    """True when every letter of the word has been guessed."""
    return all(letter in guessed for letter in word)


def display_state(word, guessed, mistakes):
    """Print gallows, masked word, wrong letters and attempts left."""
    wrong = sorted(letter for letter in guessed if letter not in word)
    print(STAGES[mistakes])
    print(f"\nWord:           {mask_word(word, guessed)}")
    print(f"Wrong guesses:  {' '.join(wrong) if wrong else '-'}")
    print(f"Attempts left:  {MAX_MISTAKES - mistakes}")


def get_guess(guessed):
    """Ask for one valid, new letter. Re-prompts on bad input."""
    while True:
        raw = input("\nGuess a letter: ").strip().lower()
        if len(raw) != 1 or not raw.isalpha():
            print("Please enter a single letter (a-z).")
        elif raw in guessed:
            print(f"You already guessed '{raw}'. Try a different letter.")
        else:
            return raw


def play_round(words):
    """Play one full game. Returns True if the player won."""
    word = choose_word(words)
    guessed = set()
    mistakes = 0

    print("\n" + "=" * 40)
    print("  H A N G M A N")
    print("=" * 40)
    print(f"The word has {len(word)} letters. You have {MAX_MISTAKES} wrong guesses.")

    while mistakes < MAX_MISTAKES and not is_word_guessed(word, guessed):
        display_state(word, guessed, mistakes)
        letter = get_guess(guessed)
        guessed.add(letter)

        if letter in word:
            print(f"Good guess! '{letter}' is in the word.")
        else:
            mistakes += 1
            print(f"Sorry, '{letter}' is not in the word.")

    display_state(word, guessed, mistakes)
    if is_word_guessed(word, guessed):
        print(WIN_BANNER)
        print(f"You guessed it with {MAX_MISTAKES - mistakes} attempt(s) to spare!")
        print(f"The word was: {word.upper()}")
        return True

    print(LOSE_BANNER)
    print(f"The word was: {word.upper()}")
    return False


def ask_play_again():
    """Ask whether to play another round."""
    while True:
        answer = input("\nPlay again? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please type 'y' or 'n'.")


def main():
    words = load_words()
    wins = losses = 0

    try:
        while True:
            if play_round(words):
                wins += 1
            else:
                losses += 1
            print(f"\nScore -> Wins: {wins} | Losses: {losses}")
            if not ask_play_again():
                break
    except (KeyboardInterrupt, EOFError):
        print()

    print("\nThanks for playing Hangman. Goodbye!")


if __name__ == "__main__":
    main()
