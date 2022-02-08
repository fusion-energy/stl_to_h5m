[![CI with install](https://github.com/fusion-energy/stl_to_h5m/actions/workflows/ci_with_install.yml/badge.svg)](https://github.com/fusion-energy/stl_to_h5m/actions/workflows/ci_with_install.yml)



This is a minimal Python package that provides a Python API interfaces for converting multiple STL files into a DAGMC h5m file ready for use in simulation.

Convert STL files to a DAGMC h5m file complete with material tags and ready for use neutronics simulations.

**warning** this approach does not imprint and merge the geometry and therefore
requires that the STL files do not overlap. Overlaps could lead to particles
being lost during transport. If imprinting and merging is required consider
using [cad-to-h5m](https://github.com/fusion-energy/cad_to_h5m).

It is strongly advised to used the DAGMC overlap checker to check the
resulting h5m file (see checking for overlaps secton below).


# Installation - Conda

This single line command should install the package and dependencies (including moab)

```bash
conda install -c fusion-energy -c conda-forge stl_to_h5m
```

# Installation - Pip + Conda

These two commands should install the package and dependencies. Moab requires a separate install as it is not available on ```pip```

```bash
conda install -c conda-forge moab
pip install stl_to_h5m
```

# Usage - single file

To convert a single STL file into a h5m file. This also tags the volume with the
material tag m1.

```python
from stl_to_h5m import stl_to_h5m

stl_to_h5m(
    files_with_tags=[('part1.stl', 'mat1')],
    h5m_filename='dagmc.h5m',
)
```

# Usage - multiple files

To convert multiple STL files into a h5m file. This also tags the relevant 
volumes with material tags called m1 and m2.

```python
from stl_to_h5m import stl_to_h5m

stl_to_h5m(
    files_with_tags=[
        ('part1.stl', 'mat1'),
        ('part2.stl', 'mat2')
    ],
    h5m_filename='dagmc.h5m'
)
```

# Usage - checking for overlaps

To check for overlaps in the resulting h5m file one can use the DAGMC
overlap checker. -p is the number of points to check on each line

```bash
conda install -c conda-forge dagmc
overlap_check dagmc.h5m -p 1000
```

# Acknowledgments

This package is largely based on [a script](https://gist.github.com/pshriwise/52452c37d4b7dd89bdc9374e13c35157) by @pshriwise
