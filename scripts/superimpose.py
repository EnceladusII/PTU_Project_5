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


def super_structure(pdbpath=str, pdblist=list, sfx=str):
    """
        Function to superimpose a liste of structure by using the best structure of the list like the reference structure for superimposition 
        by calculate the RMSD average of all superimposition for each reference in the list
            pdbpath = path  of all the pdb files (str)
            pdblist = list of the name of the pdbs to superimpose with the reference (list)
            sfx = suffix for generated files (int)

    """
    # Launch PyMol with the GUI (take lot of time)
    #pymol.finish_launching(['pymol', '-q'])

    # Define the initial variable to store the reference for the superimposition and the lowest RMSD average
    best_ref=None
    lowest_rmsd=float('inf')
    #highest_at=0

    # Calculate RMSD average for each ref structure in the list 
    for ref in pdblist:
        load_structure(pdbpath, ref)
        # Define initial parameters
        tot_rmsd=0
        #tot_at=0
        success_count=0
        # Superimpose all the structure with the actual reference
        for target in pdblist:
            # To skip the superimposition if the reference is the target too
            if target == ref:
                continue
            load_structure(pdbpath, target)
            try:
                rmsd = cmd.super(target[:-4], ref[:-4])[0]
                #at = cmd.super(target[:-4], ref[:-4])[1]
                tot_rmsd += rmsd
                #tot_at+=at
                success_count += 1
            except Exception as e:
                print(f"Error superimposing {target} on {ref}: {e}")
        # Compute the RMSD average
        avg_rmsd = tot_rmsd / success_count if success_count > 0 else float('inf')
        #avg_at = tot_at / success_count if success_count > 0 else 0
        # Compare the actual RMSD average with the actual lowest RMSD average
        if avg_rmsd < lowest_rmsd:
            # Redefine the lowest RMSD average and the best reference if the actual RMSD average is lower than the actual lowest RMSD average
            lowest_rmsd = avg_rmsd
            #highest_at=avg_at
            best_ref = ref

    print(f"Reference: {best_ref}, Avg RMSD: {lowest_rmsd}")

    # For PyMol compatibility :
    pdbpath=str(pdbpath)

    # Reinitialize PyMol
    cmd.reinitialize()

    # Create a file to store the rmsd and the number of atoms take in account for each superimposition
    with open(pdbpath + f'/RMSD_{sfx}.txt', 'w') as f:
                f.write(f"")

    # Create a file to store the pdb which are not predicted by AlphaFold 
    with open(pdbpath + f'/Error_{sfx}.txt', 'w') as f:
                f.write(f"")

    # Reference is defined like the first pdb in the list
    load_structure(pdbpath, best_ref)

    for pdb in pdblist:
        if pdb == ref:
            continue
        name=pdb[:-4]
        refname=best_ref[:-4]
        load_structure(pdbpath, pdb)
        # If pdb file containing no error
        try:
            cmd.super(name, refname)
            rmsd = cmd.super(name, refname)[0]
            nbr_at = cmd.super(name, refname)[1]
            with open(pdbpath + f'/RMSD_{sfx}.txt', 'a') as f:
                f.write(f">Superposition de {name} sur {refname}:\n{nbr_at}\n{rmsd}\n")
        #If pdb file contain an unpredicted protein by AlphaFold
        except Exception as e:
            with open(pdbpath + f'/Error_{sfx}.txt', 'a') as f:
                f.write(f">Erreur lors de la superposition de:\n{name}\n")

def save_superstructures(outpath=str, outputfolder=str):
    """
        Function to save the coordinates of the structure opened in a PyMol session in new pdb file for each structures in an output folder path 
        to use it in other molecular visualization software (Chimera, ChimeraX, DiscoveryStudio ...)
            outpath = folder path to save the outputfolders (string)
            outputfolder = folder path to save the pdb file created for each structure in the PyMol session (string)
    """
    # Create a list of all the structures in the session
    str_list=cmd.get_object_list()
    # Verify if exist and create the output folder 
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    outpath = outpath / outputfolder

    if not os.path.exists(outpath):
        os.mkdir(outpath)
    # Save pdb file for each structure in the str_list
    for structure in str_list:
        # For PyMol compatibility :
        fname=str(outpath / f"super_{structure}.pdb")
        cmd.save(fname, structure)


# Executing process:    
number=[1, 2, 3, 4, 5, 6, 7]

for bladenbr in number:
    super_structure(pdbpath / f'pdb_cut_per_blade_{bladenbr}', find_pdbblade_files(pdbpath / f'pdb_cut_per_blade_{bladenbr}'), bladenbr)
    save_superstructures(pdbsuperpath / 'pdb_superstructure',  f'pdb_superstructure_blade_{bladenbr}')
