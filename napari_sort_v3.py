import os
import shutil
import napari
from skimage.io import imread
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox

def abs_path(root, listdir_):
    listdir = listdir_.copy()
    for i in range(len(listdir)):
        listdir[i] = os.path.join(root, listdir[i])
    return listdir

def abs_listdir(path):
    return abs_path(path, os.listdir(path))

# Napari utils

load_fct = lambda v, idx, spacing: imread(list_abs[v][idx])
load_fct_lab = lambda v, idx, spacing: imread(list_abs[v][idx])

def replace_layers(viewer):
    global idx, list_abs, name_dict, spacing
    for k, v in name_dict.items():
        if k == 'image':
            viewer.layers[k].data = load_fct(v, idx, spacing)
        else:
            viewer.layers[k].data = load_fct_lab(v, idx, spacing)
    return viewer

def start_napari():
    global idx, list_abs, name_dict, spacing

    list_abs = []
    if masks_folder.get():
        list_abs.append(abs_listdir(masks_folder.get()))
    if chromos_folder.get():
        list_abs.append(abs_listdir(chromos_folder.get()))
    if images_folder.get():
        list_abs.append(abs_listdir(images_folder.get()))

    idx = 0
    list_names = []
    if masks_folder.get():
        list_names.append("mask")
    if chromos_folder.get():
        list_names.append("chromos")
    name_dict = dict(zip(["image"] + list_names, [-1] + [i for i in range(len(list_names))]))
    spacing = [1, 1, 1]

    viewer = napari.Viewer()

    for k, v in name_dict.items():
        if k == 'image':
            viewer.add_image(load_fct(v, idx, spacing), name=k)
        else:
            viewer.add_labels(load_fct_lab(v, idx, spacing), name=k)

    raw_file_log = []

    @viewer.bind_key('n', overwrite=True)
    def napari_print_next(viewer):
        global idx, list_abs
        if idx < len(list_abs[0]) - 1:
            idx += 1
            viewer = replace_layers(viewer)

    @viewer.bind_key('b', overwrite=True)
    def napari_print_previous(viewer):
        global idx, list_abs
        if idx > 0:
            idx -= 1
            viewer = replace_layers(viewer)

    @viewer.bind_key('p', overwrite=True)
    def napari_print_properties(viewer):
        global idx, list_abs
        print("current idx: ", idx)
        print("image name: ", list_abs[0][idx].split('/')[-1])

    @viewer.bind_key('d', overwrite=True)
    def napari_move_img_msk(viewer):
        global idx, list_abs
        print("current idx: ", idx)
        for j, folder_name in enumerate((["mask"] if masks_folder.get() else []) + (["chromos"] if chromos_folder.get() else []) + ["raw"]):
            print("move: ", list_abs[j][idx])
            if destination_folder.get():
                destination_folder_path = os.path.join(destination_folder.get(), folder_name)
                if not os.path.exists(destination_folder_path):
                    os.makedirs(destination_folder_path)
                if os.path.isdir(destination_folder_path):
                    shutil.move(list_abs[j][idx], destination_folder_path)
                    print("Image moved successfully to", folder_name)
                    if folder_name == "raw":
                        raw_file_log.append(os.path.join(destination_folder_path, os.path.basename(list_abs[j][idx])))
                else:
                    print("Destination folder", folder_name, "does not exist.")
            else:
                print("No destination folder specified.")
            list_abs[j].remove(list_abs[j][idx])

    napari.run()

    if destination_folder.get() and raw_file_log:
        output_log_path = os.path.join(destination_folder.get(), 'moved_files.txt')
        with open(output_log_path, 'w') as f:
            for raw_file in raw_file_log:
                f.write(os.path.basename(raw_file) + '\n')

def browse_folder(entry):
    folder_selected = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, folder_selected)

# Creating the Tkinter GUI
root = tk.Tk()
root.title("Napari Image Sorting Tool")

tk.Label(root, text="Images Folder:").grid(row=0, column=0, sticky=tk.W)
images_folder = tk.Entry(root, width=50)
images_folder.grid(row=0, column=1)
tk.Button(root, text="Browse", command=lambda: browse_folder(images_folder)).grid(row=0, column=2)

tk.Label(root, text="Masks Folder:").grid(row=1, column=0, sticky=tk.W)
masks_folder = tk.Entry(root, width=50)
masks_folder.grid(row=1, column=1)
tk.Button(root, text="Browse", command=lambda: browse_folder(masks_folder)).grid(row=1, column=2)

tk.Label(root, text="Chromos Folder:").grid(row=2, column=0, sticky=tk.W)
chromos_folder = tk.Entry(root, width=50)
chromos_folder.grid(row=2, column=1)
tk.Button(root, text="Browse", command=lambda: browse_folder(chromos_folder)).grid(row=2, column=2)

tk.Label(root, text="Destination Folder:").grid(row=3, column=0, sticky=tk.W)
destination_folder = tk.Entry(root, width=50)
destination_folder.grid(row=3, column=1)
tk.Button(root, text="Browse", command=lambda: browse_folder(destination_folder)).grid(row=3, column=2)

tk.Button(root, text="Start Napari", command=start_napari).grid(row=4, column=1)

root.mainloop()
