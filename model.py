import math
import tqdm
import requests
import sys
from collections import defaultdict
from wordle import wordle
from datetime import datetime
from multiprocessing import Pool


def parallel_entropy_calculation(word):
    return word, run_report_permutations(word)


word_list = open(
    './wordle_possibles.txt').read().strip().split('\n')


def fetch_wordle_data(date):
    """
    Fetches the Wordle data for a specific date from the New York Times API.

    Args:
        date (str): The date in YYYY-MM-DD format for which to retrieve the Wordle data.

    Returns:
        dict or None: A dictionary containing the Wordle data if the request is successful, otherwise None.
    """
    url = f"https://www.nytimes.com/svc/wordle/v2/{date}.json"

    try:
        response = requests.get(url)

        # Check if the request was successful
        response.raise_for_status()
        return response.json()["solution"]

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def possible_words(guess, report, word_set):
    """
    This function filters a set of words based on the feedback from a guess.

    Parameters:
    - guess (str): The word guessed by the user.
    - report (list of int): A list containing integers representing the feedback for each character in the guess.
    - word_set (set of str): A set of possible words to be filtered.

    Returns:
    - result (set of str): A set containing only the words that match the feedback from the guess.
    """
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
    """
    Generates a report for the given guess based on the target word.

    Args:
    guess (str): The guessed word by the user.
    target (str): The target word to be guessed.

    Returns:
    tuple: A tuple containing integers representing the status of each character in the guess:
           2 if the character is correct and in the correct position,
           1 if the character is correct but in the wrong position,
           0 if the character is incorrect.
    """
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
    """
    Calculates the entropy of word permutations based on a given guess.

    Args:
    guess (str): The guessed word to compare against a list of words.

    Returns:
    float: The calculated entropy value.
    """

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

    if '-i' in sys.argv[1:]:
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")

        print(current_date)
        game = wordle(fetch_wordle_data(current_date))
    else:
        game = wordle()

    with Pool() as pool:
        results = list(tqdm.tqdm(
            pool.imap(parallel_entropy_calculation, word_list), total=len(word_list)))

    expected_information = dict(results)

    print("Done evaluating all words")
    word_set = set(word_list)

    tries = 1

    while tries < 7:
        best_guess = max(expected_information, key=expected_information.get)
        print(f"The best guess that we have is {best_guess}")
        report = game.test_guess(best_guess)
        if not report:
            continue
        if all(r == 2 for r in report):
            print("Guessed correctly 🎉")
            print(f"Trial Count:{tries}")
            if '-i' in sys.argv[1:]:
                with open("trials_count.txt", "a", encoding="utf-8") as f:
                    f.write(f'{current_date},{tries}\n')
            sys.exit(0)
        else:
            tries += 1

        game.pretty_test_guess(report)
        word_set = possible_words(
            best_guess, report, word_set)
        expected_information = {
            key: expected_information[key] for key in expected_information if key in word_set}

    print("Failed to guess the word ❌")
