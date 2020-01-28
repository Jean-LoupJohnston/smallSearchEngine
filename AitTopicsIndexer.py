from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
from bs4 import BeautifulSoup
import json


positionalNum = 0
dictionary = {}
docNumber = 0
termFrequencies = {}
docLengths = {}
docLength = 0


#get list of ai terms 
fai= open(".\\aiterms.txt", "r")
aiTerms = word_tokenize(fai.read())

# go through all sgm files in reuters corpus
# insert path to reuters below
for root, dirs, files in os.walk(".\\aitopics\\","r"):

    for file in files: 
     #if file.endswith('.html'):
       f = open(os.path.join(root,file), errors='ignore')
       
       soup = BeautifulSoup(f, 'html.parser')

#open each file, remove unneeded tags, tokenize,remove #s,case fole, remove aiterms
       text = soup.get_text()
       text = ''.join(c for c in text if not c.isdigit())
       text = text.lower()
       text = word_tokenize(text)
       text = [w for w in text if  w in aiTerms] 
       positionalNum += len(text)
       i =0;

       
       docNumber += 1
       docLength = 0
       
# go through data, add tokens to dictionary. Count article number. 
       while i <= len(text)-1:
           docLength += 1
               
           if text[i] not in dictionary.keys():
               dictionary[text[i]] = [os.path.join(root,file)]
            
           elif os.path.join(root,file) not in dictionary[text[i]]:
               dictionary[text[i]].append(os.path.join(root,file))
 
           
           if str(os.path.join(root,file))+text[i] not in termFrequencies.keys():
               termFrequencies[os.path.join(root,file)+text[i]]=1  # keep dictionary of docId concatenated with the term, and frequency
           else:
               termFrequencies[os.path.join(root,file)+text[i]] += 1
               
               
           i += 1
           
       docLengths[os.path.join(root,file)] = docLength # keep track of document lengths
       f.close()

# get document frequency of terms
freq = {}
for term in dictionary:
    freq[term] = len(dictionary[term])
    
# write final dictionary to disk
diskWrite= open("./AiTopicsdocumentFrequencies.txt","w+") # write docFrequencies to disk
diskWrite.write(json.dumps(freq))

diskWrite.close()

#find average doc length
total = 0
for l in docLengths:
    total += docLengths[l]

print ("Avergage doc length:{}".format(total/len(docLengths)))
print ("Number of docs:{}".format(len(docLengths)))


    





