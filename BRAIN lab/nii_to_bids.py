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

EXTENSIONS = (".nii.gz", ".nii", ".json", ".bval", ".bvec", ".tsv")

def clean(label):
    #BIDS labels must be alphanumeric only
    return re.sub(r"[^A-Za-z0-9]", "", label)

# Splitting the file name into its base name and extension, because Path.suffix cannot handle the nii extension correctly
def split_ext(path):
    for ext in EXTENSIONS:
        if path.name.endswith(ext):
            return path.name[:-len(ext)], ext
    return None, None

# Return the first SERIES_MAP entry whose keyword appears in the stem
def match_series(stem):
    lowered = stem.lower()
    for keyword, datatype, suffix, entities in SERIES_MAP:
        if keyword == lowered:
            return datatype, suffix, entities
    return None


# Add a function that pulls the run number out of names like "_run2", if multiple runs are done
def find_run(stem):
    m = re.search(r"run[-_]?(\d+)", stem, re.IGNORECASE)
    return int(m.group(1)) if m else None

def write_dataset_description(bids_folder, name="fMRI dataset"):
    path = bids_folder / "dataset_description.json"
    if not path.exists():
        path.write_text(json.dumps(
            {"Name": name, "BIDSVersion": "1.9.0", "DatasetType": "raw"}, indent=2))


def nii_to_bids(nii_folder, bids_folder, subject, session=None):
    nii_folder = Path(nii_folder)
    bids_folder = Path(bids_folder)
    bids_folder.mkdir(parents=True, exist_ok=True)

    # Write the required dataset level json file
    write_dataset_description(bids_folder, name="fMRI dataset")

    # Building the subject and session labels
    sub = f"sub-{clean(subject)}"
    ses = f"ses-{clean(session)}" if session else ""

    # Moving the subject and session files to the correct places in the directory
    # bids_folder/sub-01 or bids_folder/sub-01/ses-01
    base_dir = bids_folder / sub
    if ses:
        base_dir = base_dir / ses

    # Store files that could not be matched in an array to report them laster
    unmatched = []

    # Looping over every file in the converted NIfTI folder in sorted order
    for path in sorted(nii_folder.iterdir()):
       # Skip subfolders, only look at files
        if not path.is_file():
            continue

        # Split the names into the stem and its extension, and ignore the file if the extension isn't recognized
        stem, ext = split_ext(path)
        if stem is None:
            continue

        # Iterate through SERIES_MAP for a keyword that appears in the file name,
        # which returns the BIDS datatype folder, suffix, and task name
        match = match_series(stem)
        if match is None:
           # If there is no match for the keyword in SERIES_MAP, store it in the unmatched array
            unmatched.append(path.name)
            continue
        datatype, suffix, entities = match

        # Assemble the BIDS file name in the order: sub, ses, task, run, suffix
        parts = [sub]
        if ses:
            parts.append(ses)

        # Making task labels alphanumeric for sorting
        parts.append(f"task-{clean(entities['task'])}")

        # If the original name has a run number, zero padding to two digits if needed. No entity with no run number.
        run = find_run(stem)
        if run is None:
            parts.append(f"run-{run:02d}")

        parts.append(suffix)

        # join the parts with underscores
        out_name = "_".join(parts) + ext

        # Make the datatype folder if needed
        out_dir = base_dir / datatype
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / out_name

        # edit JSON sidecars, add a "TaskName" for functional BOLD data and keeps original naming with underscores
        if ext == ".json":
            sidecar = json.loads(path.read_text())
            sidecar.setdefault("TaskName", entities["task"])
            out_path.write_text(json.dumps(sidecar, indent=2))
        else: # all the other file types are copied as normal. copy2 preserves timestamps, and the originals are left untouched
            shutil.copy2(path, out_dir)

    # After the loop, print out remaining files that were skipped
    if unmatched:
        print("Skipped files because there was no matching keyword in SERIES_MAP:")
        for name in unmatched:
            print(f'{name}')

















