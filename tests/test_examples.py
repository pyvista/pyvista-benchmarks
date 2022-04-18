import glob
import os
import pathlib

import pytest

from pyvista._version import version_info

THIS_PATH = pathlib.Path(__file__).parent.resolve()

# fetch paths of examples
EXAMPLES_PATH = os.path.join(THIS_PATH, "..", "pyvista", "examples")

# this examples segfault for certain minor versions of pyvista
RESTRICTED_EXAMPLES = {
    "02-plot/linked.py": [27, 28, 29, 30],
    "02-plot/gif.py": [27, 28, 29, 30],
    "02-plot/orbit.py": [30],
}

# extract last directory and example name
examples = glob.glob(os.path.join(EXAMPLES_PATH, "**", "*.py"), recursive=True)
EXAMPLES = []
for example in examples:
    EXAMPLES.append(
        os.path.join(
            os.path.basename(os.path.dirname(example)),
            os.path.basename(example),
        )
    )


def run_script(path):
    """Execute a python script."""
    with open(path) as fid:
        exec(fid.read())


@pytest.mark.parametrize("example", EXAMPLES)
def test_example(benchmark, example):
    if example in RESTRICTED_EXAMPLES:
        minor_version = version_info[1]
        if minor_version in RESTRICTED_EXAMPLES[example]:
            raise Exception(
                f"{example} is known to segfault on pyvista==0.{minor_version}.X"
            )
    benchmark(run_script, path=os.path.join(EXAMPLES_PATH, example))
