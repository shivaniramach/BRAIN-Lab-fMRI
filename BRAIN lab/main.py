from pathlib import Path
from dicom_to_nii import dcm_to_nii
from nii_to_bids import nii_to_bids

inputfolder = Path("/dicom data")
outputfolder = Path("/nii data")
bids_folder = Path("bids_root_dir")

# Step 1: DICOM to NIfTI and json sidecars
dcm_to_nii(inputfolder, outputfolder)

# Step 2: NIfTI to BIDS structure
for subj_dir in sorted(outputfolder.iterdir()):
    if subj_dir.is_dir():
        nii_to_bids(subj_dir, bids_folder, subject= subj_dir.name)








