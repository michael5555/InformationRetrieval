from more_itertools import unique_everseen
import sys


if __name__ == '__main__':

    if len(sys.argv) >= 3:

        readfile = sys.argv[1]
        outfile = sys.argv[2]


        with open(readfile,'r') as f, open(outfile,'w') as nodups:
            nodups.writelines(unique_everseen(f))