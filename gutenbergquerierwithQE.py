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
from java.io import StringReader;
from wordnetTest import Synonyms



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
        analyzer = LimitTokenCountAnalyzer(StandardAnalyzer(), 1048576)

     
        relevant = []
        mlt = MoreLikeThis(self.reader)
        mlt.setAnalyzer(analyzer)
        for i in result[0:nrRelevant - 1]:
            doc = self.reader.document(i.doc)
            sr = StringReader(doc.get("content"))
            relevant.append(sr)

        """querybuilder = BooleanQuery.Builder()
        for i in relevant:
            querybuilder.add(i,BooleanClause.Occur.SHOULD)

        combinedquery = querybuilder.build()"""
        mltquery = mlt.like("content",relevant)
        scoreDocs = searcher.search(mltquery, 10).scoreDocs
        return scoreDocs


if __name__ == '__main__':
    # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
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
        print("Expanding query")
        newQuery = " ".join(synonym.getSynonymList(value))
        print("Changed query: {}\nto:{}".format(value, newQuery))
        # Get search values and display to user
        result = searcher.searchWithTerm(newQuery
        )
        for res in result:
            ixreader = IndexSearcher(searcher.reader)
            doc = ixreader.doc(res.doc)
            text = doc.get("content")
            author = doc.get("author")
            title = doc.get("title")
            score = res.score

            print("title: {0}author: {1}score: {2}\n".format(title,author,score))