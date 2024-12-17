# Living Optics add-in for Orange3 Data Mining

This add-in allows Living Optics .lo files to be ingested by Orange3, and the contents of the spectral data to be used for subsequent analysis. There are two additional widgets that are added:
NDVI, which allows NDVI calculations to be made on spectral data, with the ability to adjust the bands that are used for the calculation.
Upsample, which takes the LO sparse data format and upsamples using a nearest neighbour algorithm that's found in the LO SDK to produce 'complete' information. 

## Requirements

Living Optics SDK v1.4.4 or later.
Orange data mining v3.38 or later installed.

## Installation
Requires Linux, MacOS, or Linux tools for Windows.
From a clean machine, create a folder:

`mkdir Orange3`

`cd Orange3`

Create a venv in the folder to keep Orange separate from your other python tools, then enter the venv.

`python3 -m venv venv`
`source venv/bin/activate`

Install orange3 using pip

`pip install orange3`

Download the Living Optics SDK from our cloud service https://cloud.livingoptics.com, and copy the .tar file into the Orange3 folder. This example uses SDK1.6, but adjust the command based on the version that you download:

Unpack the SDK tarball:

`tar -xf lo_sdk-1.6.0-dist.tar`

`pip install install/lo_sdk-1.6.0-py3-none-any.whl`

Download this add-in from github by clicking the 'Download Zip' button in the 'Code' dropdown. Copy the .zip file into the Orange3 folder and unzip it if your computer has not done this automatically for you. 

`pip install orange3-lo-main/`

You can now run Orange3 from the command line

`python -m Orange.canvas`

The 'Spectroscopy' add-in (found in the Options -> Add-ins... menu) contains many useful widgets to explore spectral and hyperspectral data, and it's recommended to add this to your copy of Orange by checking the box and restarting Orange.