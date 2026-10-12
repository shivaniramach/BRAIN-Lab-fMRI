from pathlib import Path 
import subprocess

# if the folders to store dicom data and nii data dont exist, this block checks for that
""" # folder that main.py is in, adding the directories to the same folder
base = Path(__file__).resolve().parent

inputfolder = base / "dicom data"
outputfolder = base / "nii data"

print("Input", inputfolder)
print("Output", outputfolder) """


# Converting the DICOM files to nii - but first making the directories
inputfolder = Path("dicom data") # these is the file structure on my MacBook, might need to change in lab
outputfolder = Path("nii data")

# Check if there is a valid output folder 
Path(outputfolder).mkdir(parents=True, exist_ok=True)
Path(inputfolder).mkdir(parents=True, exist_ok=True)

# Convert the files while catching errors
cmd = ["dcm2niix", "-z", "y", "-o", str(outputfolder), str(inputfolder)]

try:
    result = subprocess.run(
        cmd,
        capture_output = True,
        text = True,
        check = True
    )
    print(result.stdout)

except subprocess.CalledProcessError as e:
    print("dicom2niix failed")
    print(e.stderr)

# Checking the BIDS file structure

for f in sorted(Path("/nii data").rglob("*")):
    print(f) 


