'''
This script converts CP2K input file to a GROMACS NDX file. It does so following these
steps:

1 - Reads CP2K inputfile.
2 - Writes the indexes in the GROMACS NDX format. 

About this script:
__name__ = cp2kinput2ndxformat.py
__author__ = Salome Llabres Prat
__version__ = 0.1
__email__ = s.llabres@epcc.ed.ac.uk salome.llabres@gmail.com
    Date created: 20/5/2020
    Date last modified: 27/11/2020
    Python Version: 3

TO DO:
- Add exceptions
'''

import argparse

# Functions
###############################################################################

def read_cp2k_input(filename):
    '''
    Reads a CP2K input file and collects a list of QM atoms and Link atoms.
    
    I/O:
    (str) --> (list, list)
    (pdbfile) --> (list of qmatoms, list of linkatoms)

    Usage:
    read_cp2k_input("CP2Kinputfile.inp")
    '''
    
    qmatoms = []
    latoms = []

    # Read PDBfile and write information into B-factor column
    try:
        with open(filename, 'r') as f:
            while True:
                # Readline 
                myline = f.readline()
                # break at the end of the file
                if myline == '':
                    break
                # QM region
                elif "&QM_KIND" in myline:
                	myline = f.readline()
                	if "MM_INDEX" in myline:
                		mor = myline.split()
                		for elt in mor[1:]:
                			qmatoms.append(int(elt))
                elif "&LINK" in myline:
                	myline = f.readline()
                	myline = f.readline()
                	if "MM_INDEX" in myline:
                		mor = myline.split()
                		for elt in mor[1:]:
                			latoms.append(int(elt))
    except:
        raise 

    return qmatoms, latoms


def write_ndx(atoms, header):
	''' 
    Writes a GROMACS NDX file with the atom indexes.

    I/O:
    (list, str) --> (None)
    (list of atoms, Header for the ndx mask) --> (None)

    Usage:
    write_ndx(atoms, "QM atoms")
	'''

	# Open output file
	out = open(header+".ndx",'w')
    # Order aton indexes
	new_atoms = sorted(atoms)

    # Write NDX format
	out.write("[ "+header+" ]\n")
	count = 0
	for atom in new_atoms:
		if count == 15:
			out.write("\n")
			count = 0 
		out.write("%5d " % atom)
		count = count + 1
	out.close()

    
# Main
###############################################################################

if __name__=='__main__':
    
    my_parser = argparse.ArgumentParser(prog="cp2kinput2ndxformat.py",
                                        usage="%(prog)s [options] cp2kinputfile", 
                                        description="writes a &QM_KIND section of CP2K given a PDB file")
    my_parser.version="1.0"
    
    my_parser.add_argument("cp2kinputfile", metavar="inp", type=str, 
                           help="The CP2K input file to process")
    my_parser.add_argument("-v", action="version")

    # Parser
    args = my_parser.parse_args()
    inpfile = args.inpfile

    print("Read the CP2K input file:")
    qmatoms, latoms = read_cp2k_input(inpfile)
    print("Write GROMACS NDX:")
    print("- QM region atoms", len(qmatoms))
    write_ndx(qmatoms, "QM region")
    print("- Link atoms", len(latoms))
    write_ndx(latoms, "Link region")

