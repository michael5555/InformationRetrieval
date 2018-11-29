# InformationRetrieval
This is the repo for the Information Retrieval project by Michaël Adriaensen and Ken Bauwens.

# Usage
first we need to index with this command:  
    python3 indexer.py <csvdir>  
Here csvdir needs to be a directory with csv's with the following structure:  
    "id,text,redditid,subreddit,metareddit,time,author,ups,downs,authorlinkkarma,authorkarma,authorisgold"  
Then run the querier:  
    python3 querier.py  

# Extra
added a python3 script to remove dups from the reddit dataset and a bash script to automate for all csv's.

# Github Repository ( with datasets and other unnecessary stuff)
https://github.com/michael5555/InformationRetrieval.git




