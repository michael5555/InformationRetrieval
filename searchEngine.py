
import os, sys, lucene
lucene.initVM(vmargs=['-Djava.awt.headless=true'])


from org.apache.lucene.search import IndexSearcher, TermQuery, MatchAllDocsQuery,BooleanQuery,BooleanClause

from synonymGenerator import Synonyms
from querier import Querrier



if __name__ == '__main__':
    searcher = Querrier(os.path.dirname(os.path.abspath(sys.argv[0])))
    synonym = Synonyms()


    while True:
        # Loop and search until the empty string is given
        print("Enter searchquery (enter empty string to exit):")
        value = input()

        if value == "":
            # Break the loop
            print("The querrier will shut down.")
            break

        # Expand query
        print("Expanding query with synonyms")
        newQuery = " ".join(synonym.getSynonymList(value))
        print("Changed query: {}\nto:{}".format(value, newQuery))
        # Get search values and display to user

        # Get search values and display to user
        result = searcher.searchWithTerm(newQuery)
        for res in result:
            ixreader = IndexSearcher(searcher.reader)
            doc = ixreader.doc(res.doc)
            text = doc.get("content")
            author = doc.get("author")
            title = doc.get("title")
            score = res.score

            print("title: {0}author: {1}score: {2}\n".format(title,author,score))

        print("Do you want to perform pseudo relevance feedback? [Y/n] (enter empty string to exit):")
        expandval = input()

        if expandval == "":
            # Break the loop
            print("The querier will shut down.")
            break
        elif expandval == "n" or expandval == "no" or expandval == "N" or expandval ==  "NO":
            continue

        elif expandval == "y" or expandval ==  "Y" or expandval == "Yes" or expandval == "YES":
            print("performing relevance feedback ...")
            # expand query and output results
            expresult = searcher.expandQuery(result,3)
            for res in expresult:
                ixreader = IndexSearcher(searcher.reader)
                doc = ixreader.doc(res.doc)
                text = doc.get("content")
                author = doc.get("author")
                title = doc.get("title")
                score = res.score

                print("title: {0}author: {1}score: {2}\n".format(title,author,score))