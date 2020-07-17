# smallSearchEngine
Uses crawled website data to perform ranked queries, specificaly for searches queries to artificial intelligence. 
The code also uses a list of ai related to terms from aitopics.com to stengthen searches related to ai. 
# Requirements 
- pip install nltk
- python -m nltk.downloader stopwards
- python -m nltk.downloader punkt
# Usage

indexer.py goes through the crawled data and created an index. T
AitopicsIndexer.py indexes the ai terms, which will be used in the ranking.
The files have already been indexed.
Run query.py to perform ranked searches on the index.
