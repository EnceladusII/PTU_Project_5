import os
from pathlib import Path

# Path utils:
commonpath = Path(__file__).parent.parent
fpath= commonpath / 'data' / '1_intermediate' / 'pdb_cut_per_blade'

pdb_list = []
for fname in os.listdir(fpath):
    if os.path.isfile(os.path.join(fpath, fname)) and fname.endswith(f'blade{bladenbr}.pdb'):
        pdb_list.append(fname)

for i in range(1, len(pdb_list)):
    load(fpath / pdb_list[i], pdb_list[i][-4])

for i in range(2, len(fpath)):
    align(pdb_list[i][-4], pdb_list[1][-4])