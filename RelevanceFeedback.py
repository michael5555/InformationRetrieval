import os, sys, lucene
from math import log

from java.nio.file import Paths
from java.lang import System
from java.text import DecimalFormat
from java.util import Arrays

from org.apache.lucene.search import IndexSearcher, TermQuery, MatchAllDocsQuery,BooleanQuery,BooleanClause
from org.apache.lucene.store import FSDirectory, SimpleFSDirectory
from org.apache.lucene.index import (IndexWriter, IndexReader,
                                     DirectoryReader, Term, Terms,
                                     IndexWriterConfig)
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer

from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document
from org.apache.lucene.queries.mlt import MoreLikeThis

"""class RelevanceFeedback(object):

    def __init__(self,a,b,c,query,result,reader):
        self.alpha = a
        self.beta = b
        self.gamma = c
        self.orig_query = query
        self.nrRelevant = 3
        (self.relevant,self.nonrelevant) = self.splitTopDocs(result,reader)

    def splitTopDocs(self,result, reader):
        
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
        totalidfvec = []
        for i in self.relevant:
            idfvec = []
            doctermsfreqs = []
            terms = ixreader.getTermVector(i,"content")
            itr = terms.iterator(0)
            while itr.next():
                post = itr.postings()
                tf = post.freq() ** 0.5
                if tf > 0:
                    idfvec.append(1)
                else:
                    idfvec.append(0)
                doctermsfreqs.append(tf)
            alldocstermsfreqs.append(doctermsfreqs)
            totalidfvec.append(idfvec)

        totalidfvec = [sum(x) for x in zip(*totalidfvec)]

        for i in totalidfvec:
            i = float(1 + log(4/i + 1))




    def calculateSumNonRelevant(self,reader):
        ixreader = IndexSearcher(reader)
        alldocstermsfreqs = []
        totalidfvec = []
        for i in self.nonrelevant:
            idfvec = []
            doctermsfreqs = []
            terms = ixreader.getTermVector(i,"content")
            itr = terms.iterator(0)
            while itr.next():
                post = itr.postings()
                tf = post.freq() ** 0.5
                if tf > 0:
                    idfvec.append(1)
                else:
                    idfvec.append(0)
                doctermsfreqs.append(tf)
            alldocstermsfreqs.append(doctermsfreqs)
            totalidfvec.append(idfvec)

        totalidfvec = [sum(x) for x in zip(*totalidfvec)]

        for i in totalidfvec:
            i = float(1 + log(8/i + 1))


        tfidffreqvectors = []
        for it in alldocstermsfreqs:
            itvector = []
            for index in range(len(it)):
                tfidf = it[index] * totalidfvec[index]
                itvector.append(tfidf) """





def expandQuery(ixreader,result,nrRelevant):
    relevant = []
    mlt = MoreLikeThis(ixreader)
    for i in result[0:nrRelevant - 1]:
        docid = ixreader.doc(i.doc)
        relevant.append(mlt.like(docid))

    querybuilder = BooleanQuery.Builder()
    for i in relevant:
        querybuilder.add(i,BooleanClause.Occur.SHOULD)

    return querybuilder.build()
        




        

    