import os
import tkinter as tk
from tkinter import filedialog

def compare_folders(folder1, folder2):
    # Get the list of files in each folder
    files1 = set(os.listdir(folder1))
    files2 = set(os.listdir(folder2))
    
    # Find common files
    common_files = files1.intersection(files2)
    
    # Find files unique to each folder
    unique_to_folder1 = files1 - files2
    unique_to_folder2 = files2 - files1
    
    return list(common_files), list(unique_to_folder1), list(unique_to_folder2)

def write_list_to_file(file_path, file_list):
    with open(file_path, 'w') as f:
        for file in file_list:
            f.write(file + '\n')

def prefix_uncommon_files(folder, unique_files):
    for file_name in unique_files:
        original_path = os.path.join(folder, file_name)
        new_path = os.path.join(folder, "un_" + file_name)
        os.rename(original_path, new_path)

def compare_folders_gui():
    def browse_folder1():
        folder_path = filedialog.askdirectory()
        folder1_entry.delete(0, tk.END)
        folder1_entry.insert(tk.END, folder_path)
    
    def browse_folder2():
        folder_path = filedialog.askdirectory()
        folder2_entry.delete(0, tk.END)
        folder2_entry.insert(tk.END, folder_path)
    
    def compare_and_write():
        folder1 = folder1_entry.get()
        folder2 = folder2_entry.get()
        
        common_files, unique_to_folder1, unique_to_folder2 = compare_folders(folder1, folder2)
        
        common_files_file = 'common_files.txt'
        unique_to_folder1_file = 'unique_to_folder1.txt'
        unique_to_folder2_file = 'unique_to_folder2.txt'
        
        write_list_to_file(common_files_file, common_files)
        write_list_to_file(unique_to_folder1_file, unique_to_folder1)
        write_list_to_file(unique_to_folder2_file, unique_to_folder2)
        
        if prefix_uncommon_files_var.get() == 1:
            prefix_uncommon_files(folder1, unique_to_folder1)
            prefix_uncommon_files(folder2, unique_to_folder2)
            result_label.config(text="Lists have been written and uncommon files have been prefixed.\n- Common Files: {}\n- Files Unique to {}: {}\n- Files Unique to {}: {}".format(common_files_file, folder1, unique_to_folder1_file, folder2, unique_to_folder2_file))
        else:
            result_label.config(text="Lists have been written to:\n- Common Files: {}\n- Files Unique to {}: {}\n- Files Unique to {}: {}".format(common_files_file, folder1, unique_to_folder1_file, folder2, unique_to_folder2_file))
    
    # Create main window
    root = tk.Tk()
    root.title("Folder Comparison Tool")
    
    # Folder 1 Frame
    folder1_frame = tk.Frame(root)
    folder1_frame.pack(fill=tk.X, padx=10, pady=5)
    
    folder1_label = tk.Label(folder1_frame, text="Folder 1:")
    folder1_label.pack(side=tk.LEFT)
    
    folder1_entry = tk.Entry(folder1_frame, width=50)
    folder1_entry.pack(side=tk.LEFT, padx=(5, 0), expand=True, fill=tk.X)
    
    browse1_button = tk.Button(folder1_frame, text="Browse", command=browse_folder1)
    browse1_button.pack(side=tk.LEFT, padx=(5, 0))
    
    # Folder 2 Frame
    folder2_frame = tk.Frame(root)
    folder2_frame.pack(fill=tk.X, padx=10, pady=5)
    
    folder2_label = tk.Label(folder2_frame, text="Folder 2:")
    folder2_label.pack(side=tk.LEFT)
    
    folder2_entry = tk.Entry(folder2_frame, width=50)
    folder2_entry.pack(side=tk.LEFT, padx=(5, 0), expand=True, fill=tk.X)
    
    browse2_button = tk.Button(folder2_frame, text="Browse", command=browse_folder2)
    browse2_button.pack(side=tk.LEFT, padx=(5, 0))
    
    # Checkbutton for prefixing uncommon files
    prefix_uncommon_files_var = tk.IntVar()
    prefix_uncommon_files_checkbutton = tk.Checkbutton(root, text="Prefix uncommon files?", variable=prefix_uncommon_files_var)
    prefix_uncommon_files_checkbutton.pack(padx=10, pady=5)
    
    # Compare Button
    compare_button = tk.Button(root, text="Compare Folders", command=compare_and_write)
    compare_button.pack(padx=10, pady=10)
    
    # Result Label
    result_label = tk.Label(root, wraplength=400)
    result_label.pack(padx=10, pady=(0, 10))
    
    root.mainloop()

if __name__ == "__main__":
    compare_folders_gui()
