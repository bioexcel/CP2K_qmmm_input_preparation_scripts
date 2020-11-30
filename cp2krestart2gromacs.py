'''
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

About this script:
__name__ = cp2krestart2gromacs.py
__author__ = Salome Llabres Prat
__version__ = 0.1
__email__ = s.llabres@epcc.ed.ac.uk
    salome.llabres@gmail.com
    Date created: 20/5/2020
    Date last modified: 27/11/2020
    Python Version: 3

TODO: 
- add exceptions!
'''

import parmed
import argparse

# Functions
###############################################################################

def convert_cp2k2amber_units(value):
    ''' CP2K velocities (bohr/au_time) to amber velocities(Å/20.455ps)

    Given that au_time = 0.0242 fs and bohr = 0.529177 A

    More info about cp2k units here: 
        https://manual.cp2k.org/trunk/CP2K_INPUT/MOTION/PRINT/VELOCITIES.html#UNIT
    More info about amber units here: 
        archive.ambermd.org/200811/0164.html
    
    I/O:
        (float) --> (float)
        (velocities cp2k format) --> (velocities amber format)
    '''

    return value*0.529177*1000/0.0242/20.455


def convert_cp2k2gromacs_units(value):
    ''' CP2K velocities (bohr/au_time) to gromacs velocities(nm/ps)

    Given that au_time = 0.0242 fs and bohr = 0.0529177 nm

    More info about cp2k units here: 
        https://manual.cp2k.org/trunk/CP2K_INPUT/MOTION/PRINT/VELOCITIES.html#UNIT
    More info about gromacs units here: 
        manual.gromacs.org/archive/5.0.4/online/gro.html
    
    I/O:
        (float) --> (float)
        (velocities cp2k format) --> (velocities amber format)
    '''

    return value*0.0529177*1000/0.0242


def read_cp2k_restart(filename):
    '''
    Reads a CP2K restart file and collects coordinates, velocities and box size.
    
    returns:
        list with box xyz
        list with all coordinates
        list with all velocities
        str with topology

    I/O:
        (string) --> (list, list, list)
        (cp2k restart file) --> (box, coordinates amber velocities)
    '''
    
    coord_flag = False
    coord = []
    vel_flag = False
    vel = []
    cell_flag = False
    box = [0,0,0]
    velcount = 0

    # Read PDBfile and write information into B-factor column
    try:
        with open(filename, 'r') as f:
            while True:
                # Readline 
                myline = f.readline()
                #print(myline)
                # break at the end of the file
                if myline == '':
                    break

                # Box size
                elif "&CELL" in myline:
                    cell_flag = True
                elif "&END CELL" in myline:
                    cell_flag = False
                elif cell_flag:
                    mor = myline.split()
                    if mor[0] == "A":
                        box[0] = float(mor[1])
                    elif mor[0] == "B":
                        box[1] = float(mor[2])
                    elif mor[0] == "C":
                        box[2] = float(mor[3])

                # Topology file
                if "PARM_FILE_NAME" in myline:
                    mor = myline.split()
                    top =mor[1]

                # Coordinates
                elif "&COORD" in myline:
                    coord_flag = True
                    print("   Read coord_flag...")

                elif "&END COORD" in myline:
                    coord_flag = False
                elif coord_flag:
                    mor = myline.split()
                    coord.append(float(mor[1]))
                    coord.append(float(mor[2]))
                    coord.append(float(mor[3]))

                # Velocities
                elif "&VELOCITY" in myline:
                    velcount = velcount + 1 
                    if velcount == 2:
                        vel_flag = True
                        print("   Read vel_flag...")
                elif "&END VELOCITY" in myline:
                    vel_flag = False
                elif vel_flag:
                    mor = myline.split()
                    # Save velocities with gromacs units
                    vel.append(float(mor[0]))
                    vel.append(float(mor[1]))
                    vel.append(float(mor[2]))
    except:
        raise 

    return box, coord, vel, top


def write_amber_restrt_file(newfile, box, coord, vel):
    '''
    Writes a new CRD file (using newfile as basename).

    Reference: https://ambermd.org/FileFormats.php#restart

    I/O:
        (str, list, list, list) --> (None)
        (filename, box, coordinates, velocities) --> (None)
    '''

    # Open output file
    out = open(newfile+".inpcrd",'w')

    out.write("Restart built from CP2K restart file.\n")
    out.write(str(int(len(coord)/3))+"\n")

    print("   Writing coordinates...")
    count = 0
    for c in coord:
        if count == 5:
            out.write("%12.7f\n" % c)
            count = 0
        else:
            out.write("%12.7f" % c)
            count = count + 1

    if (len(coord)/3 % 2) != 0:
        out.write("\n")

    print("   Writing velocities...")
    count = 0
    for v in vel:
        if count == 5:
            out.write("%12.7f\n" % convert_cp2k2amber_units(v))
            count = 0
        else:
            out.write("%12.7f" % convert_cp2k2amber_units(v))
            count = count + 1
    
    if (len(vel)/3 % 2) != 0:
        out.write("\n")

    print("   Writing box...")
    # Assuming cubic box
    out.write("%12.7f%12.7f%12.7f%12.7f%12.7f%12.7f" % (box[0], box[1], box[2], 90.0, 90.0, 90.0))

    out.close()

