import matplotlib

import pyvista

pyvista.OFF_SCREEN = True


# ensure matplotlib plots do not show up
matplotlib.use("agg", force=True)
