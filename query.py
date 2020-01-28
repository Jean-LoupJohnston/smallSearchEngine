import json
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
    

file1 = open("./index.txt","r")
index = json.load(file1)
file2 = open("./documentFrequencies.txt","r")
docFreq = json.load(file2)
file3 = open("./DocumentLengths.txt","r")
L = json.load(file3)
file4 = open("./termFrequencies.txt","r")
freq = json.load(file4)
file5 = open("./AiTopicsdocumentFrequencies.txt","r")
freqai = json.load(file5)
stopwords = stopwords.words('english')

#bm25 values:
N = 1106
k = 5
b = 0.5
Lavg = 2091

# intersection of 2 lists
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3
#takes list of retrieved docuemnts and a query, returns ranked list of docuemnts
def bm25Rank(docList,query):

    scores = {}
    
    for doc in docList:
        scores[doc] = 0
        for term in query:
           f = 0 # term frequency
           d = 0 # document frequency
           if str(doc)+term in freq:   # make sure document has term
                f= freq[str(doc)+term]

           if term in freqai:   # make sure document frequency exists
                d= freqai[term]
                
           if term in docFreq:   
                d= docFreq[term]
               
           else:
               scores[doc] =0;
               continue
           temp = (N/d)
           
           scores[doc] += math.log(temp,10)* (((k+1)*f)/(k*((1-b)+b*(L[doc]/Lavg))+f))       
    return sorted(scores, key=scores.get, reverse=True)#return scores dictionary sorted by value

#takes list of retrieved docuemnts and a query, returns ranked list of docuemnts
def tfidfRank(docList,query):

    scores = {}
    
    for doc in docList:
        scores[doc] = 0
        for term in query:
           f = 0 # term frequency
           d = 0 # document frequency
           if str(doc)+term in freq:   # make sure document has term
                f= freq[str(doc)+term]
                
           if term in docFreq:   # make sure document frequency exists
                d= docFreq[term]
               
           else:
               scores[doc] =0;
               continue
           
           scores[doc] += (f/L[doc])*(math.log(N/docFreq[term],10))   
    return sorted(scores, key=scores.get, reverse=True)#return scores dictionary sorted by value
    
# implementation of AND query for n terms in 'q'
def ANDquery(q):
    words = q
    lists = []
    for word in words:
         if word in index:
            lists.append(index[word])
         else:
             return ""

    numLists = len(lists)

    for i in range(numLists):#intersection on i lists
        lists[0] = intersection(lists[0],lists[i])
        
    return lists[0]
# implementation of OR query for n terms in 'q'
def ORquery(q):
    words = q
    ORdict = {}

    if not words:
        return ""
    
    for word in words:
         if word in index:
            for doc in index[word]:
                if doc not in ORdict:
                    ORdict[doc]= 1
                else:
                    ORdict[doc] = ORdict[doc]+1

    return sorted(ORdict, key=lambda x: ORdict[x],reverse = True)


 # take user input and query   
while(True):                   
    
    topk = int(input("Select how many results to display: "))
    
# process the input the same way as the documents, then query
    while(True):
            inp = input("Enter a query : ").lower()
            inp = ''.join(c for c in inp if not c.isdigit())
            inp = word_tokenize(inp)
            inp = [w for w in inp if not w in stopwords]
            count = 1
            # bm25 ranking
            print("BM25 ranking:\n")
            for x in bm25Rank(ORquery(inp),inp):
               print(count,x)
               count+=1
               if count == topk+1:# only print out selected number of documents
                   count = 1
                   break
            #tf-idf ranking
            print("\ntf-idf ranking:\n")
            for x in tfidfRank(ORquery(inp),inp):
               print(count,x)
               count+=1
               if count == topk+1:# only print out selected number of documents
                   count = 0
                   break 
            
    else:
        print("Invalid selection")







