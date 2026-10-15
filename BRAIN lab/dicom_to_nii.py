from pathlib import Path 
import subprocess

# Converting the DICOM files to nii - but first making the directories
inputfolder = Path("dicom data") # this is the file structure on my MacBook, might need to change in lab
outputfolder = Path("nii data")

print("Input", inputfolder)
print("Output", outputfolder)

inputfolder.mkdir(parents = True, exist_ok = True)
outputfolder.mkdir(parents = True, exist_ok = True)

def dcm_to_nii(input_folder, output_folder):

    # Convert the files while catching errors
    cmd = ["dcm2niix", "-z", "y", "-o", str(output_folder), str(input_folder)]

    try:
        result = subprocess.run(
            cmd,
            capture_output = True,
            text = True,
            check = True
        )
        print(result.stdout)
    except FileNotFoundError:
        print("dcm2nii is not installed")
    except subprocess.CalledProcessError as e:
        print("dicom2niix failed")
        print(e.stderr)
    return False
# Checking the BIDS file structure

def list_output(output_folder):
    for f in sorted(Path(output_folder).rglob("*")): # .rglob() is a method for Path objects, the '*' is a wildcard for everything
        if f.is_file(): # .is_file is a method that points to an existing file
            print(f)

if __name__ == "__main__":
    dcm_to_nii(inputfolder, outputfolder)
    list_output(outputfolder)


