# Ship Movement Predictor

Takes AIS geo data of ship movement and plots them on a map.

PEP8 compliant, ignoring space identantion requirement (W191, E265).

Module requirements
------
Use pip3 or Anaconda for packages management. Using pip on Windows use Gohlke's binary packages (https://www.lfd.uci.edu/~gohlke/pythonlibs/) if the PiP package isn't working.

- cartopy (*)
- feather-format
- geopandas (really slow without)
- matplotlib
- pyepsg
- pyproj
- scipy

### if you are using pip on Linux
(*) Cartopy in PyPi repository currently doesn't install. So it has to be installed from distro. With debian based:

    apt install cartopy
    pip uninstall shapely
    pip install --no-binary shapely shapely

"The Shapely wheels on PyPI contain their own version of GEOS and you will need to avoid them by using pip's --no-binary option. This will install a shapely package which has extension modules linked against your system GEOS library." -- https://github.com/Toblerity/Shapely/issues/651#issuecomment-434818437

Usage
-----
Running for the first time downloads natural earth map data which can take a minute.
