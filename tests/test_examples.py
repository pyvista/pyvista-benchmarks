import os
import pathlib
import pytest
from pyvista._version import version_info
from pyvista import examples
import pyvista as pv

THIS_PATH = pathlib.Path(__file__).parent.resolve()


def run_script(path):
    """Execute a python script."""
    with open(path) as fid:
        exec(fid.read())


@pytest.mark.skipif(version_info[1] < 30, reason="Fails with pyvista<0.30")
def test_lighting_example(benchmark):
    path = os.path.join(THIS_PATH, '..', 'examples', '04-lights', 'plotter_builtins.py')
    benchmark(run_script, path=path)
