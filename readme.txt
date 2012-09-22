Project on Information Retrieval by Kedar Phadtare

Files/folders in this project:
cacm.all                      contains information about the corpus.
common_words                  contains common words to be filtered (stop words).
portStemmer.pyc               code for stemming of words in corpus.
portStemmer.py		      Obtained from http://tartarus.org/martin/PorterStemmer/python.txt.

createIndex.py                Creates the below mentioned files which form the inverted index for the corpus. (runtime on my machine = 12 secs).
-parseoutputfile1.txt         Contains sanitized version of the word in the corpus cacm.all.
-file1                        Contains the words of the corpus in the form : [Term-TermID-Offset-CTF-DF].
-file2                        Contains the words of the corpus in the form : [TermID-DocID-TermFreq].
-file3                        Contains the words of the corpus in the form : [DocID-DocName-Doclen].
-newindex.txt		      Contains the actual inverted index for the words in the corpus.

webinterface.html             Code for web page with text box for entering query.
userokbm25.py                 Code for processing user entered query and displaying ranked list of documents using Okapi BM25 retrieval model.
                              Shows the first 10 most relevant document names as links.
snippet.py		      Code to display the actual data in the document using the click on the link of the document.

Locations:
The webinterface.html,userokbm25.py,snippet.py,common_words,porterStemmer files along with the generated files (file1,file2,newindex.txt,parseoutputfile1.txt) should be kept in the /usr/lib/cgi-bin folder on a machine to be able to view via browser.
The Inverted Index can be created anywhere on a machine. 
