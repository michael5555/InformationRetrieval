import sys
import pandas as pd

if __name__ == '__main__':

    style1 =["entertainment_anime.csv","entertainment_comicbooks.csv","entertainment_harrypotter.csv","entertainment_movies.csv"]

    if len(sys.argv) >= 3:

        readfile = sys.argv[1]
        outfile = sys.argv[2]

        if readfile in style1:
            n1 = ["id","idfloatminusone","text","redditid","subreddit","metareddit","time","author","ups","downs","authorlinkkarma","authorkarma","authorisgold"]
            toclean = pd.read_csv(readfile,header=None,skiprows=2,names=n1)
            deduped = toclean.drop_duplicates(["text","author"])
            deduped = deduped.drop(columns=["id","idfloatminusone"])
            deduped.to_csv(outfile)

        else:
            n1 = ["id","text","redditid","subreddit","metareddit","time","author","ups","downs","authorlinkkarma","authorkarma","authorisgold"]
            toclean = pd.read_csv(readfile,header=None,skiprows=1,names=n1)

            deduped = toclean.drop_duplicates(["text","author"])
            deduped = deduped.drop(columns=["id"])
            deduped.to_csv(outfile)

