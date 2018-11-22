import sys
import pandas as pd

if __name__ == '__main__':

    if len(sys.argv) >= 3:

        readfile = sys.argv[1]
        outfile = sys.argv[2]

        toclean = pd.read_csv(readfile,header=None,skiprows=2)
        deduped = toclean.drop_duplicates([2,7])
        deduped.to_csv(outfile)