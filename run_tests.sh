#!/bin/bash

download_example () {
    # expects args PATH EXAMPLE_NAME
    echo -n "Downloading $1/$2..."
    wget https://raw.githubusercontent.com/pyvista/pyvista/main/$1/$2 -P $1 -q
    FILE=/etc/resolv.conf
    if test -f "$1/$2"; then
        echo " Done"
    else 
        echo " Failed"
    fi
} 

# create a virtual environment and install requirements
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -q

# clear out old benchmarks (optional, should use a command line arg)
rm -rf .benchmarks

# clone pyvista examples
rm -rf pyvista
git clone --depth 1 https://github.com/pyvista/pyvista.git

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
    "main"
    )
 
# Iterate the string array using for loop
for version in ${Versions[@]}; do
    echo "Benchmarking PyVista" $version
    if [ "$version" = "main" ]; then
        pip install .pyvista/
    else
        pip install pyvista==$version -q
    fi
    pytest tests/ --benchmark-save=$version --benchmark-quiet --disable-warnings --no-header
done

mkdir hist -p
rm hist/*
pytest-benchmark compare --histogram hist/hist --group-by name --sort fullname 1> /dev/null
