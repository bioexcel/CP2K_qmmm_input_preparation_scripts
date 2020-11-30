# CP2K_qmmm_input_preparation_scripts

A compilation of useful python scripts to create QM/MM CP2K inputfiles.

**Author:** Salomé Llabrés Prat, PhD

# 

This repository contains the following scripts:

#### cp2krestart2gromacs.py
This script converts CP2K restart file to GROMACS files. It does so following these
steps:

1 - Reads CP2K restart file.
2 - Generates a AMBER restart file.
3 - Convert AMBER (.prmtop and .inpcrd) to GROMACS format (.top and .gro) via parmed. 
4 - Rewrites GROMACS coordinates to include velocities. 

It requires the CP2K restart file and a basename to name the gromacs files. 
It needs parmed!

It outputs these files:

   AMBER restart file:                  basename.inpcrd 
   GROMACS topology:                    basename.top 
   GROMACS coordinates:                 basename.gro 
   GROMACS coordinates + velocities:    basename.vel.gro 

*Usage:*

```
cp2krestart2gromacs [options] infile outfile
```

#

#### cp2kinput2ndxformat.py

This script collects atom indexes outlined in the QM region and link atoms of a CP2K input file and writes a GROMACS NDX file for each QM region and for Link atoms. 

*Usage:*

```
cp2kinput2ndxformat.py [options] cp2kinputfile
```

#

#### get_qm_kind.py 

Reads a PDB containing the QM region and writes the atom indexes in the CP2K input format. 

*Usage:*

```
python3 get_qm_kind [options] pdbfile
```

