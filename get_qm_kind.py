# -*- coding: utf-8 -*-
"""
Reads a PDB containing the QM region and writes the atom indexes in the CP2K 
input format. 

About this script:
__name__ = get_qm_kind.py
__author__ = Salome Llabres Prat, PhD
__version__ = 0.1
__email__ = salome.llabres@gmail.com
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
    Reads a pdb file containing the QM region and returns two lists 
    of namedtuples containing all atomid and elts and list of unique elements 
    in the PDB file.
    
    I/O:
    (str) --> (list, list)
    (pdbfile) --> (list of namedtuples (atoms, element), list of elements)

    Usage:
    read_pdb("pdbfile.pdb") 
    '''
    
    # Create receptor list
    qmregion = []
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
                    qmregion.append(newatom)
                    if mor[10] not in elt_list:
                        elt_list.append(mor[10])

        return qmregion, elt_list
    
    # Returns an exception if PDB is not found                
    except FileNotFoundError:
        message= "Error: file %s was not found\n" % pdbfile
        sys.stderr(message)


def write_qm_kind_region(qmregion, elt_list, newfile):
    ''' 
    Writes QM_KIND sections of the CP2K input given a list of atoms. 
    
    I/O:
    (list, list, str) --> (None)
    (list of namedtuples, list of elements, output name) --> (None)

    Usage:
    write_qm_kind_region(qmregion, elts, "qm_region")
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
        for atom in qmregion:
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
    
    my_parser = argparse.ArgumentParser(prog="get_qm_kind.py",
                                        usage="%(prog)s [options] pdbfile", 
                                        description="writes a &QM_KIND section of CP2K given a PDB file")
    my_parser.version="1.0"
    
    my_parser.add_argument("pdbfile", metavar="pdb", type=str, 
                           help="The pdb to process")
    my_parser.add_argument("-v", action="version")
    
    
    # Parser
    args = my_parser.parse_args()
    pdbfile = args.pdbfile

    # Process PDB
    qmregion, elts = read_pdb(pdbfile)
    write_qm_kind_region(qmregion, elts, "qm_region")


