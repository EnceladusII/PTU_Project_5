# Script to superimpose structures download with ~/common/scripts/alphafold.py and filter per blade with ~/common/scripts/filter.py
# by WITTENMEYER Guillaume, MOSER Mathilda, KESHAVARZ-NAJAFI Mohsen

import os
from pathlib import Path
import pymol
from pymol import cmd


# Path utils:
commonpath = Path(__file__).parent.parent
pdbpath= commonpath / 'data' / '1_intermediate' / 'pdb_cut'
pdbsuperpath=commonpath / 'data' / '1_intermediate'

def find_pdbblade_files(fpath=str):
    """
        Function which return a list of all pdb files names present in a specific folder for a specific number of the blade of the WD Repeat
            fpath = folder path of the pdb files (str)
    """
    pdb_list = []
    for fname in os.listdir(fpath):
        # Verify if fname is a file and if he end with our correct blade number
        if os.path.isfile(os.path.join(fpath, fname)) and fname.endswith(f'.pdb'):
            pdb_list.append(fname)
    return pdb_list

def load_structure(pdbpath=str, fname=str):
    """
        Function for load structure in PyMol
            pdbpath = path of the pdb of interest (str)
            fname = name of the pdb of interest (str)
    """
    cmd.load(str(pdbpath)+f'/{fname}', fname[:-4])

def super_structure(pdbpath=str, pdblist=list):
    """
        Function to superimpose a liste of structure by using the first structure of the list like the reference structure for superimposition
            pdbpath = path  of all the pdb files (str)
            pdblist = list of the name of the pdbs to superimpose with the reference (list)
            sfx = suffix for generated files (int)

    """
    # For PyMol compatibility :
    pdbpath=str(pdbpath)

    # Reference is defined like the first pdb in the list
    ref=''
    rmsd_ref=0

    for i in range(len(pdblist)):
        rmsd=0
        supposed_ref = pdblist[i]
        print(supposed_ref)
        load_structure(pdbpath, pdblist[i])

        pop=pdblist.pop(i)

        for pdb in pop:
            name=pdb[:-4]
            load_structure(pdbpath, pdb)
            # If pdb file containing no error
            try:
                rmsd += cmd.super(name, supposed_ref)[0]
            except Exception as e:
                pass

        if rmsd < rmsd_ref:
            ref=supposed_ref
        print(rmsd_ref)

    return ref, rmsd


# Executing process:    
bladenbr=str(input('Blade number = '))
super_structure(pdbpath / f'pdb_cut_per_blade_{bladenbr}', find_pdbblade_files(pdbpath / f'pdb_cut_per_blade_{bladenbr}'))
