# Script which download from AlphaFold the WD Repeat structure from filtered rawdata sequence file ~/common/data/0_raw/WD_sequence_filtered/WD_sequence_final_filtered.fa
# by WITTENMEYER Guillaume, MOSER Mathilda, KESHAVARZ-NAJAFI Mohsen

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
        Function which download structure from AlphaFold containing from an input fasta file using the protein ID of each sequence and save the structures in a specific folder
            fpath = folder path of the input fasta file (str)
            fname = fasta file name (str)
            output_path = outpu folder path to save the AF structure
    """
    for sequence in SeqIO.parse(fpath / fname, 'fasta'):
        # Store the protein ID of the sequence containing in the head  of the sequence
        protid=sequence.id.split('|')[1]
        output_fname= protid+'.pdb'
        with open(output_fpath / output_fname,'wb') as f:
            f.write(requests.get(f'https://alphafold.ebi.ac.uk/files/AF-{protid}-F1-model_v4.pdb').content)

# Executing process:
download_pdb_from_af(rawdata_folder, 'WD_sequence_final_filtered.fa', rawpdb_folder)