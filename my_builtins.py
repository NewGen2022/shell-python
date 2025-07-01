import sys, os, readline
from utils import executable
from parser import parse_history_file

# built-in commands mapped to their handlers
COMMANDS = {
    "exit": lambda exit_code, args: on_exit(exit_code, args),  # terminate the program
    "echo": lambda *args: print(" ".join(args)),  # print all arguments
    "type": lambda args: display_type(
        args
    ),  # check if command is builtin or executable
    "pwd": lambda *_: print(os.getcwd()),  # print current working directory
    "cd": lambda *args: change_directory(args),  # change directory
    "history": lambda args, n: history(args, n),
}


def on_exit(exit_code, history_buffer):
    load_to_env_history_file(history_buffer)

    sys.exit(int(exit_code))


# print type of command: builtin, executable, or not found
def display_type(command):
    if command in COMMANDS:
        print(f"{command} is a shell builtin")
        return 1

    full_path = executable(command)
    if full_path:
        print(f"{command} is {full_path}")
        return 1

    print(f"{command}: not found")
    return 0


# handle the cd command: change directory or print error
def change_directory(args):
    if len(args) >= 2:
        print("cd: too many arguments")  # cd should receive only one argument
    else:
        dir = args[0]
        if dir == "~":  # handle home directory shortcut
            dir = os.environ["HOME"]
        exists = os.path.isdir(dir)
        if exists:
            os.chdir(dir)  # change current working directory
            return 1
        else:
            print(f"cd: {dir}: No such file or directory")


def history(buffer, n=0):
    if n >= len(buffer):
        n = 0

    for index, cmd in enumerate(buffer[-n:]):
        print(f"    {index + 1} {cmd}")

    return True


# helper function
def write_history_to_file(filename, history_buffer, mode):
    try:
        with open(filename, mode, encoding="utf-8") as f:
            for line in history_buffer:
                f.write(line + "\n")
    except IOError as e:
        print(f"history: error writing '{filename}': {e}")


def load_history_into_memory(history, history_buffer):
    for cmd in history:
        readline.add_history(cmd)
        history_buffer.append(cmd)


def history_handle(
    command_with_args, history_buffer, command, last_appended_history_index
):
    SKIP_LOOP = "continue"
    PROCESS_NORMALLY = "done"
    n = 0

    has_args = len(command_with_args) > 1
    has_two_args = len(command_with_args) > 2

    if has_args:
        try:
            n = int(command_with_args[1])
        except ValueError:
            n = 0

        if has_two_args and command_with_args[1] == "-r":
            filename = command_with_args[2]
            history = parse_history_file(filename)
            load_history_into_memory(history, history_buffer)
            return (SKIP_LOOP, last_appended_history_index)

        if has_two_args and command_with_args[1] == "-w":
            filename = command_with_args[2]
            write_history_to_file(filename, history_buffer, "w")
            return (SKIP_LOOP, last_appended_history_index)

        if has_two_args and command_with_args[1] == "-a":
            filename = command_with_args[2]
            if last_appended_history_index < len(history_buffer):
                write_history_to_file(
                    filename, history_buffer[last_appended_history_index:], "a"
                )
                last_appended_history_index = len(history_buffer)
            return (SKIP_LOOP, last_appended_history_index)

    COMMANDS[command](history_buffer, n)
    return (PROCESS_NORMALLY, last_appended_history_index)


def load_from_env_history_file(history_buffer):
    try:
        HISTFILE = os.environ.get("HISTFILE")

        if HISTFILE and os.path.exists(HISTFILE):
            history = parse_history_file(HISTFILE)
            load_history_into_memory(history, history_buffer)
    except Exception as e:
        print(f"history: failed to load from $HISTFILE: {e}")


def load_to_env_history_file(history_buffer):
    try:
        HISTFILE = os.environ.get("HISTFILE")
        if HISTFILE and os.path.exists(HISTFILE):
            write_history_to_file(HISTFILE, history_buffer, "w")
    except Exception as e:
        print(f"history: failed to write to $HISTFILE: {e}")
