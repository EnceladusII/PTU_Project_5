import os
from pathlib import Path
from pymol import cmd

# Path utils:
commonpath = Path(__file__).parent.parent
pdbbladepath= commonpath / 'data' / '1_intermediate' / 'pdb_cut_per_blade'
pdbbladepath='/home/encelade/Documents/Master/M2_BBS/S3/PTU/common/data/1_intermediate/pdb_cut_per_blade'

def find_pdbblade_files(fpath=str, bladenbr=int):
    """
        Function for append in a  list all pdb files names present in a folder
    """
    pdb_list = []
    for fname in os.listdir(fpath):
        if os.path.isfile(os.path.join(fpath, fname)) and fname.endswith(f'blade{bladenbr}.pdb'):
            pdb_list.append(fname)
    return pdb_list

def load_structure(pdbpath=str, fname=str):
    """
    
    """
    cmd.load(str(pdbpath)+f'/{fname}', fname[:-4])

def super_structure(pdbpath=str, pdblist=list):
    """
    
    """
    with open(pdbpath + '/RMSD.txt', 'w') as f:
                f.write(f"")

    with open(pdbpath + '/Error_pdb.txt', 'w') as f:
                f.write(f"")
    
    ref=pdblist[0][:-4]
    load_structure(pdbpath, pdblist[0])

    for pdb in pdblist[1:]:
        name=pdb[:-4]
        load_structure(pdbpath, pdb)
        try:
            cmd.super(name, ref)
            rmsd = cmd.super(name, ref)[0]
            print(rmsd)
            with open(pdbpath + '/RMSD.txt', 'a') as f:
                f.write(f">Superposition de {name} sur {ref}:\n{rmsd}\n")
        except Exception as e:
            with open(pdbpath + '/Error_pdb.txt', 'a') as f:
                f.write(f">Erreur lors de la superposition de:\n{name}\n")

l=find_pdbblade_files(pdbbladepath, 6)
super_structure(pdbbladepath, l)