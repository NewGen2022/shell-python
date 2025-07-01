import os
import readline
from builtins import COMMANDS
from utils import find_executables_starting_with

AUTOCOMPLETION = list(COMMANDS.keys())

tab_pressed = 0
last_completion_text = ""


def autocomplete(text, state):
    global last_completion_text, tab_pressed

    matches = [
        candidate + " " for candidate in AUTOCOMPLETION if candidate.startswith(text)
    ]

    if last_completion_text != text:
        tab_pressed = 0
        last_completion_text = text

    if state == 0:
        tab_pressed += 1

    if not matches:
        matches = find_executables_starting_with(text)

        if len(matches) > 1:
            common_prefix = os.path.commonprefix(matches)
            if common_prefix:
                difference = common_prefix[len(text) :]
                readline.insert_text(difference)
                readline.redisplay()

            if tab_pressed == 2:
                print("\n" + " ".join(matches))
                print(f"$ {text}", end="", flush=True)
            elif tab_pressed < 1 or tab_pressed > 2:
                print("\x07", end="", flush=True)
            return None

    if not matches:
        print("\x07", end="", flush=True)
        return None

    if state < len(matches):
        return matches[state]

    return None
