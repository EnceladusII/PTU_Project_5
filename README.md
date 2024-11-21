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

## Laboratory Notebook  
Check ~/lab_notebook.odt  

Conda environment parameter = {

	python -- version = 3.9.20

		Package             Version
	------------------- -----------
	biopython           1.84
	Bottleneck          1.4.2
	Brotli              1.1.0
	certifi             2024.8.30
	cffi                1.17.1
	charset-normalizer  3.4.0
	contourpy           1.2.0
	cycler              0.11.0
	et-xmlfile          1.1.0
	fonttools           4.51.0
	h2                  4.1.0
	hpack               4.0.0
	hyperframe          6.0.1
	idna                3.10
	importlib_resources 6.4.0
	kiwisolver          1.4.4
	matplotlib          3.9.2
	numexpr             2.10.1
	numpy               1.26.4
	openpyxl            3.1.5
	packaging           24.1
	pandas              2.2.2
	pillow              11.0.0
	pip                 24.2
	ply                 3.11
	pycparser           2.22
	pyparsing           3.2.0
	PyQt5               5.15.10
	PyQt5-sip           12.13.0
	PySocks             1.7.1
	python-dateutil     2.9.0.post0
	pytz                2024.1
	requests            2.32.3
	scipy               1.11.4
	setuptools          75.1.0
	sip                 6.7.12
	six                 1.16.0
	tomli               2.0.1
	tornado             6.4.1
	tzdata              2023.3
	unicodedata2        15.1.0
	urllib3             2.2.3
	weblogo             3.7.12
	wheel               0.44.0
	zipp                3.20.2
	zstandard           0.23.0	
}

---

For detailed guidance or troubleshooting, please refer to the full project documentation or contact the project lead.
