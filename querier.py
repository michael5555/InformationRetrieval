import os, sys, lucene

from java.nio.file import Paths
from java.lang import System
from java.text import DecimalFormat
from java.util import Arrays

from org.apache.lucene.search import IndexSearcher, TermQuery, MatchAllDocsQuery
from org.apache.lucene.store import FSDirectory, SimpleFSDirectory
from org.apache.lucene.index import (IndexWriter, IndexReader,
                                     DirectoryReader, Term,
                                     IndexWriterConfig)

from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
			
INDEX_DIR = "IR.Index"
TEXT = "text"

class SimpleSearcher(object):
    def searchWithTerm(self, query, indexReader):
        """
        Search an index with facets by using simple term query
        return a list of FacetResult instances
        """
        query = TermQuery(Term(TEXT, query))
        return self.searchWithQuery(query, indexReader)

    def searchWithQuery(cls, query, indexReader):
        """
        Search an index with facets for a given query
        return a list of FacetResult instances
        """
        # prepare searcher to search against
        searcher = IndexSearcher(indexReader)
        scoreDocs = searcher.search(query, 50).scoreDocs

        return scoreDocs

		
if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    searchValues = ['is', 'tree', "I", 'love' , 'cars', "I love cars.", '1']
    baseDir = os.path.dirname(os.path.abspath(sys.argv[0]))
	
		
    baseDir = os.path.dirname(os.path.abspath(sys.argv[0]))
    indexDir = FSDirectory.open(Paths.get(os.path.join(baseDir, INDEX_DIR)))
	
    indexReader = DirectoryReader.open(indexDir)

    for term in searchValues:
        print("\nsearch by term '{0}' ...".format(term))
		
        facetRes = SimpleSearcher().searchWithTerm(term, indexReader)
        print(len(facetRes))
        for value in facetRes:
            print(value.doc)

    print("Checking all documents")
    query = MatchAllDocsQuery()
    for result in SimpleSearcher().searchWithQuery(query, indexReader):
        print(result)
    # close readers
    indexReader.close()