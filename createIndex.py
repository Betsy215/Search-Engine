#!/usr/bin/env python
#file to parse the CACM file, create the intermediate files necessary to create the inverted index and the inverted index itself.
from porterStemmer import PorterStemmer
from collections import defaultdict
import os.path

cacmfile = open("cacm.all", "r").readlines()

parseoutputfile1 = open("parseoutputfile1.txt","w")
print "Parsing cacm.all collection...."
for line in cacmfile:
   if ".I" in line.strip():
       line = line.split()
       parseoutputfile1.write(line[1] +"\n")
   elif ".T" in line:
       pass
   elif ".B" in line:
       pass
   elif ".A" in line:
       pass
   elif ".N" in line:
       pass
   elif ".W" in line:
       pass
   elif ".K" in line:
       pass
   elif ".C" in line:
       pass
   elif ".X" in line:
       pass
   elif line.startswith(tuple('0123456789')):
       pass
   else:
       parseoutputfile1.write(line)
parseoutputfile1.close()

hashmap = {}

cacmparsedfile = open("parseoutputfile1.txt","r").readlines()
lst = []
print "Creating dictionary for the documents...."
for line in cacmparsedfile:
    if line.startswith(tuple('0123456789')):
        key = int(line)
        lst = []
    else:
        lst.append(line.strip().lower())
        hashmap[key] = lst

stop = open("common_words","r").read().split()
print "Processing the text...."
for key in hashmap.keys():
    temp = hashmap[key]
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
    hashmap[key] = finalstring.strip()

idmap = {}
i = 1
print "Giving ID's to words...."
for key in hashmap.keys():
   for value in hashmap[key].split():
      if idmap.has_key(value):
         pass
      else:
         idmap[value] = i
         i += 1

"""
#Unique words:
for key in hashmap.keys():
   temp = hashmap[key].split()
   for value in temp:
      if value not in lst:
         lst.append(value)
      else:
         pass
"""

wordcount = defaultdict(int)
print "writing to small files...."
for key in hashmap.keys():
   temp = hashmap[key].split()
   doclen = len(temp)
   for word in temp:
      wordcount[word] += 1
      
   for word in wordcount.keys():
      #print "processing word: %s ID: %s" %(word,idmap[word])
      if os.path.exists("files/"+word):
         append = open("files/"+word,"a")
         docid = str(key)
         termfreq = str(wordcount[word])
         termid = str(idmap[word])
         doclen = str(doclen)
         append.write(docid)                        
         append.write(" ")
         append.write(termfreq)
         append.write(" ")
         append.write(word)
         append.write(" ")
         append.write(termid)
         append.write(" ")
         append.write(doclen)
         append.write("\n")
         append.close()
      else:
         append = open("files/"+word,"w")
         docid = str(key)
         termfreq = str(wordcount[word])
         termid = str(idmap[word])
         doclen = str(doclen)
         append.write(docid)                        
         append.write(" ")
         append.write(termfreq)
         append.write(" ")
         append.write(word)
         append.write(" ")
         append.write(termid)
         append.write(" ")
         append.write(doclen)
         append.write("\n")
         append.close()
   wordcount.clear()

filenames = os.listdir('files/')
newindex = open("newindex.txt","a")
file2 = open("file2","a")
print "writing file2==>[TermID-DocID-TermFreq]...."
for f in filenames:
   data = open("files/"+f,"r")
   for line in data:
      newindex.write(line)
      line = line.split()
      file2.write(line[3])
      file2.write(" ")
      file2.write(line[2])
      file2.write(" ")
      file2.write(line[0])
      file2.write(" ")
      file2.write(line[1])
      file2.write("\n")
   data.close() 
file2.close()
newindex.close()

doc3 = {}   
file3 = open("file3","a")
print "writing file3==>[DocID-DocName-Doclen]...."
final = open("newindex.txt","r").readlines()
for entry in final:
   entry = entry.split()
   docid = entry[0]
   termfreq = entry[1]
   termid = entry[3]
   doclen = entry[4]
   if doc3.has_key(docid):
      pass
   else:
      file3.write(docid + " " + "CACM-"+docid + " " + doclen + "\n") 
      doc3[docid] = ("CACM-"+docid,doclen)
file3.close()

termdict = defaultdict(list)
termfile = open("file2","r").readlines()
offset = 1
ctf = 1
df = 1
startoffset = 0
file1 = open("file1","a")
print "writing file1==>[Term-TermID-Offset-CTF-DF]...."
for x in xrange(len(termfile)-1):
   line = termfile[x]
   nextline = termfile[x+1]
   line = line.strip()
   line = line.split()
   nextline = nextline.strip()
   nextline = nextline.split()
   nexttermid = nextline[0]
   nextterm = nextline[1]
   termid = line[0]
   term = line[1]
   if(termid == nexttermid):
      offset += 1
      ctf += int(line[3])
      df += 1
   else:
      file1.write(term)
      file1.write(" ")
      file1.write(termid)
      file1.write(" ")
      file1.write(str(offset-df+1))
      file1.write(" ")
      file1.write(str(offset))
      file1.write(" ")
      file1.write(str(ctf))
      file1.write(" ")
      file1.write(str(df))
      file1.write("\n")
      ctf = int(nextline[3])
      df = 1
      offset += 1
      

avgdoclen = 0
for word,doclen in doc3.values():
   avgdoclen += int(doclen)
avgdoclen = avgdoclen/float(len(doc3.keys()))
#print avgdoclen

print "Indexing done...."
