# handle redirection for >, 1>, 2> and
# append operation for >>, 1>>, 2>>
def handle_redirection(command_with_args):
    output_file = None
    error_file = None

    for symbol in [">", "1>", "2>", ">>", "1>>", "2>>"]:
        if symbol in command_with_args:
            redirect_index = command_with_args.index(symbol)

            redirect_to = command_with_args[redirect_index + 1]
            command_with_args = command_with_args[:redirect_index]

            if symbol in [">", "1>", "2>"]:
                if symbol == "2>":
                    error_file = open(redirect_to, "w")
                else:
                    output_file = open(redirect_to, "w")
            elif symbol in [">>", "1>>", "2>>"]:
                if symbol == "2>>":
                    error_file = open(redirect_to, "a")
                else:
                    output_file = open(redirect_to, "a")

    return command_with_args, error_file, output_file
