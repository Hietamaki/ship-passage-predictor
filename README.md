# Ship Movement Predictor

Takes AIS geo data of ship movement and plots them on a map.

Module requirements
------
On Windows use Anaconda. On Linux packages can be manually installed with pip3 if wanted.

- cartopy (*)
- feather-format
- geopandas (really slow without)
- matplotlib
- pyepsg
- pyproj
- scipy

### if you are using manual installation on Linux
(*) Cartopy in PyPi repository currently doesn't install. So it has to be installed from distro. With debian based:

    apt install cartopy
    pip uninstall shapely
    pip install --no-binary shapely shapely

"The Shapely wheels on PyPI contain their own version of GEOS and you will need to avoid them by using pip's --no-binary option. This will install a shapely package which has extension modules linked against your system GEOS library." -- https://github.com/Toblerity/Shapely/issues/651#issuecomment-434818437

Usage
-----
Running for the first time downloads natural earth map data which can take a minute.
