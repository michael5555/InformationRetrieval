import os, sys, lucene

from java.nio.file import Paths
from java.lang import System
from java.text import DecimalFormat
from java.util import Arrays

from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer

from org.apache.lucene.search import IndexSearcher, TermQuery, MatchAllDocsQuery
from org.apache.lucene.store import FSDirectory, SimpleFSDirectory
from org.apache.lucene.index import (IndexWriter, IndexReader,
                                     DirectoryReader, Term,
                                     IndexWriterConfig, IndexOptions)
from org.apache.lucene.document import Document, Field, TextField, FieldType



"""Creates an indexer."""

INDEX_DIR = "IR.Index"

class Indexer(object):

    def __init__(self, indexDir):
        # create and open an index writer
        indexDir = FSDirectory.open(Paths.get(indexDir))

        root = "testdocs"

        # TODO make appropriate analyzer add to config
        analyzer = LimitTokenCountAnalyzer(StandardAnalyzer(), 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        iw = IndexWriter(indexDir, config)

        self.indexDocs(root,iw)

    def indexDocs(self, root, iw):

        t1 = FieldType()
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

        t2 = FieldType()
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        for filename in os.listdir(root):
            if not filename.endswith('.txt'):
                print("file is not a txt file. we skip it.")
                continue
            print("adding", filename)
            path = os.path.join(root,filename)
            file = open(path)
            contents = file.read()
            file.close()
            doc = Document()
            doc.add(Field("name", filename, t1))
            doc.add(Field("path", root, t1))
            if len(contents) > 0:
                doc.add(Field("contents", contents, t2))
            else:
                print("warning: no content in %s" % filename)
            iw.addDocument(doc)

if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    Indexer(os.path.join(base_dir, INDEX_DIR))


