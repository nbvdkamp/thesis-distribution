#!.venv/bin/python

from shared import *
import pandas
import pypst
import re

def make_table(df: pandas.DataFrame) -> pypst.Table:
    table = pypst.Table.from_dataframe(df)
    table.stroke = "none"
    table.align = "left"
    table.add_hline(1, stroke="1.5pt")
    table.add_hline(len(df) + df.columns.nlevels, stroke="1.5pt")
    return table

def write_figure_to_file(filename: str, figure: pypst.Figure, ref: str, add_2nd_0: bool):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode="wt") as f:
        f.write("#set text(size: 10pt)\n")
        result = figure.render().replace("[nan]", "[DNF]") # Replace NaN for clarity
        if add_2nd_0:
            result = re.sub(r"\[([0-9]+\.[0-9])\]", r"[\g<1>0]", result)
        f.write(result + ref)
        print(f"Done writing {filename}")

def make_tables(df_time: pandas.DataFrame, df_memory: pandas.DataFrame, prefix: str, ref_time: str, ref_memory: str):
    # Check how many runs were performed (so we don't need to hardcode it and merged csvs just work)
    time_counts = df_time.groupby("File").count()[df_time.columns[1]]
    memory_counts = df_memory.groupby("File").count()[df_memory.columns[1]]
    first_count = time_counts.iloc[0]
    if all(time_counts == first_count) and all(memory_counts == first_count):
        runs = first_count
    else:
        raise ValueError('Not all files have the same number of runs')

    time_to_seconds = '--seconds' in flags or '-s' in flags
    if time_to_seconds:
        df_time[df_time.select_dtypes(include=['number']).columns] /= 1000
    df_time = df_time.groupby("File").agg([("mean"), ("std")])
    df_time = df_time.astype(float).round(2 if time_to_seconds else 1)

    time_table = make_table(df_time)
    time_unit = "seconds" if time_to_seconds else "ms"
    time_figure = pypst.Figure(time_table, caption=f'"Average time taken per Search command per method in {time_unit} over {runs} runs"')
    write_figure_to_file(uniquify(prefix + "time.typ"), time_figure, ref_time, add_2nd_0=time_to_seconds)

    df_memory = df_memory.groupby("File").max()
    df_memory = df_memory.astype(float).round(2)

    memory_table = make_table(df_memory)
    memory_figure = pypst.Figure(memory_table, caption=f'"Maximum memory used per Search command per method in GB over {runs} runs"')

    write_figure_to_file(uniquify(prefix + "memory.typ"), memory_figure, ref_memory, add_2nd_0=True)
