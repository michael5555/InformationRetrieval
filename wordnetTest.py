import lucene
from java.io import StringReader, Reader
from org.apache.lucene.analysis.synonym import WordnetSynonymParser

from org.apache.lucene.analysis.core import WhitespaceAnalyzer,  FlattenGraphFilter
from org.apache.lucene.analysis.standard import StandardTokenizer
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
from org.apache.lucene.analysis.synonym import SynonymGraphFilter, SynonymMap
from org.apache.lucene.util import CharsRef

lucene.initVM(vmargs=['-Djava.awt.headless=true'])


class Synonyms:

    def __init__(self, analyser=WhitespaceAnalyzer(), file="prolog/wn_s.pl"):

        self.parser = WordnetSynonymParser(True, True, analyser)

        # Read the prolog-file for wordnet in a stringreader
        PlFile = StringReader(open(file, 'r').read())

        # Parse the prologfile with the WordnetSynonymParser
        self.parser.parse(PlFile)

        # Build the synonymmap
        self.map = self.parser.build()

    def getSynonyms(self, query, tokenizer = StandardTokenizer()):
        '''
        :param query: The query for which to get synonyms
        :param tokenizer: The tokenizer used for synonymgraphfilter
        :return: A tokenStream with the synonyms
        '''

        # Add query to tokenizer
        tokenizer.setReader(StringReader(query))

        # Use synonymfilter to generate synonyms & flatten to get words from graph
        synGraph = SynonymGraphFilter(tokenizer, self.map, True)
        return FlattenGraphFilter(synGraph)

    def getSynonymList(self, query):
        '''
        :param query: The query for which to get synonyms
        :return: Synonyms in list format
        '''
        resultList = []
        syns = self.getSynonyms(query)

        charTermAttrib = syns.getAttribute(CharTermAttribute.class_)
        syns.reset()

        while syns.incrementToken():
            resultList.append(charTermAttrib.toString())

        return resultList

if __name__ == '__main__':
    text = "catcher, spatter"

    # Use the default whitespaceanalyzer
    analyser = WhitespaceAnalyzer()

    # WordnetSynonymparser with whitespaceanalyzer
    parser = WordnetSynonymParser(True, True, analyser)

    # Read the prolog-file for wordnet in a stringreader
    PlFile = StringReader(open("prolog/wn_s.pl", 'r').read())

    # Parse the prologfile with the WordnetSynonymParser
    parser.parse(PlFile)

    # Build the synonymmap
    map = parser.build()

    test = Synonyms()

    print(test.getSynonymList(text))
