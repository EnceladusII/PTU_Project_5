# Script to generate figure of the RMSD in function of number of atoms take in cont during superimposition of ~/common/scripts/superimpose.py
# by WITTENMEYER Guillaume, MOSER Mathilda, KESHAVARZ-NAJAFI Mohsen

import os
from pathlib import Path
import matplotlib.pyplot as plt
import math

# Path utils:
commonpath = Path(__file__).parent.parent
txtpath= commonpath / 'data' / '1_intermediate' / 'pdb_cut_per_blade'

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

def graphs(fpath=str, fname=str):
    """
        Function to show the graphic of the log10(RMSD) in function of the number of atoms take in count during the superimpostion 
        containing  in the 'RMSD.txt' generated file of super_structure()
            fname = folder path of the 'RMSD.txt' file (str)
    """
    # To stock the number of atom take in count and the rmsd for each superimposition in the file
    nbr_at=[]
    log_rmsd=[]
    output_fname=f'Graphs_RMSD_blade{fname[-6:-4]}.png'
    # Found and store the number of atoms take in count and the RMSD
    with open(fpath / fname, 'r') as f:
       lines=f.readlines()
       for i in range(0, len(lines), 3):
            nbr_at.append(int(lines[i+1]))
            log_rmsd.append(math.log10(float(lines[i+2])))
    
    # Show and save the plot
    plt.figure(figsize=(10, 6))
    plt.scatter(log_rmsd, nbr_at, color='blue', marker='o')
    plt.ylabel("Nombre d'atomes pris en comptes")
    plt.xlabel("RMSD Log10(Å)")
    plt.title(f"Nombre d'atomes pris en compte en fonction du Log10(RMSD) pour {fname}")
    plt.grid(True)
    plt.savefig(fpath / output_fname)
    plt.show()

# Executing process:
for f in find_rmsd_txtfiles(txtpath):
    graphs(txtpath, f)