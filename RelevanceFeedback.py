import os, sys, lucene

from java.nio.file import Paths
from java.lang import System
from java.text import DecimalFormat
from java.util import Arrays

from org.apache.lucene.search import IndexSearcher, TermQuery, MatchAllDocsQuery, BoostQuery
from org.apache.lucene.store import FSDirectory, SimpleFSDirectory
from org.apache.lucene.index import (IndexWriter, IndexReader,
                                     DirectoryReader, Term, Terms,
                                     IndexWriterConfig)
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer

from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document

class RelevanceFeedback(object):

    def __init__(self,a,b,c,query,result,reader):
        self.alpha = a
        self.beta = b
        self.gamma = c
        self.orig_query = query
        self.nrRelevant = 3
        (self.relevant,self.nonrelevant) = self.splitTopDocs(result,reader)

    def splitTopDocs(self,result, reader):
        """ get the relevant and non relevant docs"""
        relevant = []
        nonrelevant = []
        ixreader = IndexSearcher(reader)

        for i in result[0:self.nrRelevant - 1]:
            relevant.append(ixreader.doc(i.doc))

        for i in result[self.nrRelevant:]:
            nonrelevant.append(ixreader.doc(i.doc))

        return (relevant,nonrelevant)

    def calculateAlphaQuery(self):
        bq = BoostQuery(self.orig_query,self.alpha)
        return bq

    def calculateSumRelevant(self,reader):
        ixreader = IndexSearcher(reader)
        alldocstermsfreqs = []
        for i in self.relevant:
            doctermsfreqs = []
            terms = ixreader.getTermVector(i.id,"content")
            itr = terms.iterator(0)
            while itr.next():
                post = itr.postings()
                freq = post.freq()
                doctermsfreqs.append(freq)
            alldocstermsfreqs.append(doctermsfreqs)



    def calculateSumNonRelevant(self,reader):
        ixreader = IndexSearcher(reader)
        alldocstermsfreqs = []
        for i in self.nonrelevant:
            doctermsfreqs = []
            terms = ixreader.getTermVector(i.id,"content")
            itr = terms.iterator(0)
            while itr.next():
                post = itr.postings()
                freq = post.freq()
                doctermsfreqs.append(freq)
            alldocstermsfreqs.append(doctermsfreqs)

    def expandQuery(self):
        pass



        

    