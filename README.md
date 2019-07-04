# Ship Movement Predictor

Uses historical AIS geodata of ship movement and builds a model based on knn method that can predict future ship movement.

PEP8 compliant, ignoring space identantion requirement (W191, E265). Also max line length is set to 99.

Module requirements
------
Use pip3 or Anaconda for packages management. If you are using pip on Windows, Gohlke's binary packages is required for uninstallable PyPi modules (https://www.lfd.uci.edu/~gohlke/pythonlibs/).

- alphashape
- cartopy (*)
- descartes
- feather-format
- geopandas (really slow without)
- matplotlib
- pyepsg
- pyproj
- scipy
- (tables)

### if you are using pip on Linux
(*) Cartopy in PyPi repository currently doesn't install. So it has to be installed from distro. With debian based:

    apt install cartopy
    pip3 uninstall shapely
    pip3 install --no-binary shapely shapely

"The Shapely wheels on PyPI contain their own version of GEOS and you will need to avoid them by using pip's --no-binary option. This will install a shapely package which has extension modules linked against your system GEOS library." -- https://github.com/Toblerity/Shapely/issues/651#issuecomment-434818437

Usage
-----
Running for the first time downloads natural earth map data which can take up to a minute.
