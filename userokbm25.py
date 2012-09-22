#!/usr/bin/env python
#calcuating the score using okapi-BM25 retrieval scheme for given query.
from math import log
from porterStemmer import PorterStemmer
from collections import defaultdict,OrderedDict
import sys
import cgi, cgitb
form = cgi.FieldStorage() 
query = form.getvalue('query')

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Kedar's CACM search Engine</title>"
print "</head>"
print "<body>"
print "<center><h1>CACM Search Results</h1></center>"
queryhashmap = {}

queryhashmap[1] = query.split()   

stop = open("common_words","r").read().split()

for key in queryhashmap.keys():
    temp = queryhashmap[key]
    strg = ""
    for elements in temp:
        strg += " " + elements

    punc1 = [",","-","=","/","'",";","^","+","|",":","<",">","`","&","(",")"]
    punc2 = [".",'"',"[","]","?","!","*","%","{","}"]
    for punc in punc1:
       if punc in strg:
          strg = strg.replace(punc," ")
    for punc in punc2:
       if punc in strg:
          strg = strg.replace(punc,"")
    
    strg = strg.split()
    finallist = [x for x in strg if x not in stop]
    p = PorterStemmer()
    midlist = [(p.stem(word, 0, len(word)-1)) for word in finallist]
    newlist = [x for x in midlist if x not in stop]
    finalstring = ''.join(" " + x for x in newlist)
   
    queryhashmap[key] = finalstring.strip()

avgdoclen = 46.25
#avgdoclen = 46.2484394507 #zipfs avgdoclen

def calcOBM25(OBM25dict,docid,doclen,termfreq,df):
    b = 0.6 #0.2-1.0
    k = 1.6 #1.2-2.0
    idf = log(3204.0/df)
    numerator = termfreq * float(k+1.0)
    denominator = termfreq + k*(1.0 - b + (b*doclen)/avgdoclen)
    score = idf * (numerator/denominator)
    if OBM25dict.has_key(docid):
        OBM25dict[docid] = OBM25dict[docid] + score
    else:
        OBM25dict[docid] = score
    return OBM25dict


def printOBM25(OBM25dict):
    i = 1
    finalresult = OrderedDict(sorted(OBM25dict.items(),key=lambda t: t[1],reverse=True)).items()
    for docid,value in finalresult:
        if i < 11: 
            print "<center><h4><a href='snippet.py?document=%s'>%s</a> %s %s<h4></center>" %(docid,"CACM-"+str(docid),i,value) 
            i += 1


OBM25dict = {}
querywordcount = defaultdict(float)
file1 = open("file1","r").readlines()

for key in queryhashmap.keys():
    query = queryhashmap[key].split()
    querydict = {}
    #for term in query:
    #    querywordcount[term] += 1
    #for words in querywordcount.keys():
    #    querydict[words] = querywordcount[words]/(querywordcount[words] + 0.5 + 1.5*float(len(querywordcount.keys())))
    use = {}
    for term in query:
        ctf = 0 
        for line in file1:
            line = line.split()
            if term==line[0]:
                termid = line[1]
                startoffset = int(line[2])
                endoffset = int(line[3])
                df = float(line[5])
                file2 = open("file2","r")
                for i,line in enumerate(file2):
                   if(i>=(startoffset-1) and i<endoffset):
                      line = line.strip()
                      line = line.split()
                      docid = int(line[2])
                      termfreq = int(line[3])
                      doclen = int(line[4])
                      use[i]=(term,docid,doclen,termfreq)
                      ctf += termfreq
                for keys,values in use.items():
                    OBM25dict = calcOBM25(OBM25dict,values[1],values[2],values[3],df)
                use.clear()
                file2.close()
            else:
               pass

    printOBM25(OBM25dict)
    OBM25dict.clear()


print "</body>"
print "</html>"
