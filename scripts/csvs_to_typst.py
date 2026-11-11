#!.venv/bin/python

import sys
import re
import pandas
from shared_typst import make_tables
from shared import get_files, flags

bench_dir = "results/"
prefix_regex = re.compile(r'(.*)time[0-9]*\.csv')
files = get_files('.csv')
first = files[0]
second = files[1]

m = prefix_regex.match(first)

if m:
    prefix = m[1]
    dir_name = prefix.removeprefix(bench_dir).split('/')[-1]
    ref_time = f" <benchmark_{dir_name}time>"
    ref_memory = f" <benchmark_{dir_name}memory>"

    df_time = pandas.read_csv(first)
    df_memory = pandas.read_csv(second)

    make_tables(df_time, df_memory, prefix, ref_time, ref_memory)
else:
    print("Invalid arguments")