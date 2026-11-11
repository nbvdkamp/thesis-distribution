#!.venv/bin/python

from shared import *
import pandas
import pypst
import re
import os
import numpy
from pathlib import Path
from shared_typst import make_tables

pattern_regex = re.compile(r'Search (.*)\.')
dir_regex = re.compile(r'^examples/(.*)/.*')

files = get_files('.v')
if 'examples/correctness/injective.v' in files:
    # It has multiple Search commands, in this script we assume one so skip it
    files.remove('examples/correctness/injective.v')

if len(files) == 0:
    exit(0)

runs = 3

methods = [
    Method.NO_UNFOLDING,
    Method.NO_UNFOLDING_WITH_CACHING,
    Method.CBV_UNFOLDING,
    Method.UNFOLDING_DURING_MATCHING_NO_CACHE,
    Method.UNFOLDING_DURING_MATCHING_UNFOLDED_CACHE_ONLY,
    Method.UNFOLDING_DURING_MATCHING_SUBTERM_CACHE_ONLY,
    Method.UNFOLDING_DURING_MATCHING,
]

names = {
    Method.NO_UNFOLDING: "No unfolding",
    Method.NO_UNFOLDING_WITH_CACHING: "No unfolding (with cache)",
    Method.CBV_UNFOLDING: "Method 1",
    Method.UNFOLDING_DURING_MATCHING_NO_CACHE: "Method 2",
    Method.UNFOLDING_DURING_MATCHING_UNFOLDED_CACHE_ONLY: "Method 3",
    Method.UNFOLDING_DURING_MATCHING_SUBTERM_CACHE_ONLY: "Method 4",
    Method.UNFOLDING_DURING_MATCHING: "Method 5",
}

method_names = [names[m] for m in methods]
col = pandas.Index(["File"] + method_names)
df_time = pandas.DataFrame(columns=col)
df_memory = pandas.DataFrame(columns=col)

bench_dir = "results/"
prefix = bench_dir
ref_time = ""
ref_memory = ""
try:
    matches = [dir_regex.match(f)[1] for f in files]
    if all(x == matches[0] for x in matches):
        dir_name = matches[0]
        prefix = f"{bench_dir}{dir_name}_"
        ref_time = f" <benchmark_{dir_name}_time>"
        ref_memory = f" <benchmark_{dir_name}_memory>"
except:
    pass

for file in files:
    if file.startswith('examples/stdlib') or file.startswith('examples/unimath'):
        with open(file) as f:
            last_line = f.read().splitlines()[-1]
            try:
                pattern = pattern_regex.match(last_line)[1]
                index = f'```rocq {pattern}```'
            except:
                index = f'@{Path(file).name}'
    else:
        index = f'@{Path(file).name}'
    
    failed = set()

    print(f'Running file: {file}', sep='')
    for i in range(0, runs):
        outputs = []
        for method in methods:
            if method in failed:
                # Skip method after first OOM
                o = Output(method)
                o.out_of_memory = True
                outputs.append(o)
            else:
                outputs.append(run_file(file, method))
        first = outputs[0]

        if len(methods) > 1 and not first.commands_match(outputs[1]):
            print(f"Error: Commands don't match for {file}")
            exit(1)

        for i in range(0, len(first.commands)):
            if first.commands[i].command.startswith('Search'):
                time = [index]
                memory = [index]
                for output in outputs:
                    if output.out_of_memory:
                        time.append(numpy.nan)
                        memory.append(numpy.nan)
                        failed.add(output.method)
                    else:
                        time.append(output.commands[i].seconds * 1000) # to ms
                        memory.append(output.max_memory_usage / 1e9) # to GB
                df_time = pandas.concat([df_time, pandas.DataFrame([time], columns=col)])
                df_memory = pandas.concat([df_memory, pandas.DataFrame([memory], columns=col)])

#Write the results to csv (and read them back in to get rid of annoying datatype problem)
time_filename = uniquify(prefix + "time.csv")
os.makedirs(os.path.dirname(time_filename), exist_ok=True)
df_time.to_csv(time_filename, index=False)
df_time = pandas.read_csv(time_filename)

memory_filename = uniquify(prefix + "memory.csv")
os.makedirs(os.path.dirname(memory_filename), exist_ok=True)
df_memory.to_csv(memory_filename, index=False)
df_memory = pandas.read_csv(memory_filename)

make_tables(df_time, df_memory, prefix, ref_time, ref_memory)
