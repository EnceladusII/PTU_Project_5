# Script to separate pdb proteic file in ~/common/data/0_raw/pdb/ in her different blades using the extracted raw data in ~/common/data/0_raw/excel/WD_extacted_data.xlsx
# by WITTENMEYER Guillaume, MOSER Mathilda, KESHAVARZ-NAJAFI Mohsen

import os
from pathlib import Path
import Bio.PDB as bp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Path utils:
commonpath = Path(__file__).parent.parent
pdbrawfolder = commonpath / 'data' / '0_raw' / 'pdb'
pdbcutfolder = commonpath / 'data' / '1_intermediate' 
rawexcel = commonpath / 'data' / '0_raw' / 'excel' / 'WD_extracted_data.xlsx'

read_pdb=bp.PDBParser(PERMISSIVE=True, get_header=True, structure_builder=None, QUIET=False)

def find_pdb_files(fpath=str):
    """
        Function which return a  list all pdb files names present in a specific folder
            fpath = folder path to search pdb files (string)
    """
    # Create list for append each pdb file found in fpath
    pdb_list = []
    
    for fname in os.listdir(fpath):
        # Verify if each entity in the forler are a file, and if it's the case verify if the file name end with '.pdb'
        if os.path.isfile(os.path.join(fpath, fname)) and fname.endswith('.pdb'):
            pdb_list.append(fname)
    return pdb_list


def res_filter(structure, resmin=int, resmax=int):
    """
        Function which return a list of all residues containing in a pdb file between a residue number interval [resmin ; resmax]
            structure = a pdb definde as a structure using BioPython
            resmin = residue number for the interval min (integer)
            resmax = residue number for the interval max (integer)
    """
    # Create a list of the wanted residues
    residue_list=[]
    # With BioPython, travel accross the pdb structure
    for model in structure.get_models():
        for chain in model.get_chains():
            # At the residue level, compare the residue number with the interval, if it's in, append the entire residue into the wanted residues list
            for residue in chain.get_residues():
                if residue.get_id()[1] >= resmin and residue.get_id()[1]<=resmax:
                    residue_list.append(residue)

    return residue_list

def write_pdb(s,outfname=str, res_list=list):
    """ 
        Write the structure into a pdb file using an initial pdb and a list of residue to rite in the final structure
            s = a pdb definde as a structure using BioPython
            outfname = output file name for the written structure (string)
            res_list = list of residue return by res_filter() for exemple to write in the outputfname (list)
    """
        
    # PDB format give by the pdb documentation to format a file as a pbd file
    pdbstr = "{:6s}{:5d} {:^4s}{:1s}{:3s} {:1s}{:4d}{:1s}   {:8.3f}{:8.3f}{:8.3f}{:6.2f}{:6.2f}{:>2s}{:2s}\n"
    # Write the structure into the outfname structure file    
    pdb = open(outfname,'w')
    qf = 1.0
    bf = 1.0
    altloc = ''
    atnum = 1
    # Travel accross the initial structure for each residue int the res_list
    for residue in res_list:
        for model in s.get_models():
            for ch in model.get_chains():
                for r in ch.get_residues():
                    # Only write the corresponding residues in the outfname file structure
                    if r==residue:
                        for at in r.get_atoms():
                            (atx,aty,atz) = at.get_coord()
                            atname = at.get_id()
                            resnam = r.get_resname()
                            resnum = r.get_id()[1]
                            cn = ch.get_id()
                            # print(atnum,ch)
                            # Line correspondig to the pdb format
                            line = pdbstr.format('ATOM',atnum,atname,altloc,resnam,cn,resnum,' ',atx,aty,atz,qf,bf,' ',' ')
                            pdb.write(line)
                            atnum += 1
    pdb.close()

def write_blades(dfname=str, pdbpath=str, pdb_outputpath=str):
    """
        Function which automate the process of filter the structure of each blade containing in our ~/common/data/0_raw/excel/WD_extracted_data.xlsx
        of our pdbs structures to analyse these structure using PyMol
            dfname = excel file which contain the WD repeat information (~/common/data/0_raw/excel/WD_extracted_data.xlsx)
            pdbpath = folder path of the entire domain which needed to separate in 7 blades (WD repeats)
            pdb_outputpath = folder path to store the WD repeat cut structure
    """
    # Read the raw data xlsx as a dataframe using Pandas
    df = pd.read_excel(dfname)
    # Have the list of all the raw pdb proteic domain download using AlphaFold (alphafold.py)
    pdblist=find_pdb_files(pdbpath)
    # Create a new folder to store the results if this folder doesn't exist
    if os.path.exists(pdb_outputpath / 'pdb_cut_per_blade'):
        pass
    else:
        os.mkdir(pdb_outputpath / 'pdb_cut_per_blade')
    # For each raw pdb containing in the pdblist we want to cut the pdb for each blade information containing for the proteic structure in the dataframe
    for pdb in pdblist:
        # Define the raw pdb file as a structure using BioPython to use with the functions
        structure=read_pdb.get_structure("structure", pdbpath / pdb)
        # Variable to define each blade in the dataframe as a specific blade number.
        bladenbr=0
        code=pdb[:-4]
        # Found the WD features for a specific pdb ID in the Dataframe and write this feature in a specific pdb file
        for i in range(len(df)):
            if df.iloc[i]['code']==code and df.iloc[i]['feature'] == 'WD':
                bladenbr+=1
                resmin=df.iloc[i]['start']
                resmax=resmin+df.iloc[i]['length']
                res_list=res_filter(structure, resmin, resmax)

                write_pdb(structure, pdb_outputpath / 'pdb_cut_per_blade' / f'{pdb[:-4]}_blade{bladenbr}.pdb', res_list)

# Executing process

write_blades(rawexcel, pdbrawfolder, pdbcutfolder)