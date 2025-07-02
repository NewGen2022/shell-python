# PyShell – A Python Shell from Scratch

**PyShell** (originally `shell-python`) is a miniature Unix-like shell written in Python.  
It was built from scratch as a deep dive into how command-line interpreters work.  
Inspired by the [Codecrafters "Build your own Shell" challenge](https://app.codecrafters.io/courses/shell/overview), 
this implementation was coded to truly understand each component.

## 🚀 Project Motivation

The primary goals of this project were to:
- Learn **how shells like Bash actually work under the hood**, by recreating them step by step.
- Gain hands-on experience with parsing, process control (`fork`, `exec`), file descriptors, and piping.
- Build a robust, interactive CLI tool that goes beyond scripting and touches system-level programming concepts — all in Python.

## ✨ Features

This shell is surprisingly complete for a learning project. It supports:

✅ **Prompt & REPL Loop**  
- Displays `$ ` and waits for user input in a continuous loop.

✅ **Command Execution**  
- Executes both built-in and external commands found in `$PATH`.

✅ **Built-in Commands**  
- `exit [code]` — exit the shell (optionally with a status code).  
- `echo [args...]` — print arguments.  
- `pwd` — print current directory.  
- `cd <dir>` — change directory, supports `cd ~` for home.  
- `type <cmd>` — tells if `cmd` is a shell builtin or external executable.  
- `history [N]` — print last `N` commands, or all if `N` not given.  
- `history -w <file>` — write current history to file.  
- `history -r <file>` — read history from file.  
- `history -a <file>` — append new entries to file.

✅ **Quoting & Escaping**  
- Handles `'single quotes'`, `"double quotes"`, and backslashes `\`.

✅ **I/O Redirection**  
- `>` `>>` — redirect stdout (overwrite or append).  
- `2>` `2>>` — redirect stderr.

✅ **Pipelines**  
- `cmd1 | cmd2 | cmd3` — chains multiple commands, mixing built-ins and external programs.

✅ **Autocomplete (TAB completion)**  
- Completes built-in and external command names.  
- Handles multi-match: press TAB again to list options.

✅ **History with Up/Down keys**  
- Navigate previous commands with arrow keys.

✅ **History Persistence**  
- If `HISTFILE` is set, loads it on startup and saves on exit.

## 🔍 Example Usage

```bash
$ pwd
/home/user/projects/shell-python

$ cd /tmp
$ pwd
/tmp

$ echo "Hello World"
Hello World

$ echo 'multi word argument' | tr a-z A-Z
MULTI WORD ARGUMENT

$ ls nonexistent 2> errors.log
$ cat errors.log
ls: cannot access 'nonexistent': No such file or directory

$ echo First > out.txt
$ echo Second >> out.txt
$ cat out.txt
First
Second

$ history 5
    1 cd /tmp
    2 pwd
    3 echo Hello World
    4 ls nonexistent 2> errors.log
    5 echo First > out.txt

$ type cd
cd is a shell builtin

$ gi<TAB><TAB>
git grep gzip
