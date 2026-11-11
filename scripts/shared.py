import os
import sys
import time
import datetime
import subprocess
import psutil
import re
from enum import Enum

class Method(Enum):
    NO_UNFOLDING = 1
    CBV_UNFOLDING = 2
    UNFOLDING_DURING_MATCHING = 3
    UNFOLDING_DURING_MATCHING_UNFOLDED_CACHE_ONLY = 5
    UNFOLDING_DURING_MATCHING_SUBTERM_CACHE_ONLY = 4
    UNFOLDING_DURING_MATCHING_NO_CACHE = 6
    NO_UNFOLDING_WITH_CACHING = 7

class CommandOutput:
    """Represents the output corresponding to one command's output and how many seconds it took"""
    command: str
    seconds: float
    output: list[str]

    def __init__(self, command: str, seconds: float, output: list[str]) -> None:
        self.command = command
        self.seconds = seconds
        self.output = output

class Output:
    """Represents the output of a rocq run as a list of CommandOutputs"""
    commands: list[CommandOutput]
    method: Method
    max_memory_usage: int
    out_of_memory: bool

    def __init__(self, method: Method) -> None:
        self.commands: list[CommandOutput] = []
        self.method = method
        self.max_memory_usage = 0
        self.out_of_memory = False
    
    def add(self, cmd: CommandOutput):
        self.commands.append(cmd)

    def commands_match(self, other):
        if self.out_of_memory or other.out_of_memory:
            return True

        return len(self.commands) == len(other.commands) and all(map(lambda x : x[0].command == x[1].command, zip(self.commands, other.commands)))

    def update_max_memory_usage(self, current: int):
        if current > self.max_memory_usage:
            self.max_memory_usage = current

if os.getcwd().endswith('scripts'):
    os.chdir('..')

examples_dir : str = 'examples/'
executable : str = '../rocq/_build/install/default/bin/rocq'
timestamp_file: str = '../rocq/.dune-stamp'

modified_time : float = os.path.getmtime(timestamp_file)
modified_datetime = datetime.datetime.fromtimestamp(modified_time)
current_time : datetime.datetime = datetime.datetime.now()

def strip_dir(f: str) -> str:
    return f[len(examples_dir):] if f.startswith(examples_dir) else f

def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + str(counter) + extension
        counter += 1

    return path

args = sys.argv[1:]
flags: list[str] = [x for x in args if x.startswith('-')]

def get_files(extension: str) -> list[str]:
    files : list[str] = [f for f in args if not f.startswith('-') and f.endswith(extension)]

    if len(files) == 0:
        print("Error: No files passed")
        exit(1)
    
    return files

def run_file(file: str, method: Method) -> Output:
    result = Output(method)

    flags = [
        # The timing output after each command lets us know where its output ends and how long it took
        '-time',
        # Set printing width to a large number so types don't have linebreaks
        # in them and sorting the outputs doesn't mess up the diff
        '-set', 'Printing Width=1000'
    ]

    if method == Method.NO_UNFOLDING_WITH_CACHING:
        flags = flags + ['-set', 'Search No Unfolding With Caching']
    if method == Method.CBV_UNFOLDING:
        flags = flags + ['-set', 'Search Unfold Cbv']
    elif method == Method.UNFOLDING_DURING_MATCHING:
        flags = flags + ['-set', 'Search Unfold During Matching']
    elif method == Method.UNFOLDING_DURING_MATCHING_UNFOLDED_CACHE_ONLY:
        flags = flags + ['-set', 'Search Unfold During Matching Unfolded Cache Only']
    elif method == Method.UNFOLDING_DURING_MATCHING_SUBTERM_CACHE_ONLY:
        flags = flags + ['-set', 'Search Unfold During Matching Subterm Cache Only']
    elif method == Method.UNFOLDING_DURING_MATCHING_NO_CACHE:
        flags = flags + ['-set', 'Search Unfold During Matching No Cache']

    if 'unimath' in file.lower():
        flags = flags + ['-q', '-noinit', '-indices-matter', '-w', '-notation-overridden',  "-w", "-deprecated-native-compiler-option", "-native-compiler", "no", "-Q", "../UniMath/UniMath", "UniMath"]

    args = [executable, 'compile'] + flags + [file]
    process = subprocess.Popen(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    psutilprocess = psutil.Process(process.pid)

    while True:
        try:
            (stdout, stderr) = process.communicate(timeout=0.01)
            break
        except subprocess.TimeoutExpired:
            bytes_in_use = psutilprocess.memory_info().rss
            result.update_max_memory_usage(bytes_in_use)

            # Is it using more than 8GB?
            if bytes_in_use > 8e9:
                process.kill()
                process.communicate()
                result.out_of_memory = True
                return result

            time.sleep(0.02)

    if process.returncode == 0:
        pattern = re.compile(r'^Chars \d+ - \d+ \[(?P<cmd>.*)\] (?P<secs>\d+\.\d*) secs \(\d+\.\d*u,\d+\.\d*s\)$')
        lines = stdout.decode('utf-8').splitlines()
        current: list[str] = []

        f = open(file, "r")
        file_contents: list[str] = f.read().splitlines()
        f.close()

        for line in lines:
            m = pattern.match(line)
            if m:
                d = m.groupdict()
                command = d["cmd"].replace('~', ' ')

                if command.startswith('Search'):
                    # Find the full command that belonged to this short version
                    if command.endswith("..."):
                        command_prefix = command[0:-3]
                    else:
                        command_prefix = command
                    def remove_parens(s: str):
                        return s.replace('(', '').replace(')', '')

                    matches = []

                    while len(matches) == 0 and len(command_prefix) > 6:
                        matches = [x for x in file_contents if remove_parens(x).startswith(remove_parens(command_prefix.replace("inside", "in")))]
                        # strip last letter off in case we don't find any (for example if inside gets cut off and we can't replace it)
                        command_prefix = command_prefix[0:-1]

                    if len(matches) == 0:
                        print(f"Error: No matching line for {command}")
                        exit(1)
                    elif len(matches) > 1:
                        print(f"Error: Multiple matches for {command}")
                        exit(1)
                    result.add(CommandOutput(matches[0], float(d["secs"]), current))
                else:
                    result.add(CommandOutput(command, float(d["secs"]), current))
                current = []
            else:
                current.append(line)

        return result
    else:
        print('Error:')
        print(stderr.decode('utf-8'))
        exit(process.returncode)

def make_expectation_filename(file: str) -> str:
    return f"{examples_dir}/out/{file.replace('.v', '.out')}"