import os, sys, lucene, time
import tqdm
from org.apache.lucene.search import IndexSearcher

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

from querier import Querrier
from synonymGenerator import Synonyms


def scoreResult(title, topDocs, reader):
    '''
    Gives a score for a query result given a title
    :param topDocs: The topdocs returned by a querier
    :param title: The title on which the search was done
    :return:
    '''

    for idx, result in enumerate(topDocs):
        ixreader = IndexSearcher(reader)
        doc = ixreader.doc(result.doc)
        if title == doc.get("title"):
            return 1/(idx+1)

    return 0

if __name__ == '__main__':
    zoek = Querrier(os.path.dirname(os.path.abspath(sys.argv[0])))
    reader = zoek.reader

    titles = open("titles.txt", 'r').readlines()
    synonym = Synonyms()

    basicScore = 0
    basicTime = 0
    synScore = 0
    synTime = 0
    expScore = 0
    expTime = 0
    synexpScore = 0
    count = len(titles)

    print("Testing regular querier ...")
    timeA = time.time()
    for title in tqdm.tqdm(titles):
        results = zoek.searchWithTerm(title)
        basicScore += scoreResult(title, results, reader)

    basicTime = time.time() - timeA


    print("Testing querier with synonym expansion ...")
    timeA = time.time()
    for title in tqdm.tqdm(titles):
        newQuery = " ".join(synonym.getSynonymList(title))
        results = zoek.searchWithSynonyms(title,newQuery)
        synScore += scoreResult(title, results, reader)

    synTime = time.time() - timeA


    print("Testing querier with relevance feedback ...")
    timeA = time.time()
    for title in tqdm.tqdm(titles):
        result = zoek.searchWithTermSingle(title)
        expresult = zoek.expandQuery(title,result, 3)
        expScore += scoreResult(title, expresult, reader)

    expTime = time.time() - timeA

    print("Scores:")
    print("Basic query: {}".format(basicScore / count))
    print("Synonym expansion: {}".format(synScore/count))
    print("Relevance feedback: {}".format(expScore/count))

    print("\nTimes:")
    print("Basic query: {}s : {}s/query".format(basicTime, basicTime/count))
    print("Synonym expansion: {}s : {}s/query".format(synTime, synTime/count))
    print("Relevance feedback: {}s : {}s/query".format(expTime, expTime/count))