# -*- coding: utf-8 -*-
"""
Reads a PDB containing the QM region and writes the atom indexes in the CP2K 
input format. 

About this script:
__name__ = get_qm_kind.py
__author__ = Salome Llabres Prat, PhD
__version__ = 0.1
__email__ = s.llabres@epcc.ed.ac.uk salome.llabres@gmail.com
    Date created: 1/6/2020
    Date last modified: 27/11/2020
    Python Version: 3
"""

import sys,os
import numpy as np
import argparse
from collections import namedtuple 

# Functions
###############################################################################

def read_pdb(pdbfile):
    '''
    Reads a pdb file containing the QM region and returns a list 
    of atomid and elts.
    
    positional arguments:
    pdbfile = (str) Path to a pdbfile 
    
    returns:
    receptor = list of namedtuples of properties of the atoms in the PDB 
    - atomid
    - elts
    elt_list = list of elements included in the qm region. only unique values. 
    '''
    
    # Create receptor list
    receptor = []
    # Create elt_list
    elt_list = []
    # Create named tuple for atoms
    atom = namedtuple('atom', 'id elt')
    
    # Read file and append atom information into receptor
    try:
        with open(pdbfile, 'r') as f:
            while True:
                myline = f.readline()
                if myline == '':
                    break
                elif "ATOM" in myline or "HETATM" in myline:
                    mor = myline.split()
                    newatom = atom(id=int(mor[1]), elt=mor[10],)
                    receptor.append(newatom)
                    if mor[10] not in elt_list:
                        elt_list.append(mor[10])

        return receptor, elt_list
    
    # Returns an exception if PDB is not found                
    except FileNotFoundError:
        message= "Error: file %s was not found\n" % pdbfile
        sys.stderr(message)


def print_qm_kind_region(receptor, elt_list, newfile):
    ''' 
    Writes QM_KIND sections of the CP2K input given a list of atoms. 

    (list, list, str) --> (None)

    '''
    # Open output file
    out = open(newfile+".cp2k",'w')

    # For each elements in elt_list
    for kind in elt_list:
        # Print a message 
        print("Writting "+kind+" atoms.")
        # Writes the QM_king and MM_index format.
        out.write("    &QM_KIND "+kind+"\n")
        out.write("      MM_INDEX")
        # Writes all the indices.
        for atom in receptor:
            if atom.elt == kind:
                out.write(" %d" % atom.id)
                print(atom.id)
        # Writes the end of the QM_kind loop.
        out.write("\n    &END QM_KIND\n")
    # Close output file.
    out.close()


# Main
###############################################################################


if __name__=='__main__':
    
    my_parser = argparse.ArgumentParser(prog="get_qm_kind",
                                        usage="%(prog)s [options] pdbfile", 
                                        description="writes a &QM_KIND section of CP2K given a PDB file")
    my_parser.version="1.0"
    
    my_parser.add_argument("pdbfile", metavar="pdb", type=str, 
                           help="The pdb to analyze")
    my_parser.add_argument("-v", action="version")
    
    
    
    args = my_parser.parse_args()
    pdbfile = args.pdbfile
    ligand, elts = read_pdb(pdbfile)
    print_qm_kind_region(ligand, elts, "qm_region")


