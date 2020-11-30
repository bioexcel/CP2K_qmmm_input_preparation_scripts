# CP2K_qmmm_input_preparation_scripts

A compilation of useful python scripts to create QM/MM CP2K inputfiles.

**Author:** Salomé Llabrés Prat, PhD

<<<<<<< HEAD
##

### cp2krestart2gromacs.py
=======
## 

This repository contains the following scripts:

#### cp2krestart2gromacs.py
>>>>>>> 7e76fd11d55599020d1e0edb2b0b2d063353f257

This script converts CP2K restart file to GROMACS files.

*Usage:*

```cp2krestart2gromacs [options] infile outfile```


#### cp2kinput2ndxformat.py

This script converts CP2K input file to a GROMACS NDX file. 

*Usage:*

```cp2kinput2ndxformat.py [options] cp2kinputfile```


#### get_qm_kind.py 

Reads a PDB containing the QM region and writes the atom indexes in the CP2K input format. 

<<<<<<< HEAD
**Usage:** 
=======
*Usage:*
>>>>>>> 7e76fd11d55599020d1e0edb2b0b2d063353f257

```python3 get_qm_kind [options] pdbfile```


