# lidar4fire

This repo performs analyses of .las/.laz files for forestry & fire management. It's open source, so feel free to fork and improve! Report any issues and we will address asap.

## data products
Some data products operate on a single pointcloud, but some require multiple (e.g., fuel volume reduction requires pre and post fire pointclouds).
Current analyses produce the following GeoTIFFS:
- DEM
- slope
- aspect
- fuel volume percent reduced
- powerline encroachment

## setup
Clone with git lfs:
```
git clone https://github.com/robotics-88/lidar4fire.git
git lfs pull
```

Then setup your workspace and pull dependencies into a python virtual environment with:
```
cd lidar4fire
./setup.sh
```
This will install pip and create the virtual python environment, ensuring that any pip libraries installed will not conflict with your system python libraries. This is important, do not run `pip install` commands outside the venv. You can tell the venv is activated because it will show (venv) on each line of your terminal.

## usage
Activate the virtual environment at the start of any new terminal session:
```
cd lidar4fire
source .venv/bin/activate
```