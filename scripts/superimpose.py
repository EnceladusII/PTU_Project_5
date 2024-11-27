# Script to superimpose structures download with ~/common/scripts/alphafold.py and filter per blade with ~/common/scripts/filter.py
# by WITTENMEYER Guillaume, MOSER Mathilda, KESHAVARZ-NAJAFI Mohsen

import os
from pathlib import Path
import pymol
from pymol import cmd


# Path utils:
commonpath = Path(__file__).parent.parent
pdbpath= commonpath / 'data' / '1_intermediate' / 'pdb_cut_per_blade'
# For PyMol compatibility (necessary to change your path):
pdbbladepath='/home/encelade/Documents/Master/M2_BBS/S3/PTU/common/data/1_intermediate/pdb_cut_per_blade'

def find_pdbblade_files(fpath=str, bladenbr=int):
    """
        Function which return a list of all pdb files names present in a specific folder for a specific number of the blade of the WD Repeat
            fpath = folder path of the pdb files (str)
            bladenbr = blade number of the wanted files (int)
    """
    pdb_list = []
    for fname in os.listdir(fpath):
        # Verify if fname is a file and if he end with our correct blade number
        if os.path.isfile(os.path.join(fpath, fname)) and fname.endswith(f'blade{bladenbr}.pdb'):
            pdb_list.append(fname)
    return pdb_list

def load_structure(pdbpath=str, fname=str):
    """
        Function for load structure in PyMol
            pdbpath = path of the pdb of interest (str)
            fname = name of the pdb of interest (str)
    """
    cmd.load(str(pdbpath)+f'/{fname}', fname[:-4])

def super_structure(pdbpath=str, pdblist=list, sfx=str):
    """
        Function to superimpose a liste of structure by using the first structure of the list like the reference structure for superimposition
            pdbpath = path  of all the pdb files (str)
            pdblist = list of the name of the pdbs to superimpose with the reference (list)
            sfx = suffix for generated files (int)

    """
    # Launch PyMol with the GUI
    pymol.finish_launching(['pymol', '-q']) 

    # Create a file to store the rmsd and the number of atoms take in account for each superimposition
    with open(pdbpath + f'/RMSD_{sfx}.txt', 'w') as f:
                f.write(f"")

    # Create a file to store the pdb which are not predicted by AlphaFold 
    with open(pdbpath + f'/Error_{sfx}.txt', 'w') as f:
                f.write(f"")
    
    # Reference is defined like the first pdb in the list
    ref=pdblist[0][:-4]
    load_structure(pdbpath, pdblist[0])

    for pdb in pdblist[1:]:
        name=pdb[:-4]
        load_structure(pdbpath, pdb)
        # If pdb file containing no error
        try:
            cmd.super(name, ref)
            rmsd = cmd.super(name, ref)[0]
            nbr_at = cmd.super(name, ref)[1]
            with open(pdbpath + f'/RMSD_{sfx}.txt', 'a') as f:
                f.write(f">Superposition de {name} sur {ref}:\n{nbr_at}\n{rmsd}\n")
        #If pdb file contain an unpredicted protein by AlphaFold
        except Exception as e:
            with open(pdbpath + f'/Error_{sfx}.txt', 'a') as f:
                f.write(f">Erreur lors de la superposition de:\n{name}\n")

# Executing process:    
bladenbr=int(input('Blade number = '))
super_structure(pdbbladepath, find_pdbblade_files(pdbbladepath, bladenbr), str(bladenbr))
