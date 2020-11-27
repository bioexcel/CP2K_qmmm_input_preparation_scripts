# CP2K_qmmm_input_preparation_scripts
A compilation of useful python scripts to create QM/MM CP2K inputfiles

**Author:** Salomé Llabrés Prat, PhD

This repository contains the following scripts:

### cp2krestart2gromacs.py

This script converts CP2K restart file to GROMACS files.

**Usage:**


### cp2kinput2ndxformat.py

This script converts CP2K input file to a GROMACS NDX file. 

**Usage:**


### get_qm_kind.py 

Reads a PDB containing the QM region and writes the atom indexes in the CP2K input format. 

**Usage:** 

```python3 get_qm_kind [options] pdbfile```


