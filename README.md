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
### give all the data
If you want to run everything and get all data products, make a new folder under `data/` and copy your laz files there. For everything, you will need 2 pointclouds called `before.laz` and `after.laz`. To test, you can make a copy of the folder `data/sample`. E.g.:
```
cd lidar4fire
source .venv/bin/activate
cp data/sample data/mytest
python scripts/run_all.py data/mytest
```
This creates a folder, `data/mytest/outputs`, with all the resulting GeoTIFFs computed both before and after.

### just a sample plz
If you want to run a small test on your own data, especially if the pointcloud is large, we recommend first truncating your pointclouds. Input args x_len and y_len are the lengths of the bounding box you'd like to test on in meters, counted from the lower righthand corner of the original bounding box of your pointcloud.

> 🚧 Warn
>
>    This script renames your original files as e.g. `before_original.laz`! It then replaces your original file `before.laz` with a truncated pointcloud. Don't be alarmed that the new pointcloud with the old filename is smaller.

```
python scripts/truncate_las.py --x_len 100 --y_len 100 data/mytest/before.laz
python scripts/truncate_las.py --x_len 100 --y_len 100 data/mytest/after.laz
```
Now you can proceed with the previous section and it'll run on your smaller dataset.

Note that when you're done playing with the small dataset, you'll need to delete/move the truncated .laz files and rename the originals:
```
mv data/mytest/before_original.laz data/mytest/before.laz
mv data/mytest/after_original.laz data/mytest/after.laz
```
