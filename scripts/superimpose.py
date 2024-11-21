import os
from pathlib import Path
import Bio.PDB as bp

# Path utils:
commonpath = Path(__file__).parent.parent
pdbbladepath= commonpath / 'data' / '1_intermediate' / 'pdb_cut_per_blade'

def find_pdb_files(fpath=str):
    """
        Function for append in a  list all pdb files names present in a folder
    """
    pdb_list = []
    for fname in os.listdir(fpath):
        if os.path.isfile(os.path.join(fpath, fname)) and fname.endswith('.pdb'):
            pdb_list.append(fname)
    return pdb_list

def load_structure(fname=str):
    