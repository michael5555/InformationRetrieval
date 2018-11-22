import sys
import pandas as pd

if __name__ == '__main__':

    if len(sys.argv) >= 3:

        readfile = sys.argv[1]
        outfile = sys.argv[2]

        toclean = pd.read_csv(readfile,header=None,names=["id","idfloatminusone","text","redditid","subreddit","metareddit","time","author","ups","downs","authorlinkkarma","authorkarma","authorisgold"])
        deduped = toclean.drop_duplicates(["text","author"])
        deduped.to_csv(outfile)