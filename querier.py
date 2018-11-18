import os, sys, lucene

from java.nio.file import Paths
from java.lang import System
from java.text import DecimalFormat
from java.util import Arrays

from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.search import IndexSearcher, TermQuery, MatchAllDocsQuery
from org.apache.lucene.store import FSDirectory, SimpleFSDirectory
from org.apache.lucene.index import (IndexWriter, IndexReader,
                                     DirectoryReader, Term,
                                     IndexWriterConfig)
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.facet import DrillSideways, DrillDownQuery
from org.apache.lucene.facet import (Facets, FacetField, FacetResult,
                                     FacetsConfig, FacetsCollector)
from org.apache.lucene.facet.taxonomy import FastTaxonomyFacetCounts
from org.apache.lucene.facet.taxonomy.directory import (DirectoryTaxonomyWriter,
                                                        DirectoryTaxonomyReader)