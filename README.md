# Repository Overview

This repository contains several Python scripts designed to perform a variety of file management and image processing tasks.

## Files:

### 1. `FileDeleter.py`
This script provides a graphical user interface (GUI) for deleting specific files from a folder. The user can select a text file containing a list of filenames to delete, and a target folder from which to remove these files. The script checks if each file exists and deletes it, providing feedback on whether the deletion was successful.

#### Features:
- Uses `Tkinter` for a simple and intuitive GUI.
- Allows users to browse and select:
  - A text file containing the list of filenames to delete.
  - A folder containing the files to be deleted.
- Deletes files listed in the text file from the specified folder.
- Displays success or error messages after the deletion process is completed.

#### How it works:
1. The user selects a text file where each line represents the name of a file to be deleted.
2. The user selects the folder containing these files.
3. The script attempts to delete each file listed, reporting success or failure for each file.
4. A message box provides feedback at the end of the process.

This script is useful for bulk deleting files based on predefined lists, helping users avoid manually removing files.

### 2. `Random_image_selector.py`
This Python script, integrated with OMERO (an open-source platform for managing, visualizing, and analyzing microscopy images), is designed to randomly select images from datasets and move them to a specified output dataset. It groups images based on common filename prefixes and ensures a certain number of images per prefix are selected for transfer.

#### Features:
- Uses the **OMERO** framework for managing image datasets.
- Randomly selects a specified number of images from each prefix group within a dataset.
- Moves the selected images to a new dataset.
- Groups images by common prefixes (e.g., parts of filenames before underscores or hyphens).
- Provides a command-line interface for specifying input and output datasets as well as the number of images to select per prefix.

#### How it works:
1. **Dataset and Image Selection**: 
   - The user provides the IDs of input datasets and the output dataset.
   - The user also specifies how many images to select per prefix.
2. **Prefix Grouping**:
   - Images are grouped based on common filename prefixes, identified by shared characters before underscores or hyphens.
3. **Random Image Selection**:
   - For each prefix group, a random subset of images (up to the specified number) is selected.
4. **Image Transfer**:
   - Selected images are moved to the output dataset via OMERO's API.
5. **Output**:
   - The script provides feedback on the moved images or any encountered errors.

#### Use Cases:
- This script is useful in scenarios where users need to analyze or work with a random subset of images from large datasets, especially when images are organized by naming conventions.
- Suitable for scientific workflows involving microscopy or other image-heavy research.

#### Script Parameters:
- `Dataset_IDs`: A list of dataset IDs to process.
- `Num_Images_Per_Prefix`: The number of images to randomly select from each prefix group.
- `Output_Dataset_ID`: The ID of the output dataset where selected images will be moved.

#### Example Workflow:
1. The user specifies multiple datasets from which images will be randomly selected.
2. The script groups images by their filename prefixes (e.g., `sample_A_1.jpg` and `sample_A_2.jpg` share the prefix `sample_A_`).
3. A random subset of images from each prefix group is moved to a new dataset for further analysis or processing.

### 3. `folder_comparator_v2.py`
This Python script provides a GUI-based tool for comparing the contents of two folders. It identifies common files, as well as files that are unique to each folder, and offers the option to rename unique files by adding a prefix.

#### Features:
- Uses `Tkinter` to create a simple GUI for folder selection and comparison.
- Compares two folders and identifies:
  - Files common to both folders.
  - Files unique to each folder.
- Generates three output files:
  - `common_files.txt` – lists files that exist in both folders.
  - `unique_to_folder1.txt` – lists files only found in the first folder.
  - `unique_to_folder2.txt` – lists files only found in the second folder.
- Optionally prefixes files unique to each folder with `"un_"` to help differentiate them.

#### How it works:
1. The user selects two folders for comparison.
2. The script compares the contents of the two folders:
   - Files that exist in both are considered common.
   - Files that exist in only one folder are considered unique.
3. The comparison results are saved into text files (`.txt`).
4. If the user selects the option to prefix uncommon files, files unique to each folder are renamed with the `"un_"` prefix.
5. The results are displayed in the GUI, showing the names of the generated text files and the status of the optional prefixing.

This script is ideal for comparing folder contents in scenarios like backup verification, data synchronization, or content audits.

### 4. `napari_sort_v3.py`
The `napari_sort_v3.py` script is designed to help users visually inspect and sort image datasets. Using **Napari** for visualization and **Tkinter** for folder selection, the script allows for interactive browsing and manual sorting of images, masks, and chromocenters images. Files can be moved to specified destination folders, with the process logged for reference.

---

#### Key Components & Workflow

1. **Folder Selection via Tkinter GUI**:
    - Users can select directories for images, masks, and chromosome data, as well as a destination folder where files will be moved.

2. **Image & Layer Management with Napari**:
    - **Napari** opens a viewer displaying images and labels.
    - Users can navigate through images using keyboard shortcuts:
        - `n`: Next image
        - `b`: Previous image
        - `p`: Print current image index and name
        - `d`: Move current image to the specified destination folder
