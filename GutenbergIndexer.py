import os, csv, sys, lucene

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

    def __init__(self, indexDir,root="testdocs"):
        # create and open an index writer
        indexDir = FSDirectory.open(Paths.get(indexDir))

        # TODO make appropriate analyzer add to config
        analyzer = LimitTokenCountAnalyzer(StandardAnalyzer(), 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        iw = IndexWriter(indexDir, config)
        self.authorcount = 0
        self.titlecount = 0
        self.errorcount = 0
        self.indexDocs(root,iw)

    def parseBook(self,filename,t1,t2,iw):
        with open(filename, 'r', errors="ignore") as book:
            lines = book.readlines()
            doc = Document()
            beginindex = endindex = 0
            author = None
            title = None

            for index, text in enumerate(lines):
                if text.startswith("Author:"):
                    author = text[8:]
                    doc.add(Field("author", text[8:], t1))

                if text.startswith("Title: "):
                    title = text[7:]
                    doc.add(Field("title", text[7:], t1))
                elif text.startswith(" Title: "):
                    title = text[8:]
                    doc.add(Field("title", text[8:], t1))

                if text.startswith("*** START OF THIS PROJECT GUTENBERG"):
                    #   extract rest of the text
                    beginindex = index

                if text.startswith("*** END OF THIS PROJECT GUTENBERG"):
                    endindex = index
                    break

            if author == None:
                print("Didnt find author")
                self.authorcount += 1

            if title == None:
                print("Didnt find title")
                self.titlecount += 1

            text = None
            # Check if indices are correct
            if beginindex == 0 or endindex == 0:
                print("Skipping book {}\nSomething went wrong when extracting text".format(filename))
                text = "".join(lines)
                self.errorcount += 1
            else:
                text = "".join(lines[beginindex:endindex])
            doc.add(Field("content", text, t2))

            iw.addDocument(doc)

    def indexDocs(self, root, iw):

        t1 = FieldType()
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

        t2 = FieldType()
        t2.setStored(True)
        t2.setTokenized(True)
        t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        for filename in os.listdir(root):
            if not filename.endswith(".txt"):
                print("file is not a txt file. we skip it.")
                continue
            print("adding", filename)
            path = os.path.join(root,filename)
            self.parseBook(path,t1,t2,iw)

        # Prints a set of statistics displaying missing data
        # Authorerror = number of authors not found
        # Titleerror = number of titles not found
        # Documenterror = number of documents where text could not be extracted so entire document was indexed
        print("AuthorError: {}".format(self.authorcount))
        print("TitleError: {}".format(self.titlecount))
        print("DocumentError: {}".format(self.errorcount))
        iw.close()

if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    if len(sys.argv) == 1:
        Indexer(os.path.join(base_dir, INDEX_DIR))
    else:
        Indexer(os.path.join(base_dir, INDEX_DIR),root=sys.argv[1])


