import re
import os				
from snap import *

#download : http://snap.stanford.edu/snappy/
#download datasets : http://snap.stanford.edu/data/egonets-Facebook.html
#documentation : http://snap.stanford.edu/snappy/doc/tutorial/index-tut.html
#test if snap.py work well : http://snap.stanford.edu/snappy/file/quick_test.py
#example of a script : http://snap.stanford.edu/snappy/file/intro.py

#Read the informations stored in the file.edges and for features

	
#create a new graph: TNEANet : Returns a new directed multigraph with node and edge attributes
Graph = TNEANet.New()

#reading file.edges
f = open("0.edges",'r')
print "Creating nodes and edges from the file ...."
for ligne in f.readlines():
	m = re.search(r"([0-9]+) ([0-9]+)", ligne)
	nId = m.group(1)
	if(not Graph.IsNode(int(nId)) ) :
		Graph.AddNode(int(nId))

	nId1 = m.group(2)
	if(not Graph.IsNode(int(nId1))) :
		Graph.AddNode(int(nId1))
			
	if(not Graph.IsEdge(int(nId),int(nId1))) : 
		Graph.AddEdge(int(nId),int(nId1))

f.close()
print "Graph: Nodes %d, Edges %d" % (Graph.GetNodes(), Graph.GetEdges())

	
	 
#reading file.feat and file.featnames
ficfeat = open("0.feat",'r');
ficfeatnames = open("0.featnames",'r');
print "Adding features to the graph ...."

#creation of the list for the features
list_featnames = []
for line in ficfeatnames.readlines():
	mfeatnames = re.search(r"[0-9]+ ([a-z;_]+);anonymized feature ([0-9]+)",line)
	e1 = mfeatnames.group(1)
	e2 = mfeatnames.group(2)
	tuple = [str(e1), int(e2)]
	#adding all the features in the list
	list_featnames.append(tuple)


for element in list_featnames :
	Graph.AddIntAttrN(str(element[0]), int(element[1]))

#Adding features to the nodes
for linef in ficfeat.readlines():
	s = linef.split(" ")
	list = []
	
	for e in s:
		list.append(e)
		
	length = 0
	for element in list:
		length = length +1
		
	nid=int(list[0])
	if(Graph.IsNode(nid)) :
		NI = Graph.GetNI(nid)
		for i in range(1,length) : 
			if(list[i] == "1") :
				if(i<length) : 
					c = list_featnames[i] 
					Graph.AddIntAttrDatN(nid, int(c[1]), str(c[0]))
				else :
					Graph.AddIntAttrDatN(nid, 0, "Unknownfeature")

print "All features added to the graph"

ficfeat.close()
ficfeatnames.close()	

	

