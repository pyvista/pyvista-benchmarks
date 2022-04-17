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

# create a virtual enviornment and install requirements
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -q

# clear out old benchmarks (optional, should use a command line arg)
rm -rf .benchmarks

# download examples
rm -rf examples/
download_example "examples/04-lights" "plotter_builtins.py"
download_example "examples/01-filter" "contouring.py"


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
    echo "Benchmarking PyVista" $version
    pip install pyvista==$version -q
    pytest --benchmark-save=$version -v --benchmark-quiet --disable-warnings --no-header -k lighting
done

# mkdir hist -p
# pytest-benchmark compare --histogram hist/hist --group-by name --sort fullname 1> /dev/nullcase 
# rm -rf .venv
