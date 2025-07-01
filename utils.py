import os


# check if a command is in PATH and is executable
def executable(command):
    path_env = os.environ["PATH"]
    folders_to_search = path_env.split(":")

    for folder in folders_to_search:
        if not os.path.isdir(folder):
            continue
        full_path = os.path.join(folder, command)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path  # return full path if executable is found


def find_executables_starting_with(prefix):
    path_env = os.environ["PATH"]
    folders_to_search = path_env.split(":")
    matches = []

    for folder in folders_to_search:
        if not os.path.isdir(folder):
            continue
        for file in os.listdir(folder):
            if file.startswith(prefix):
                full_path = os.path.join(folder, file)
                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    matches.append(file + " ")  # add full path if executable is found
    return sorted(matches)
