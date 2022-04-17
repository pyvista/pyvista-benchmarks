import os

import numpy as np
import pytest
import pyvista as pv
from pyvista import examples
from pyvista._version import version_info

## setup
VOLUME = examples.download_brain()


def import_pyvista():
    os.system("python -c 'import pyvista'")


def plot_volume():
    VOLUME.plot(volume=True)


def create_gif(directory=None):
    """Taken from the pyvista gif example"""

    x = np.arange(-10, 10, 0.5)
    y = np.arange(-10, 10, 0.5)
    x, y = np.meshgrid(x, y)
    r = np.sqrt(x**2 + y**2)
    z = np.sin(r)

    # Create and structured surface
    grid = pv.StructuredGrid(x, y, z)

    # Create a plotter object and set the scalars to the Z height
    plotter = pv.Plotter(notebook=False, off_screen=True)
    plotter.add_mesh(
        grid,
        scalars=z.ravel(),
        lighting=False,
        show_edges=True,
        scalar_bar_args={"title": "Height"},
        clim=[-1, 1],
    )

    # Open a gif
    plotter.open_gif(os.path.join(directory, "wave.gif"))

    pts = grid.points.copy()

    # Update Z and write a frame for each updated position
    nframe = 15
    for phase in np.linspace(0, 2 * np.pi, nframe + 1)[:nframe]:
        z = np.sin(r + phase)
        pts[:, -1] = z.ravel()
        plotter.update_coordinates(pts, render=False)
        plotter.update_scalars(z.ravel(), render=False)

        # Write a frame. This triggers a render.
        plotter.write_frame()

    # Closes and finalizes movie
    plotter.close()


def create_plot_uniform_grid(dim=None, plot=None):
    dataset = pv.UniformGrid((dim, dim, dim))
    if plot:
        dataset.plot()


def create_plot_plane(dim=None, plot=None):
    dataset = pv.Plane(i_resolution=dim, j_resolution=dim)
    if plot:
        dataset.plot()


def test_import_pyvista(benchmark):
    benchmark(import_pyvista)


@pytest.mark.parametrize("plot", [True, False])
@pytest.mark.parametrize("dim", [10, 100, 1000])
def test_uniform_grid(benchmark, dim, plot):
    benchmark(create_plot_uniform_grid, dim=dim, plot=plot)


@pytest.mark.parametrize("plot", [True, False])
@pytest.mark.parametrize("dim", [10, 100, 1000, 2000])
def test_polydata(benchmark, dim, plot):
    benchmark(create_plot_plane, dim=dim, plot=plot)


@pytest.mark.skipif(
    version_info[1] in [27, 28, 29, 30],
    reason="Fails with pyvista>=0.27, pyvista<=0.30",
)
def test_create_gif(benchmark, tmpdir):
    benchmark(create_gif, directory=str(tmpdir))


def test_plot_volume(benchmark):
    benchmark(plot_volume)