def add_velocities_to_grofile(grofile, vel):
    ''' Adds velocities to an existing GRO file.

    Using the following formar: 
        http://manual.gromacs.org/archive/5.0.4/online/gro.html 

    I/O:
        (str, list) --> (None)
        (filename, velocities) --> (None)
    '''
    
    # Open output file
    out = open(grofile+".vel.gro",'w')
    
    # Read PDBfile and write information into B-factor column
    try:
        with open(grofile+".gro", 'r') as f:
            # Skipping the first 2 lines : label and n_atoms
            out.write(f.readline())
            out.write(f.readline())
            while True:
                myline = f.readline()
                mor = myline.split()
                if myline == '':
                    break
                # Continue when you find a water molecule
                elif len(mor) == 3:
                    out.write(myline)
                    out.write("\n")
                else:
                    out.write("%5d%-5s%5s%5d%8.3f%8.3f%8.3f%8.4f%8.4f%8.4f\n" % 
                    #out.write("%5d%-5s%5s%5d%8.3f%8.3f%8.3f\n" % 
                        (int(myline[0:5]), myline[5:10], myline[10:15], 
                        int(myline[15:20]), float(myline[20:28]), float(myline[28:36]), 
                        float(myline[36:44]), 
                        convert_cp2k2gromacs_units(vel.pop(0)), 
                        convert_cp2k2gromacs_units(vel.pop(0)), 
                        convert_cp2k2gromacs_units(vel.pop(0))))

        out.close()
        if len(vel) != 0:
            print("WARNING: There is some error with the velocities.")
    except:
        raise


def convert_parmed(newfile ,top):
    '''Converts the topology and the coordinate file from AMBER to GROMACS via parmed.
    '''
    # load AMBER files
    amber = parmed.load_file(top, xyz=newfile+'.inpcrd')
    #save a GROMACS topology and GRO file
    amber.save(newfile+'.top')
    amber.save(newfile+'.gro')
    print("   Parmed created GROMACS .top & .gro files...")


# Main
###############################################################################

if __name__ == '__main__':

    my_parser = argparse.ArgumentParser(prog="cp2krestart2gromacs",
                                        usage="%(prog)s [options] infile outfile", 
                                        description="Converts CP2K restart file to GROMACS format (including velocities).")
    my_parser.version="1.0"
    my_parser.add_argument("infile", metavar="in", type=str, 
                           help="CP2K restart file")
    my_parser.add_argument("outfile", metavar="out", type=str, 
                           help="basename for gromacs files")
    my_parser.add_argument("-v", action="version")

    # Get filenames from parser
    args = my_parser.parse_args()
    infile = args.infile
    newfile = args.outfile

    # Read CP2K file and output a summary:
    print("Reading CP2K restart file: "+infile+".")
    box, coord, vel, top = read_cp2k_restart(infile)

    print("\n=======================================================")
    print("   Box size read:\t"+str(len(box)))
    print("   Coordinates read:\t"+str(int(len(coord)/3)))
    print("   Velocities read:\t"+str(int(len(vel)/3)))
    print("   Topology file read:\t"+top)
    print("=========================================================\n")

    # Print an AMBER CRD file (+velocities)
    print("Writing new CRD file: "+newfile+".inpcrd.")
    write_amber_restrt_file(newfile, box, coord, vel)

    # Convert filr format with Parmed
    print("\nConvert AMBER topology and coordinates to GROMACS.")
    convert_parmed(newfile, top)

    # Add velocities to GRO file
    print("\nAdding velocities to .gro file: "+newfile+".vel.gro.")
    add_velocities_to_grofile(newfile, vel)

    # Print a summary
    print("\n=======================================================")
    print("Files created")
    print("   AMBER restart file:\t\t\t"+newfile+".inpcrd ")
    print("   GROMACS topology:\t\t\t"+newfile+".top ")
    print("   GROMACS coordinates:\t\t\t"+newfile+".gro ")
    print("   GROMACS coordinates + velocities:\t"+newfile+".vel.gro ")
    print("==========================================================\n")
