# parse user input handling quotes and backslashes correctly
def parse_input(string):
    temp = ""
    parsed_string = []
    is_open_single_quote = False
    is_open_double_quote = False

    index = 0
    length = len(string)
    skip_next = False

    for index in range(length):
        if skip_next:
            skip_next = False
            continue

        char = string[index]

        # toggle single quote flag (ignore if inside double quotes)
        if char == "'" and not is_open_double_quote:
            is_open_single_quote = not is_open_single_quote
            continue  # skip quote character itself

        # toggle double quote flag (ignore if inside single quotes)
        if char == '"' and not is_open_single_quote:
            is_open_double_quote = not is_open_double_quote
            continue  # skip quote character itself

        # escape next character with backslash (only outside quotes)
        if char == "\\":
            if not (is_open_single_quote or is_open_double_quote):
                if index + 1 < length:
                    temp += string[index + 1]  # add escaped character literally
                    skip_next = True
                continue  # skip backslash itself

            if is_open_double_quote:
                if index + 1 < length:
                    next_char = string[index + 1]  # add character literally
                    if next_char in ['"', "\\"]:
                        temp += next_char
                    else:
                        temp += "\\" + next_char
                    skip_next = True
                continue  # skip backslash itself

        # split by space outside quotes
        if char == " " and not (is_open_single_quote or is_open_double_quote):
            if temp != "":
                parsed_string.append(temp)
                temp = ""
            continue  # skip space as it's a separator

        temp += char  # add character to current token

    # add last token if exists
    if temp != "":
        parsed_string.append(temp)

    return parsed_string


def parse_pipeline(input):
    pipeline = []
    current = []

    for token in input:
        if token == "|":
            if current:
                pipeline.append(current)
                current = []
        else:
            current.append(token)

    if current:
        pipeline.append(current)

    return pipeline


def parse_history_file(file):
    history = []

    try:
        with open(file, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    history.append(line)
    except FileNotFoundError:
        print(f"history: cannot open file '{file}'")

    return history
