import os
import tkinter as tk
from tkinter import filedialog, messagebox

def delete_files_from_folder(file_list_path, folder_path):
    try:
        with open(file_list_path, 'r') as file:
            files_to_delete = file.read().splitlines()
        
        for filename in files_to_delete:
            file_path = os.path.join(folder_path, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            else:
                print(f"File not found: {file_path}")
        
        messagebox.showinfo("Success", "Deletion process completed.")
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def select_file_list():
    file_path = filedialog.askopenfilename(title="Select the text file containing filenames")
    file_list_entry.delete(0, tk.END)
    file_list_entry.insert(0, file_path)

def select_folder():
    folder_path = filedialog.askdirectory(title="Select the folder containing files to delete")
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def start_deletion():
    file_list_path = file_list_entry.get()
    folder_path = folder_entry.get()
    if not file_list_path or not folder_path:
        messagebox.showwarning("Input Error", "Please select both the file list and the folder.")
        return
    delete_files_from_folder(file_list_path, folder_path)

# Set up the GUI
root = tk.Tk()
root.title("File Deletion Tool")

tk.Label(root, text="Select the text file containing filenames:").grid(row=0, column=0, padx=10, pady=10)
file_list_entry = tk.Entry(root, width=50)
file_list_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_file_list).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Select the folder containing files to delete:").grid(row=1, column=0, padx=10, pady=10)
folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_folder).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Start Deletion", command=start_deletion).grid(row=2, columnspan=3, pady=20)

root.mainloop()
