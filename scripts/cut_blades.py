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
        Function for append in a  list all pdb files names present in a folder
    """
    pdb_list = []
    for fname in os.listdir(fpath):
        if os.path.isfile(os.path.join(fpath, fname)) and fname.endswith('.pdb'):
            pdb_list.append(fname)
    return pdb_list


def blade_filter(structure, resmin=int, resmax=int):
    """
    
    """
    residue_list=[]

    for model in structure.get_models():
        for chain in model.get_chains():
            for residue in chain.get_residues():
                if residue.get_id()[1] >= resmin and residue.get_id()[1]<=resmax:
                    residue_list.append(residue)

    return residue_list

def write_pdb(s,outfname=str, res_list=list):
    """ Write the structure into a pdb file """
        
    # PDB format
    pdbstr = "{:6s}{:5d} {:^4s}{:1s}{:3s} {:1s}{:4d}{:1s}   {:8.3f}{:8.3f}{:8.3f}{:6.2f}{:6.2f}{:>2s}{:2s}\n"
        
    pdb = open(outfname,'w')
    qf = 1.0
    bf = 1.0
    altloc = ''
    atnum = 1
    for residue in res_list:
        for model in s.get_models():
            for ch in model.get_chains():
                for r in ch.get_residues():
                    if r==residue:
                        for at in r.get_atoms():
                            (atx,aty,atz) = at.get_coord()
                            atname = at.get_id()
                            resnam = r.get_resname()
                            resnum = r.get_id()[1]
                            cn = ch.get_id()
                            # print(atnum,ch)
                            line = pdbstr.format('ATOM',atnum,atname,altloc,resnam,cn,resnum,' ',atx,aty,atz,qf,bf,' ',' ')
                            pdb.write(line)
                            atnum += 1
    pdb.close()

def write_blades(dfname=str, pdbpath=str, pdb_outputpath=str):
    """
    
    """

    df = pd.read_excel(dfname)
    pdblist=find_pdb_files(pdbpath)

    if os.path.exists(pdb_outputpath / 'pdb_cut_per_blade'):
        pass
    else:
        os.mkdir(pdb_outputpath / 'pdb_cut_per_blade')

    for pdb in pdblist:
        structure=read_pdb.get_structure("structure", pdbpath / pdb)
        bladenbr=0
        code=pdb[:-4]

        for i in range(len(df)):
            if df.iloc[i]['code']==code and df.iloc[i]['feature'] == 'WD':
                bladenbr+=1
                resmin=df.iloc[i]['start']
                resmax=resmin+df.iloc[i]['length']
                res_list=blade_filter(structure, resmin, resmax)

                write_pdb(structure, pdb_outputpath / 'pdb_cut_per_blade' / f'{pdb[:-4]}_blade{bladenbr}.pbd', res_list)

write_blades(rawexcel, pdbrawfolder, pdbcutfolder)