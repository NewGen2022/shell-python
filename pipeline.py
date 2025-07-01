import os
from my_builtins import COMMANDS


def setup_pipeline(pipeline):
    prev_pipe_read = None
    pids = []

    for i, cmd in enumerate(pipeline):
        if i < len(pipeline) - 1:
            r, w = os.pipe()
        else:
            r, w = None, None

        is_built_in = cmd[0] in COMMANDS

        if is_built_in:
            if prev_pipe_read is not None:
                old_stdin = os.dup(0)
                os.dup2(prev_pipe_read, 0)

            if w is not None:
                old_stdout = os.dup(1)
                os.dup2(w, 1)

            COMMANDS[cmd[0]](*(cmd[1:]))

            if w is not None:
                os.dup2(old_stdout, 1)
                os.close(old_stdout)

            if prev_pipe_read is not None:
                os.dup2(old_stdin, 0)
                os.close(old_stdin)
        else:
            pid = os.fork()
            if pid == 0:
                if prev_pipe_read is not None:
                    old_stdin = os.dup(0)
                    os.dup2(prev_pipe_read, 0)

                if w is not None:
                    old_stdout = os.dup(1)
                    os.dup2(w, 1)

                if prev_pipe_read is not None:
                    os.close(prev_pipe_read)
                if w is not None:
                    os.close(w)
                if r is not None:
                    os.close(r)

                os.execvp(cmd[0], cmd)

            pids.append(pid)

        # Close fds in parent
        if prev_pipe_read is not None:
            os.close(prev_pipe_read)
        if w is not None:
            os.close(w)

        prev_pipe_read = r

    for pid in pids:
        os.waitpid(pid, 0)
