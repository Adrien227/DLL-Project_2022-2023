# https://github.com/dwyl/english-words for the list of words

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from pynput import keyboard
import time


# Check word length
def check_word_length(word):
    if len(word) != 5:
        return False
    else:
        return True


list_of_words = open("words_alpha.txt", "r").read().strip().splitlines()
list_of_words = list(filter(check_word_length, list_of_words))


def on_release(key):
    # Start button
    if key == keyboard.Key.esc:
        return False  # stop listener


def get_row_results(game_row):
    tiles = game_row.find_elements(By.CLASS_NAME, "Tile-module_tile__3ayIZ")
    evaluation = []
    eval_to_int = {
        "correct": 1,
        "present": 0,
        "absent": -1,
        "empty": -2,
        "tbd": -3
    }
    for tile in tiles:
        evaluation.append(eval_to_int[tile.get_attribute("data-state")])
    print(evaluation)
    return tuple(evaluation)


def enter_word(word):
    keyboard_controller = keyboard.Controller()
    keyboard_controller.type(word)
    keyboard_controller.tap(keyboard.Key.enter)
    time.sleep(2)


def main():
    # Start the browser
    browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    browser.get("https://www.nytimes.com/games/wordle/index.html")

    # Wait for start
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()
    print("Starting")

    # Get the game rows
    game_rows = browser.find_elements(By.CLASS_NAME, 'Row-module_row__dEHfN')

    first_string = "tests"
    enter_word(first_string)
    get_row_results(game_rows[0])

    time.sleep(1)

    second_string = "trees"
    enter_word(second_string)
    get_row_results(game_rows[1])


if __name__ == "__main__":
    main()
