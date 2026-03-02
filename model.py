import math
import tqdm
from collections import defaultdict
from wordle import wordle

from multiprocessing import Pool


def parallel_entropy_calculation(word):
    return word, run_report_permutations(word)


word_list = open(
    '/home/doge/Packages/wordle-solver/wordle_possibles.txt').read().strip().split('\n')


def possible_words(guess, report, word_set):
    result = set()

    for word in word_set:
        valid = True
        tmp_word = word
        word = list(word)
        for i, value in enumerate(report):
            if value == 2 and guess[i] == word[i]:
                word[i] = " "
            elif value == 1 and guess[i] in word and guess[i] != word[i]:
                word[word.index(guess[i])] = " "
            elif value == 0 and guess[i] not in word:
                valid = True
            else:
                valid = False
                break

        if valid:
            result.add("".join(tmp_word))

    return result


def generate_report(guess, target):
    report = []
    target = list(target)
    for i, char in enumerate(guess):
        value = 0
        if char == target[i]:
            value = 2
            target[i] = " "
        elif char in target:
            value = 1
            target[target.index(char)] = " "
        report.append(value)
    return tuple(report)


def run_report_permutations(guess):

    count = defaultdict(int)
    for word in word_list:
        report = generate_report(guess, word)
        count[report] += 1

    entropy = 0
    for value in count.values():
        p = value/len(word_list)
        entropy += -p * math.log(p, 2)

    return entropy


if __name__ == "__main__":

    game = wordle()
    report = None

    with Pool() as pool:
        results = list(tqdm.tqdm(
            pool.imap(parallel_entropy_calculation, word_list), total=len(word_list)))

    expected_information = dict(results)

    print("Done evaluating all words")
    word_set = set(word_list)
    while True:
        best_guess = max(expected_information, key=expected_information.get)
        print(f"The best guess that we have is {
              best_guess} {game.correct_word}")
        report = game.test_guess(best_guess)
        game.pretty_test_guess(report)
        word_set = possible_words(
            best_guess, report, word_set)
        expected_information = {
            key: expected_information[key] for key in expected_information if key in word_set}
