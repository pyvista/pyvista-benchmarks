import pytest

import pyvista


def create_plot_uniform_grid(dim=None, plot=None):
    uniform_grid = pyvista.UniformGrid((dim, dim, dim))
    if plot:
        uniform_grid.plot()


@pytest.mark.parametrize("plot", [True, False])
@pytest.mark.parametrize("dim", [1, 10, 100, 500, 1000])
def test_uniform_grid(benchmark, dim, plot):
    benchmark(create_plot_uniform_grid, dim=dim, plot=plot)
