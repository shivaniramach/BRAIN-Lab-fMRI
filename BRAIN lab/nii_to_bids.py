# This program converts raw data off the fMRI scanner to the BIDS structure
import json
import re
import shutil
from pathlib import Path

# Matching keywords in the converted file name to BIDS structure
SERIES_MAP = [
    # (keyword, datatype, suffix, entities)
    ("math_unjudged", "func", "bold", {"task": "math_unjudged"}),
    ("math_judged", "func", "bold", {"task": "math_judged"}),
    ("rest", "func", "bold", {"task": "rest"}),
    ("speech_prep", "func", "bold", {"task": "speech_prep"}),

]

EXTENSIONS = (".nii.gz", ".nii", "json", ".bval", ".bvec", ".tsv")

def clean(label):
    #BIDS labels must be alphanumeric only
    return re.sub(r"[^A-Za-z0-9]", "", label)

# Splitting the file name into its base name and extension, because Path.suffix cannot handle the nii extension correctly
def split_ext(path):
    for ext in EXTENSIONS:
        if path.name.endswith(ext):
            return path.name[:-len(ext)], ext
    return None, None


def nii_to_bids(nii_folder, bids_folder, session=None):
    nii_folder = Path(nii_folder)
    bids_folder = Path(bids_folder)
    bids_folder.mkdir(parents=True, exist_ok=True)
    pass
    # Required json file

