import random
import sys


class wordle:

    def __init__(self):
        """
        Initializes a new Wordle game instance.
        Loads the word list from a file and selects a random word as the answer.
        Prints the selected word for debugging purposes (should not be shown in actual gameplay).
        """
        self.word_list = open(
            "/home/doge/Packages/wordle-solver/wordle_possibles.txt").read().split('\n')
        self.correct_word = random.choice(self.word_list)
        print("The word to guess is : " + self.correct_word)
        self.word = list(self.correct_word)

    def validate_guess(self, guess):
        """
        Validates the user's guess.
        Checks if the guess is 5 letters long and a valid word from the word list.

        Args:
            guess (str): The user's guess.

        Returns:
            bool: True if the guess is valid, False otherwise.
        """
        if len(guess) != 5:
            print("Guess is not 5 letters")
            return False
        elif "".join(guess) not in self.word_list:
            print("Guess not a valid word")
            return False
        return True

    def test_guess(self, guess):
        """
        Tests the user's guess against the correct word.
        Provides feedback on the position and accuracy of each character.

        Args:
            guess (str): The user's guess.

        Returns:
            list: A list of integers representing the feedback for each character in the guess.
                  0 - Letter is not in the word
                  1 - Letter is in the word but in the wrong position
                  2 - Letter is in the word and in the correct position
        """
        if not self.validate_guess(guess):
            return False

        if guess == self.correct_word:
            self.pretty_test_guess([2, 2, 2, 2, 2])
            print("Guessed correctly 🎉")
            sys.exit(0)

        report = []
        local_word = self.word.copy()
        for i, char in enumerate(guess):
            value = 0
            if char == local_word[i]:
                value = 2
                local_word[i] = " "
            elif char in local_word:
                value = 1
                local_word[local_word.index(char)] = " "
            report.append(value)
        return report

    def emojis(self, char):
        """
        Converts the feedback integer to an emoji string.

        Args:
            char (int): The feedback integer.

        Returns:
            str: An emoji representing the feedback.
        """
        if char == 0:
            return '⬜️'
        elif char == 1:
            return '🟨'
        elif char == 2:
            return '🟩'

    def pretty_test_guess(self, report):
        """
        Prints the feedback as a string of emojis.

        Args:
            report (list): A list of integers representing the feedback for each character in the guess.
        """
        print_line = list(map(self.emojis, report))
        print("".join(print_line))


if __name__ == "__main__":
    wordle = wordle()

    tries = 0

    while tries < 6:
        guess = input("Guess: ")
        report = wordle.test_guess(list(guess))
        if report:
            wordle.pretty_test_guess(report)
            tries += 1

    print("Failed to guess the word ❌")
