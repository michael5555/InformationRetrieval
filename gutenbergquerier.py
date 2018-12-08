import os, sys, lucene

from java.nio.file import Paths
from java.lang import System
from java.text import DecimalFormat
from java.util import Arrays

from org.apache.lucene.search import IndexSearcher, TermQuery, MatchAllDocsQuery,BooleanQuery,BooleanClause
from org.apache.lucene.store import FSDirectory, SimpleFSDirectory
from org.apache.lucene.index import (IndexWriter, IndexReader,
                                     DirectoryReader, Term,
                                     IndexWriterConfig)
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer

from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document
from org.apache.lucene.queries.mlt import MoreLikeThis


TEXT = "text"

class Querrier(object):

    def __init__(self, baseDir, indexDirectory="IR.Index"):
        """
        :param baseDir: The directory where this querrier is run
        :param indexDirectory: Directory of indices, default value = 'IR.Index'
        """
        indexDir = FSDirectory.open(Paths.get(os.path.join(baseDir, indexDirectory)))

        self.reader = DirectoryReader.open(indexDir)

    def searchWithTerm(self, query):
        """
        Search an index with facets by using simple term query
        return a list of FacetResult instances
        """
        analyzer = LimitTokenCountAnalyzer(StandardAnalyzer(), 1048576)
        query = QueryParser("content", analyzer).parse(query)
        return self.searchWithQuery(query)

    def searchWithQuery(self, query):
        """
        Search an index with facets for a given query
        return a list of FacetResult instances
        """
        # prepare searcher to search against
        searcher = IndexSearcher(self.reader)
        scoreDocs = searcher.search(query, 10).scoreDocs

        return scoreDocs

    def expandQuery(self,result,nrRelevant):
        searcher = IndexSearcher(self.reader)
     
        relevant = []
        mlt = MoreLikeThis(self.reader)
        for i in result[0:nrRelevant - 1]:
            docid = self.reader.doc(i.doc)
            relevant.append(mlt.like(docid))

        querybuilder = BooleanQuery.Builder()
        for i in relevant:
            querybuilder.add(i,BooleanClause.Occur.SHOULD)

        combinedquery = querybuilder.build()
        scoreDocs = searcher.search(combinedquery, 10).scoreDocs
        return scoreDocs


if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    searcher = Querrier(os.path.dirname(os.path.abspath(sys.argv[0])))

    while True:
        # Loop and search until the empty string is given
        print("Enter searchquery (enter empty string to exit):")
        value = input()

        if value == "":
            # Break the loop
            print("The querrier will shut down.")
            break

        # Get search values and display to user
        result = searcher.searchWithTerm(value)
        for res in result:
            ixreader = IndexSearcher(searcher.reader)
            doc = ixreader.doc(res.doc)
            text = doc.get("content")
            author = doc.get("author")
            title = doc.get("title")
            score = res.score

            print("title: {0}author: {1}score: {2}\n".format(title,author,score))

        print("Do you want to expand your query? [Y/n] (enter empty string to exit):")
        expandval = input()

        if expandval == "":
            # Break the loop
            print("The querrier will shut down.")
            break
        elif expandval == "n" or "no" or "N" or "NO":
            continue

        elif expandval == "y" or "Y" or "Yes" or "YES":

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
            




