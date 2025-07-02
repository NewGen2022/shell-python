# PyShell – A Python Shell from Scratch

**PyShell** (working title, originally `shell-python`) is a miniature Unix-like shell implemented in Python.  
It was built from the ground up as a learning project inspired by the [CodeCrafters "Build your own Shell"](https://app.codecrafters.io/courses/shell/overview) challenge.  
The goal was to deeply understand how command-line interpreters (shells) work by implementing one from scratch.  
This shell supports core features of a POSIX shell, including command parsing, pipelines (`|`), I/O redirection (`>`, `>>`, `2>`, `2>>`), tab auto-completion, and a suite of built-in commands (`echo`, `cd`, `pwd`, `exit`, `history`, `type`).  
Throughout development, each feature was added step-by-step with careful consideration, resulting in a fully functional shell and a deeper understanding of system programming and CLI tools.

---

## 🚀 Project Motivation and Goals

The project’s purpose is to **build a shell from scratch** to learn how real command-line shells work under the hood.  
By reimplementing a shell, the project covers concepts such as:

- Creating a Read-Evaluate-Print Loop (REPL) that continually reads user input and executes commands.
- Parsing user input with proper handling of quotes and escape characters (similar to a shell grammar).
- Executing external programs and built-in commands.
- Handling Unix process management for pipelines (using low-level `fork()` and `exec()` calls in Python via the `os` module).
- Managing file descriptors for I/O redirection (redirecting `stdout`/`stderr` to files or pipes).
- Implementing auto-completion for command names (as shells do when pressing TAB).
- Maintaining a command history (with navigation via arrow keys and persistence across sessions).

The ultimate goal was educational: to gain **deep understanding** of shell internals (instead of just reading about it) by implementing each feature and solving the challenges that arise.  
This is evident in how each piece of functionality was added incrementally and thoughtfully, mirroring the progression of the Codecrafters course.  
The result is a mini-shell that, while not as fully featured as Bash or Zsh, behaves similarly in many aspects.  
It’s written in a clean Python style, making it easy to read and extend, and demonstrating competence in systems programming concepts using Python.

---

## ✨ Features and Implementation

### 🔄 Prompt & REPL Loop
- Prints `$ ` and waits for user input in a continuous loop.
- Reads, parses, executes commands — repeats until exit.
- Handles invalid commands gracefully (`command not found`).

### 🚀 Executing External Commands
- If a command is not built-in, searches `$PATH` and runs it as external program.
- Uses `subprocess.run()` for simple commands, `os.execvp()` and `fork()` for pipelines.

### 🔧 Built-in Commands
- `exit [code]` – exits shell.
- `echo [args...]` – prints args.
- `pwd` – current directory.
- `cd <dir>` – change directory, handles `cd ~`.
- `type <cmd>` – shows if built-in, external, or not found.
- `history n` — print last `n` commands, or all if `n` not given.  
- `history -w <file>` — write current history to file.  
- `history -r <file>` — read history from file.  
- `history -a <file>` — append new entries to file.

### 📝 Command Parsing & Quoting
- Splits input by spaces, respects:
  - `'single quotes'`
  - `"double quotes"`
  - `\` for escaping

### 📁 I/O Redirection
- `>`, `1>`: stdout overwrite
- `>>`, `1>>`: stdout append
- `2>`, `2>>`: stderr overwrite/append
- Multiple redirects supported.  
- Uses Python’s file objects & swaps `sys.stdout` / `sys.stderr` for built-ins.

### 🔗 Pipelines
- Supports arbitrary `cmd1 | cmd2 | cmd3`.
- Internally:
  - Parses by `|`.
  - Sets up pipes (`os.pipe()`), forks, uses `dup2`.
  - Built-ins run in main process with temporary fd swaps.

### 🔥 Autocompletion
- Press TAB to complete built-ins + executables from `$PATH`.
- Press TAB again to list multiple options.
- Uses `readline`.

### 📜 Command History & Persistence
- Up/Down keys navigate.
- `history` lists with numbering.
- `HISTFILE` env var auto-loads/saves history on start/exit.

---

## 💻 Usage Examples

```bash
$ pwd
/home/user/projects/shell-python

$ cd /tmp
$ pwd
/tmp

$ echo "Hello World"
Hello World

$ echo Shells are 'fun to use'
Shells are fun to use

$ echo "She said: \"Hello\""
She said: "Hello"

$ echo A\ B C
A B C

$ echo "First" > out.txt
$ echo "Second" >> out.txt
$ cat out.txt
First
Second

$ ls nonexistent 2> err.log
$ cat err.log
ls: cannot access 'nonexistent': No such file or directory

$ echo "one two\nthree four" | grep two | awk '{print $2}'
two

$ history
    1 cd /tmp
    2 pwd
    3 echo "Hello World"
    4 echo "First" > out.txt
    5 echo "Second" >> out.txt
    6 ls nonexistent 2> err.log
    7 echo "one two\nthree four" | grep two | awk '{print $2}'
```

### 🚀 Running the Shell
```bash
python3 main.py
```
- Runs on Linux/macOS
- Exit with exit

### ✅ Conclusion
PyShell is a complete educational shell replicating many Bash/Zsh behaviors:
- Proves skill with Python for low-level Unix concepts: processes, pipes, file descriptors.
- Shows parsing care (quotes, escapes) like real shells.
- Demonstrates thoughtful CLI UX: autocompletion, history, arrow keys.
- Was not a mere tutorial copy — each step manually designed, reflecting real understanding.
- It’s both a working toy shell and showing deep system-level programming competence.
