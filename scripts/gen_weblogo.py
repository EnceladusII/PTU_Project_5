from weblogo import *
from pathlib import Path

# Path utils:
commonpath = Path(__file__).parent.parent
rawdata_folder = commonpath / 'data' / '1_intermediate' / 'MAFFT_alignment'

# Charger les séquences depuis un fichier FASTA
fin = open(rawdata_folder / 'MAFFT_WD_sequence.fasta')
seqs = read_seq_data(fin)

# Créer l'objet LogoData
logodata = LogoData.from_seqs(seqs)

# Définir les options pour le logo
logooptions = LogoOptions()
logooptions.title = "A Logo Title"  # Titre du logo

# Créer le format du logo
logoformat = LogoFormat(logodata, logooptions)

# Générer le logo en SVG
png_data = png_formatter(logodata, logoformat)

# Sauvegarder le logo en fichier SVG
output_path = commonpath / 'output_logo.svg'
with open(output_path, 'wb') as f:
    f.write(png_data)
    
print(f"Logo SVG généré et sauvegardé sous {output_path}")

