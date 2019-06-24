# Ship Movement Predictor

Takes AIS geo data of ship movement and plots them on a map.

Module requirements
------
Install packages with pip3.

### from default pypi repository
- matplotlib
- pyproj
- scipy
- shapely (only on Linux)

### on windows install wheels package: http://www.lfd.uci.edu/~gohlke/pythonlibs/
- cartopy
- shapely

### on linux install from distro repository
- cartopy

Also without 'geopandas' performance is really slow. For installation you need (use wheels)
- GDAL 2.4 (3.0 not supported by Fiona)
- fiona
- rtree

Usage
-----
Running for the first time downloads natural earth map data which can take a few minutes.
