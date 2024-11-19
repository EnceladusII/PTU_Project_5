import os
from pathlib import Path
from Bio import SeqIO
import requests

# Path utils:
commonpath = Path(__file__).parent.parent
rawdata_folder = commonpath / 'data' / '0_raw' / 'sequences_fasta' /'WD_sequence_filtered'
rawpdb_folder = commonpath / 'data' / '0_raw' / 'pdb'

def download_pdb_from_af(fpath=str, fname=str, output_fpath=str):
    """
    
    """
    for sequence in SeqIO.parse(fpath / fname, 'fasta'):
        protid=sequence.id.split('|')[1]
        output_fname= protid+'.pdb'
        with open(output_fpath / output_fname,'wb') as f:
            f.write(requests.get(f'https://alphafold.ebi.ac.uk/files/AF-{protid}-F1-model_v4.pdb').content)

download_pdb_from_af(rawdata_folder, 'WD_sequence_final_filtered.fa', rawpdb_folder)