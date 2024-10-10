#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
------------------------------------------------------------------------------
This script moves randomly selected images from the specified datasets to another dataset.
"""
import omero
import omero.scripts as scripts
from omero.gateway import BlitzGateway
from omero.rtypes import rstring, rlong, unwrap
import omero.model
import random


def trouver_prefixes_communs(liste_noms):
    prefixes_communs = []
    prefixes_occurrences = {}
    noms_par_prefixe = {}

    if not liste_noms:
        return prefixes_communs, prefixes_occurrences, noms_par_prefixe

    liste_noms_triee = sorted(liste_noms)

    premier_nom = liste_noms_triee[0]
    deuxieme_nom = liste_noms_triee[1]

    # Find le plus long préfixe commun entre les deux premiers noms
    i = 0
    while i < len(premier_nom) and i < len(deuxieme_nom) and premier_nom[i] == deuxieme_nom[i]:
        i += 1
    prefixe_commun = premier_nom[:i]

    # Vérifier si le préfixe contient un underscore ou un tiret avant le dernier élément
    last_underscore_index = prefixe_commun.rfind('_')
    last_hyphen_index = prefixe_commun.rfind('-')
    if last_underscore_index > last_hyphen_index:
        truncate_index = last_underscore_index
    else:
        truncate_index = last_hyphen_index

    if truncate_index != -1:
        prefixe_commun = prefixe_commun[:truncate_index + 1]

    # Ajouter le premier préfixe commun à la liste et initialiser son compteur à 0
    prefixes_communs.append(prefixe_commun)
    prefixes_occurrences[prefixe_commun] = 0

    # Parcourir les noms restants pour trouver les préfixes communs
    for j in range(1, len(liste_noms_triee) - 1):
        nom_courant = liste_noms_triee[j]
        nom_suivant = liste_noms_triee[j + 1]

        i = 0
        # Trouver le plus long préfixe commun entre le nom courant et le nom suivant
        while i < len(nom_courant) and i < len(nom_suivant) and nom_courant[i] == nom_suivant[i]:
            i += 1
        # Extraire le préfixe commun trouvé
        prefixe_commun = nom_courant[:i]

        # Vérifier si le préfixe contient un underscore ou un tiret avant le dernier élément
        last_underscore_index = prefixe_commun.rfind('_')
        last_hyphen_index = prefixe_commun.rfind('-')
        if last_underscore_index > last_hyphen_index:
            truncate_index = last_underscore_index
        else:
            truncate_index = last_hyphen_index

        if truncate_index != -1:
            prefixe_commun = prefixe_commun[:truncate_index + 1]

        # Vérifier si le préfixe commun n'est pas déjà inclus dans la liste des préfixes communs
        if all(not p.startswith(prefixe_commun) for p in prefixes_communs):
            prefixes_communs.append(prefixe_commun)
            prefixes_occurrences[prefixe_commun] = 0

    # parcourir à nouveau la liste pour compter les occurrences de chaque préfixe commun
    for nom in liste_noms:
        for prefixe in prefixes_communs:
            if nom.startswith(prefixe):
                prefixes_occurrences[prefixe] += 1
                if prefixe not in noms_par_prefixe:
                    noms_par_prefixe[prefixe] = []
                noms_par_prefixe[prefixe].append(nom)
                break  

    # Print all prefixes found
    print("Prefixes found:", prefixes_communs)

    return prefixes_communs, prefixes_occurrences, noms_par_prefixe


def move_random_images_to_new_dataset(conn, dataset_id, output_dataset_id, num_images_per_prefix):
    """
    Selects random images from the dataset and copy them to the output dataset.
    """
    update_service = conn.getUpdateService()
    message = ""

    try:
        # Get the dataset
        dataset = conn.getObject("Dataset", dataset_id)
        if dataset is None:
            message += f"Dataset ID {dataset_id} not found.\n"
            return message

        # Get all images in the dataset
        images = list(dataset.listChildren())
        if not images:
            message += f"No images found in dataset ID {dataset_id}.\n"
            return message

        # Retrieve image names
        image_names = [image.getName() for image in images]

        # Group images by common prefixes and select images per prefix
        _, _, noms_par_prefixe = trouver_prefixes_communs(image_names)

        # Move selected images to the output dataset
        for prefix, noms in noms_par_prefixe.items():
            selected_images = random.sample(noms, min(num_images_per_prefix, len(noms)))
            for image_name in selected_images:
                image = next(image for image in images if image.getName() == image_name)
                image_obj = conn.getObject("Image", image.getId())
                if image_obj is not None:
                    link = omero.model.DatasetImageLinkI()
                    link.setParent(omero.model.DatasetI(output_dataset_id, False))
                    link.setChild(image_obj._obj)
                    update_service.saveObject(link)
                    print(f"Moved image ID {image.getId()} to dataset ID {output_dataset_id}")
                else:
                    message += f"Image ID {image.getId()} not found.\n"

    except Exception as exc:
        message += f"Error while moving images: {str(exc)}"

    return message


def run_script():
    """
    The main entry point of the script, as called by the client via the
    scripting service, passing the required parameters.
    """
    client = scripts.client(
        'Random_Image_Selector',
        """
        Randomly select a specified number of images from each genotype in a dataset and copy them to a new dataset. Multiple datasets can be processed simultaneously by separating their IDs with commas.
        """,

        scripts.String(
            "Dataset_IDs", optional=False, grouping="2",
            description="List of Dataset IDs to process."),

        scripts.Long(
            "Num_Images_Per_Prefix", optional=False, grouping="2",
            description="Number of images to randomly select per prefix."),


        scripts.String(
            "Output_Dataset_ID", optional=False, grouping="2",
            description="Output Dataset ID where images will be copied."),

        version="2.0",
        authors=["Sami Safarbati", "GReD"],
        institutions=["UCA"],
        contact="sami.safarbati@uca.fr",
    )

    try:
        parameter_map = client.getInputs(unwrap=True)
        dataset_ids_str = parameter_map["Dataset_IDs"]
        output_dataset_id = parameter_map["Output_Dataset_ID"]
        num_images_per_prefix = int(parameter_map["Num_Images_Per_Prefix"])

        # Split the input string by commas and convert to a list of integers
        dataset_ids = [int(id.strip()) for id in dataset_ids_str.split(',') if id.strip().isdigit()]

        # Create a wrapper so we can use the Blitz Gateway.
        conn = BlitzGateway(client_obj=client)

        for dataset_id in dataset_ids:
            message = move_random_images_to_new_dataset(conn, dataset_id, output_dataset_id, num_images_per_prefix)

            client.setOutput("Message", rstring(message))

    finally:
        client.closeSession()


if __name__ == "__main__":
    run_script()
