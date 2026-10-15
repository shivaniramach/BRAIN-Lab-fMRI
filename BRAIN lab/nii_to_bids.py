# This program converts raw data off the fMRI scanner to the BIDS structure
import json
import re
import shutil
from pathlib import Path
from dicom_to_nii import dcm_to_nii

# Stage one - convert raw data (dicom) to nii
inputfolder = Path("/dicom data")
outputfolder = Path("/nii data")

dcm_to_nii(inputfolder, outputfolder)

# Stage 2 - put into BIDs structure
