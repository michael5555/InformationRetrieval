import os, sys, lucene

from org.apache.lucene.store import FSDirectory, SimpleFSDirectory
from org.apache.lucene.index import (IndexWriter, IndexReader,
                                     DirectoryReader, Term,
                                     IndexWriterConfig)
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer

from org.apache.lucene.queryparser.classic import QueryParser,MultiFieldQueryParser
from org.apache.lucene.queryparser.simple import SimpleQueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer

from org.apache.lucene.document import Document
from org.apache.lucene.queries.mlt import MoreLikeThis
from java.io import StringReader

from org.apache.lucene.search import IndexSearcher, TermQuery, MatchAllDocsQuery,BooleanQuery,BooleanClause

from java.nio.file import Paths
from java.lang import System
from java.text import DecimalFormat
from java.util import Arrays

class Querrier(object):

    def __init__(self, baseDir, indexDirectory="IR.Index"):
        """
        :param baseDir: The directory where this querrier is run
        :param indexDirectory: Directory of indices, default value = 'IR.Index'
        """
        indexDir = FSDirectory.open(Paths.get(os.path.join(baseDir, indexDirectory)))

        self.reader = DirectoryReader.open(indexDir)

    def searchWithTerm(self, query):

        query2 = query
        analyzer = LimitTokenCountAnalyzer(StandardAnalyzer(), 1048576)
        query = SimpleQueryParser(analyzer, "content").parse(query)
        qstring = query.toString()

        query2 = SimpleQueryParser(analyzer, "title").parse(query2)
        qstring2 = query2.toString()

        mfqp = MultiFieldQueryParser(["title","content"],analyzer)
        query = mfqp.parse([qstring2,qstring],["title","content"],analyzer)
        return self.searchWithQuery(query)

    def searchWithTermSingle(self, query):

        analyzer = LimitTokenCountAnalyzer(StandardAnalyzer(), 1048576)
        query = SimpleQueryParser(analyzer, "content").parse(query)
        return self.searchWithQuery(query)

    def searchWithSynonyms(self, oldquery,newquery):

        analyzer = LimitTokenCountAnalyzer(StandardAnalyzer(), 1048576)
        newquery = SimpleQueryParser(analyzer, "content").parse(newquery)
        newqstring = newquery.toString()

        oldquery = SimpleQueryParser(analyzer, "title").parse(oldquery)
        oldqstring = oldquery.toString()

        mfqp = MultiFieldQueryParser(["title","content"],analyzer)
        query = mfqp.parse([oldqstring,newqstring],["title","content"],analyzer)
        return self.searchWithQuery(query)

    def searchWithRelevanceFeedback(self, oldquery,newquery):

        analyzer = LimitTokenCountAnalyzer(StandardAnalyzer(), 1048576)
        """newquery = SimpleQueryParser(analyzer, "content").parse(newquery)
        newqstring = newquery.toString()"""

        oldquery = SimpleQueryParser(analyzer, "title").parse(oldquery)
        oldqstring = oldquery.toString()

        mfqp = MultiFieldQueryParser(["title","content"],analyzer)
        query = mfqp.parse([oldqstring,newquery],["title","content"],analyzer)
        return self.searchWithQuery(query)

    def searchWithQuery(self, query):

        # prepare searcher to search with
        searcher = IndexSearcher(self.reader)
        scoreDocs = searcher.search(query, 10).scoreDocs

        return scoreDocs

    def expandQuery(self,oldquery, result, nrRelevant):
        #searcher = IndexSearcher(self.reader)
        analyzer = LimitTokenCountAnalyzer(StandardAnalyzer(), 1048576)

        relevant = []
        mlt = MoreLikeThis(self.reader)
        mlt.setAnalyzer(analyzer)
        for i in result[:nrRelevant]:
            doc = self.reader.document(i.doc)
            sr = StringReader(doc.get("content"))
            relevant.append(sr)

        mltquery = mlt.like("content", relevant)
        mltqstring = mltquery.toString()
        return self.searchWithRelevanceFeedback(oldquery,mltqstring)
        """scoreDocs = searcher.search(mltquery, 10).scoreDocs
        return scoreDocs"""
