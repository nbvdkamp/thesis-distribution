This repository contains the test files and scripts required to reproduce the experimental results of my thesis on extending Rocq's `Search` command to work modulo unfolding.

## Dependencies

Python is required to run the scripts, opam to install the required dependencies to build Rocq itself and make for building. Once these are installed the following commands will install the necessary packages:
```bash
pip install pandas numpy pypst psutil
opam install zarith ounit2 camlzip ocamlfind dune
```

## Building Rocq and the libraries

The following commands will clone my branch of Rocq which has parallel implementations of the different methods described in the thesis:
```bash
cd ..
git clone git@github.com:nbvdkamp/rocq.git
cd rocq
git checkout all-unfolding-methods
make world ci-stdlib #the standard library is only required for examples/stdlib/
cd ../thesis-distribution
```
It is cloned to `..` as that's where the scripts expect it to be.
Then to clone and build UniMath:

```bash
cd ..
git clone git@github.com:UniMath/UniMath.git
cd UniMath
git checkout 5ed6c6b707c5e5841f62a77c2d46d6103e1f1d94
make -j8
cd ../thesis-distribution
```

## Examples

The `examples` directory contains the following subdirectories with sets of example programs:
- correctness: test cases annotated with which new results unfolding should find
- perf: standalone benchmarks for exponential blowup of unfolding
- stdlib: standard libary benchmarks
- unimath: UniMath benchmarks
- unimath_no_lambdacalculus: the same programs but with search commands excluding the lambda calculus module and the modules which use it

## Running the examples

To run a single example:
```bash
../rocq/_build/install/default/bin/rocq compile examples/correctness/injective.v
```
UniMath files require more flags:
```bash
../rocq/_build/install/default/bin/rocq compile -q '-noinit' '-indices-matter' '-w'\
    '-notation-overridden' "-w" "-deprecated-native-compiler-option" "-native-compiler" "no"\
    -Q ../UniMath/UniMath UniMath examples/unimath/symmetry.v
```

### Scripts

Each of the scripts accepts a list of `.v` files to run. `compare_outputs.py` is meant to be used with the files in `examples/correctness/` and checks if the only new results which are found correspond to the annotations in the comments after the Search commands.

```bash
python scripts/compare_outputs.py examples/correctness/*.v
```

`benchmark_search_to_typst.py` benchmarks the examples for the different methods and outputs the results as `.csv` files as well as `.typ` files (typst files containing tables). By default it runs each available method 3 times, this can be changed by changing the `runs` variable in the script. Methods can be disabled by commenting out lines in the `methods` array.

```bash
python scripts/benchmark_search_to_typst.py examples/stdlib/*.v
```