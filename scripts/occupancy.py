# Script to filter the each alignment using the occupancy for each residues using a threshold to generate understandable weblogos
# by WITTENMEYER Guillaume, MOSER Mathilda, KESHAVARZ-NAJAFI Mohsen

from Bio import AlignIO
import os
from pathlib import Path
from Bio import SeqIO
from collections import Counter


# Path utils:
commonpath = Path(__file__).parent.parent / 'data' / '1_intermediate' / 'MAFFT_alignment'
mafftdata_folder = commonpath
mafftdata_folder_fil = commonpath / 'WD_sequence_filtered'
mafftdata_folder_10_fil = commonpath / 'WD_sequence_10_filtered'
mafftdata_folder_20_fil = commonpath / 'WD_sequence_20_filtered'


def filter_alignment_by_occupancy(input_fasta=str, output_fasta=str, threshold=float):
    """
        Function which filter and write a new alignment by calculating the occupancy of each residue and only store residue with an occupancy over a threshold
            input_fasta = fasta file alignment we want to filter (string)
            output_fasta = the output file name of the filtered input_fasta alignment file (string)
            threshold = treshold for the occupancy (0 < float < 1)
    """
    # Using BioPyhton to read the alignment file in input
    alignment = AlignIO.read(input_fasta, "fasta")
    num_sequences = len(alignment)
    # Calcul de l'occupancy pour chaque position dans l'alignement si la colonne n'est pas vide ( = gap)
    valid_columns = []
    for i in range(alignment.get_alignment_length()):
        column = alignment[:, i]
        num_non_gaps = sum(1 for char in column if char != '-')
        occupancy = num_non_gaps / num_sequences
        if occupancy >= threshold:
            valid_columns.append(i)
    # Store the filtered sequence for each position using the threshold
    filtered_alignment = []
    for sequence in alignment:
        filtered_seq = "".join(sequence.seq[i] for i in valid_columns)
        filtered_alignment.append(f">{sequence.id}\n{filtered_seq}")
    #Write the new alignment fasta file containing only the position with an occupancy better than the threshold
    with open(output_fasta, "w") as output:
        output.write("\n".join(filtered_alignment) + "\n")

def find_alignment_files(fpath=str):
    """
        Function which append in a list all alignment files names present in a folder
            fpath = folder path to search alignment files (string)
    """
    # Create list for append each alignment file found in fpath
    ali_list = []

    for fname in os.listdir(fpath):
        # Verify if each entity in the forler are a file, and if it's the case verify if the file name end with '.fasta'
        if os.path.isfile(os.path.join(fpath, fname)) and fname.endswith('.fasta'):
            ali_list.append(fname)
    return ali_list

def gen_weblogo_fil(fpathlist=list, threshold=float):
    """
        Generate an idea of the alignment file generate by filter_alignment_by_occupancy()
            fpathlist = folder path which contain the filtered alignment fasta files (string)
            threshold = treshold for the occupancy (0 < float < 1)
    """
    for path in fpathlist:
        ali_list=find_alignment_files(path)
        for ali in ali_list:
            outfname=ali[:-6]+f'_fil_occ_{int(threshold*100)}%.fasta'
            filter_alignment_by_occupancy(path / ali, path / 'occupancy' / outfname, threshold)

# Executing process :

# Pathlist  for the alignment files to filter with the occupancy
pathlist=[mafftdata_folder, mafftdata_folder_fil, mafftdata_folder_10_fil, mafftdata_folder_20_fil]

# Create a folder to store the results if this folder doesnt exist
for path in pathlist:
    if os.path.exists(path / 'occupancy'):
        pass
    else:
        os.mkdir('occupancy')
    

# Generate the filtered alignment
threshold_list=[0.6, 0.7, 0.8]
for threshold in threshold_list:
    gen_weblogo_fil(pathlist, threshold)