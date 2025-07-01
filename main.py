import sys, os
import subprocess
import readline
from autocomplete import autocomplete
from parser import parse_input, parse_pipeline
from pipeline import setup_pipeline
from redirection import handle_redirection
from utils import executable
from my_builtins import COMMANDS, history_handle, load_from_env_history_file, on_exit


def main():
    readline.set_completer(autocomplete)
    readline.parse_and_bind("tab: complete")
    readline.set_auto_history(False)

    history_buffer = []
    last_appended_history_index = 0

    load_from_env_history_file(history_buffer)

    while True:
        # read and parse input from user
        input_string = input("$ ")

        if not input_string:
            continue

        readline.add_history(input_string)
        history_buffer.append(input_string)

        command_with_args = parse_input(input_string)

        if "|" in command_with_args:
            pipeline = parse_pipeline(command_with_args)
            setup_pipeline(pipeline)
            continue  # pipeline already executed

        command_with_args, error_file, output_file = handle_redirection(
            command_with_args
        )

        # extract command
        command = command_with_args[0]

        # run external executable if not builtin
        if not command in COMMANDS:
            full_path = executable(command)
            if full_path:
                subprocess.run(
                    [command, *(command_with_args)[1:]],
                    stdout=output_file if output_file else None,
                    stderr=error_file if error_file else None,
                )  # run executable with args
            else:
                print(f"{command}: command not found")  # error if command not found
            if output_file:
                output_file.close()
            if error_file:
                error_file.close()
            continue  # skip builtin execution since it's external command
        else:
            if output_file:
                original_stdout = sys.stdout
                sys.stdout = output_file
            if error_file:
                original_stderr = sys.stderr
                sys.stderr = error_file

            # call built-in command
            if command == "history":
                skip_builtin, last_appended_history_index = history_handle(
                    command_with_args,
                    history_buffer,
                    command,
                    last_appended_history_index,
                )
                if skip_builtin == "continue":
                    continue
            elif command == "exit":
                if len(command_with_args) > 1:
                    exit_code = command_with_args[1]
                else:
                    exit_code = 0
                on_exit(exit_code, history_buffer)
            else:
                COMMANDS[command](*(command_with_args)[1:])

            if output_file:
                sys.stdout = original_stdout
            if error_file:
                sys.stderr = original_stderr

        if output_file:
            output_file.close()
        if error_file:
            error_file.close()


if __name__ == "__main__":
    main()
