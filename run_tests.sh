#!/bin/bash

# create a virtual enviornment and install requirements
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -q

# clear out old benchmarks (optional, should use a command line arg)
rm -rf .benchmarks

# Declare an array of string with type
declare -a Versions=(
    "0.20.4"
    "0.21.4"
    "0.22.4"
    "0.23.1"
    "0.24.3"
    "0.25.3"
    "0.26.1"
    "0.27.4"
    "0.28.1"
    "0.29.1"
    "0.30.1"
    "0.31.3"
    "0.32.1"
    "0.33.3"
    "0.34.0"
    )
 
# Iterate the string array using for loop
for version in ${Versions[@]}; do
    pip install pyvista==$version -q
    pytest --benchmark-save=$version -q
done

mkdir hist -p
pytest-benchmark compare --histogram hist/hist --group-by name --sort fullname 1> /dev/null

rm -rf .venv
