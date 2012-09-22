#! /usr/bin/env python
import cgi, cgitb
print "Content-type:text/html\r\n\r\n"

form = cgi.FieldStorage() 
docid = form.getvalue('document')

print "<html>"
print "<head>"
print "<title>document %s</title>" %docid
print "</head>"
print "<body>"
print "<center><h1>Text for document %s</h1></center>" %docid

docid = int(docid)
parsed = open("parseoutputfile1.txt","r").readlines()
queryhashmap = {}
lst = []

for line in parsed:
    if line.startswith(tuple('0123456789')):
        key = int(line)
        lst = []
    else:
        lst.append(line.strip())
        queryhashmap[key] = lst

for key in queryhashmap.keys():
    temp = queryhashmap[key]
    strg = ""
    for elements in temp:
        strg += " " + elements
    queryhashmap[key] = strg.strip()

print "<h4>%s</h4>" %queryhashmap[docid]

print "</body>"
print "</html>"
