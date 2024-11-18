# Exploration of New Approaches for Defining and Evaluating a Family of Repeated Regions by Alignment Using UniProt Annotations and AlphaFold Predictions

## Overview
WD repeats form one of the largest fold families in humans, with over 2,000 instances across 300 different proteins. These repeated regions assemble into a three-dimensional globular structure known as a beta-propeller, featuring 4 to 8 blades depending on the repeat families. Due to their high sequence variability, WD repeats are challenging to characterize and classify, leading to frequent annotation errors in the UniProt database.

This project proposes a novel approach by focusing directly on WD repeats, analyzing them through sequence and structural alignment using data from UniProt and AlphaFold. The goal is to propose multiple definitions for WD repeats and establish objective criteria to assess the validity of each.

## Project Objectives
1. **Query UniProt for WD repeat annotations**
2. **Align, filter, and group repeat sequences**, and identify critical residues
3. **Retrieve AlphaFold (and/or PDB) predicted structures**, superimpose, filter, and group these structures
4. **Identify critical residues in the structures** and compare them with sequence alignment results
5. **Compare results with existing annotations**, identifying cases where the annotation might be incorrect
6. **Define multiple ways to characterize WD repeats** within beta-propellers and quantify the relevance of each method

## Approach
This project is divided into several key tasks:
- **Data Collection**: Retrieve annotations of WD repeats from the UniProt database.
- **Sequence Alignment**: Align, filter, and group WD repeat sequences, and identify critical residues for each group.
- **Structural Alignment**: Collect predicted structures of WD repeats from AlphaFold and/or PDB, superimpose, filter, and group these structures.
- **Critical Residue Identification**: Identify critical residues in both sequence and structural alignments, and compare results.
- **Annotation Assessment**: Compare your conclusions with existing UniProt annotations, identifying potential annotation errors.
- **WD Repeat Redefinition**: Propose different ways to define WD repeats within beta-propellers and establish criteria for evaluating each method.

## Potential Collaboration
Collaboration with **Project 3** is possible, allowing the exploration of further methods and perspectives for redefining the boundaries of beta-propellers formed by WD repeats.


<======================== Cahier de Laboratoire  ===============================>
## Abbréviation utilisé
AAs --> Acides Aminés


## Cahier de laboratoire
    Format : 
    {**AAAA-MM-DD :**
    travail excécuté par :
    "contenu"}

**2024-10-19 :**  
Travail excecuté par : MOSER Mathilda  
Production des premier alignements à partir des séquences fasta des WD repeats, des WD repeats étendus de 10 acides aminés (AAs) de chaque coté et des WD repeats étendus de 20 AAs de chaque coté. Les fichiers de sorties sont réorganisés
Ces alignements ont été obtenu grâce à la version web en ligne de clustalΩ disponible à cette adresse : " https://www.ebi.ac.uk/jdispatcher/msa/clustalo " .  Les paramètres d'entrée ont été laissés par défaut sur le site sauf pour le format qui à été changé vers le format FASTA.  

(PARAMETRES UTILISEES :
  - OUTPUT FORMAT : Pearson/FASTA
  - DEALIGN INPUT : NO
  - MBED-LIKE CLUSTERING GUIDE-TREE : yes
  - MBED-LIKE CLUSTERING ITERATION : yes
  - COMBINED ITERATIONS : default(0)
  - MAX GUIDE TREE : default
  - MAX HMM ITERATIONS : default
  - ORDER : aligned
  - DISTANCE MATRIX : no
  - OUTPUT GUIDE TREE : yes )  

Les résultats ont été obtenues au format FASTA et on été visualisé en utilisant le programme Jalview v2.11.4.0. 
À cette étape du projet, aucune conclusion ni correction n'a été apporté vis-à-vis de ces alignements.

**2024-10-29**  
Travail executé par : WITTENMEYER Guillaume  
Pour comparer avec avec l'alignement de clustalΩ, génération d'alignement de ces séquences grâce au programme MAFFT via l'interface web " https://usegalaxy.eu " avec l'historique accessible ici : " https://usegalaxy.eu/u/encelade/h/wdrepeats "
(PARAMETRES UTILISES :
 - Type of sequences : Amino acids
 - Type of scoring matrix : BLOSUM
 - Coefficient of the BLOSUM matrix : 62
 - Configure gap costs : Use default values
 - Reorder output : Yes/No (générer un de chaque)
 - Output format : FASTA )

Les résultats ont été enregistrés au format FASTA avec le PATH: " /data/projet5/common/data/1_intermediate/MAFFT_alignment "
Les résultats ont été obtenues au format FASTA et on été visualisé en utilisant le programme Jalview v2.11.4.0.

**2024-10-29**  
Travail excecuté par : WITTENMEYER Guillaume, KESHAVARZ-NAJAFI Mohsen, MOSER Mathilda  
Production de nouveaux alignements en utilisant MAFFT. Nous avons générés, pour chaque fichier d'entrée, deux fichiers de sorties. Le premier fichier de sortie possèdent l'ordre du fichier d'entrée. l'ordre des séquence à été réorganisé automatiquement pour le deuxième fichier. 
Ces étapes ont été réalises à partir des séquences fasta des WD repeats, des WD repeats étendus de 10 acides aminés (AAs) de chaque coté et des WD repeats étendus de 20 AAs de chaque coté.

Les résultats ont été obtenues au format FASTA et on été visualisé en utilisant le programme Jalview v2.11.4.0.

**2024-10-29**  
Travail excecuté par : WITTENMEYER Guillaume, KESHAVARZ-NAJAFI Mohsen, MOSER Mathilda  
A partir de l'alignement ne possédant pas les AAs supplémentaire, nous avons essayer de trouver des résidus fortements conservés, nosu avons principalement trouvés des résidues hydrophobes, apolaires et non ionisables (Val, Leu, Ile, Gly)

Les résultats ont été obtenues au format FASTA et on été visualisé en utilisant le programme Jalview v2.11.4.0.


---

For detailed guidance or troubleshooting, please refer to the full project documentation or contact the project lead.
