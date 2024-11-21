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
    
    """
    alignment = AlignIO.read(input_fasta, "fasta")
    num_sequences = len(alignment)
    
    valid_columns = []
    for i in range(alignment.get_alignment_length()):
        column = alignment[:, i]
        num_non_gaps = sum(1 for char in column if char != '-')
        occupancy = num_non_gaps / num_sequences
        if occupancy >= threshold:
            valid_columns.append(i)
    
    filtered_alignment = []
    for sequence in alignment:
        filtered_seq = "".join(sequence.seq[i] for i in valid_columns)
        filtered_alignment.append(f">{sequence.id}\n{filtered_seq}")
    
    with open(output_fasta, "w") as output:
        output.write("\n".join(filtered_alignment) + "\n")

def find_alignment_files(fpath=str):
    """
        Function for append in a  list all pdb files names present in a folder
    """
    ali_list = []
    for fname in os.listdir(fpath):
        if os.path.isfile(os.path.join(fpath, fname)) and fname.endswith('.fasta'):
            ali_list.append(fname)
    return ali_list

def gen_weblogo_fil(fpathlist=list, threshold=float):
    """
    
    """

    for path in fpathlist:
        ali_list=find_alignment_files(path)
        for ali in ali_list:
            outfname=ali[:-6]+f'_fil_occ_{threshold}.fasta'
            filter_alignment_by_occupancy(path / ali, path / 'occupancy' / outfname, threshold)

pathlist=[mafftdata_folder, mafftdata_folder_fil, mafftdata_folder_10_fil, mafftdata_folder_20_fil]

for path in pathlist:
    if os.path.exists(path / 'occupancy'):
        pass
    else:
        os.mkdir('occupancy')

gen_weblogo_fil(pathlist, 0.7)