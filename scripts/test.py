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
# Path utils:
commonpath = Path(__file__).parent.parent
txtpath= commonpath / 'data' / '1_intermediate' / 'pdb_cut'

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



def super_structure2(pdbpath, pdblist):
    """
    Superimpose all structures in pdblist and find the best reference.
    """
    pdbpath = Path(pdbpath)
    best_ref = None
    at_ref=0
    lowest_rmsd = float('inf')

    # Iterate over each structure as the potential reference
    for ref in pdblist:
        # Load the reference structure
        cmd.reinitialize()  # Reset PyMOL to clear previous loads
        load_structure(pdbpath, ref)
        total_rmsd = 0
        at_tot=0
        success_count = 0

        for target in pdblist:
            if target == ref:
                continue  # Skip self-superposition
            
            load_structure(pdbpath, target)
            try:
                # Perform superimposition and sum RMSD values
                rmsd = cmd.super(target[:-4], ref[:-4])[0]
                at=rmsd = cmd.super(target[:-4], ref[:-4])[1]
                at_tot+=at
                total_rmsd += rmsd
                success_count += 1
            except Exception as e:
                print(f"Error superimposing {target} on {ref}: {e}")

        # Calculate the average RMSD
        avg_rmsd = total_rmsd / success_count if success_count > 0 else float('inf')
        avg_at = at_tot / success_count if success_count > 0 else 0

        # Update the best reference
        if avg_rmsd < lowest_rmsd:
            lowest_rmsd = avg_rmsd
            best_ref = ref
            at_ref=avg_at

    return best_ref, lowest_rmsd, at_ref

def find_rmsd_txtfiles(fpath=str):
    """
        Function which return a list of all RMSD files generated by superimpose.py present in a specific folder
            fpath = folder path of the file (str)
    """
    txt_list = []
    for fname in os.listdir(fpath):
        # Verify if fname is a file and if he is an RMSD file
        if os.path.isfile(os.path.join(fpath, fname)) and fname.startswith('RMSD_'):
            txt_list.append(fname)
    return txt_list

def avg(fpath=str, fname=str):
    """

    """
    # To stock the number of atom take in count and the rmsd for each superimposition in the file
    nbr_at=0
    rmsd=0
    count=0
    # Found and store the number of atoms take in count and the RMSD
    with open(fpath / fname, 'r') as f:
       lines=f.readlines()
       for i in range(0, len(lines), 3):
            count+=1
            nbr_at+=int(lines[i+1])
            rmsd+=float(lines[i+2])

    return nbr_at/count, rmsd/count, count
    
# Executing process:
for bladenbr in range(1,8):
    for f in find_rmsd_txtfiles(txtpath / f'pdb_cut_per_blade_{bladenbr}'):
        print(bladenbr, avg(txtpath / f'pdb_cut_per_blade_{bladenbr}', f))
        #graphs(txtpath / f'pdb_cut_per_blade_{bladenbr}', f)

# Executing process:    
#bladenbr=str(input('Blade number = '))
#print(super_structure2(pdbpath / f'pdb_cut_per_blade_{bladenbr}', find_pdbblade_files(pdbpath / f'pdb_cut_per_blade_{bladenbr}')))
