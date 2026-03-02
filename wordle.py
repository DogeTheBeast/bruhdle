import random
import sys


class wordle():

    def __init__(self):
        self.word_list = open(
            "/home/doge/Packages/wordle-solver/wordle_possibles.txt").read().split('\n')
        word = self.word_list[random.randint(0, len(self.word_list))]
        print("The word to guess is : " + word)
        self.correct_word = word
        self.word = list(word)

    def validate_guess(self, guess):

        if len(guess) != 5:
            print("Guess is not 5 letters")
            return False
        elif "".join(guess) not in self.word_list:
            print("Guess not a valid word")
            return False
        return True

    def test_guess(self, guess):

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
        if char == 0:
            return '⬜️'
        elif char == 1:
            return '🟨'
        elif char == 2:
            return '🟩'

    def pretty_test_guess(self, report):
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
