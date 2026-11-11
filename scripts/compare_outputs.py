#!/bin/python

import os
import difflib
from shared import *
import re

expected_new_results_pattern = re.compile(r'.*\(\*\s*New: (.*)\s*\*\)')
new_results_pattern = re.compile(r"\s*\+([a-zA-Z_][a-zA-Z_0-9.']*)\s*:.*")
files = get_files('.v')

additional: int = 0
missing: int = 0
commands_with_unexpected_output: int = 0

def diff(a: str, b: str) -> list[str]:
    return list(difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm=''))

for file in files:
    old = run_file(file, Method.NO_UNFOLDING)
    new = run_file(file, Method.UNFOLDING_DURING_MATCHING)
    if not old.commands_match(new):
        print(f"Error: Commands don't match for {file}")
        exit(1)

    print(f'\nFILE {file}:')

    for (o, n) in zip(old.commands, new.commands):

        if n.command.startswith('Search'):
            expected_new_results = []
            m = expected_new_results_pattern.match(n.command)
            if m:
                expected_new_results = sorted(m.group(1).split())

            if not o.command.startswith('Search'):
                non_search_command_change += 1

            # Sort the outputs so ordering doesn't affect the diff
            d = diff('\n'.join(sorted(o.output)), '\n'.join(sorted(n.output)))[2:] #Drop the first lines that only contain --- and +++
            new_lines = [line for line in d if line.startswith('+')]
            missing_lines = [line for line in d if line.startswith('-')]
            additional += len(new_lines)
            missing += len(missing_lines)

            print(o.command)

            if len(d) > 0:
                # Only print the diff if it's under 20 lines
                if len(d) < 20:
                    print('\n'.join(map(lambda s : '\t' + s, d)))
                else:
                    print(f'{len(d)} line diff omitted +{len(new_lines)}/-{len(missing_lines)}')

            new_results = []
            for x in new_lines:
                m = new_results_pattern.match(x)
                if m:
                    new_results.append(m.group(1))

            if (sorted(new_results) != expected_new_results or len(missing_lines) > 0):
                commands_with_unexpected_output += 1
                print("Output did not match expectation")
            else:
                print("✓ Output matches")
        elif o.output != n.output:
            print("Error: non-Search command's output changed")

print(f'\nFound {additional + missing} differences (+{additional}/-{missing})')

if commands_with_unexpected_output > 0:
    print(f"Error: output didn't match the expected result ({commands_with_unexpected_output } times)")