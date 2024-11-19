import os
from pathlib import Path
from Bio import SeqIO


# Path utils:
commonpath = Path(__file__).parent.parent
rawdata_folder = commonpath / 'data' / '0_raw' / 'sequences_fasta'


def WD_repeat_class_filter (fpath=str, fname=str, wd_class=str, output_fpath=str):
    """
        Function to filter WD_sequence file for one class of repeat
    """
    output_fname=fname[:-3]+'_classfiltered_'+wd_class+'.fa'

    with open(output_fpath / output_fname,'w') as f:
        for sequence in SeqIO.parse(fpath / fname, 'fasta'):
            if sequence.description.endswith('-'+wd_class):
                f.write(sequence.format('fasta'))

def WD_repeat_filter (fpath=str, fname=str, wd_class=list, output_fpath=str):
    """
        Function to filter WD_sequence file for multiple classes of repeat
    """
    output_fname=fname[:-3]+'_filtered'+'.fa'

    with open(output_fpath / output_fname,'w') as f:
        for sequence in SeqIO.parse(fpath / fname, 'fasta'):
            if any('-'+cls in sequence.description for cls in wd_class):
                f.write(sequence.format('fasta'))


# Like we have analyse in our lab file, we only focus on the protein with 7 repeats to simplify the alignments:
rawdatas_list=['WD_sequence.fa', 'WD_sequence_10.fa', 'WD_sequence_20.fa']
wdclass_list=['1','2','3','4','5','6','7']

for fname in rawdatas_list:
    # Create folders to contain the different filtered fasta files for each raw datas
    filtered_foldername= rawdata_folder / f'{fname[:-2]}_filtered'
    os.mkdir(filtered_foldername)
    # Filter the raws datas for realign only the proteins with a maximum of 7 repeats
    WD_repeat_filter(rawdata_folder, fname, wdclass_list, filtered_foldername)
    # Filter raws data for each repeat class to align these for analyses
    for cl in wdclass_list:
        WD_repeat_class_filter(rawdata_folder, fname, cl, filtered_foldername)