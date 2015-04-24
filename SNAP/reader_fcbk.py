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
GraphNEANet = TNEANet.New()
GraphTUN = TUNGraph.New()

#reading file.edges
f = open("414.edges",'r')
print "Creating nodes and edges from the file ...."
for ligne in f.readlines():
	m = re.search(r"([0-9]+) ([0-9]+)", ligne)
	nId = m.group(1)
	if(not GraphNEANet.IsNode(int(nId)) ) :
		GraphNEANet.AddNode(int(nId))
		GraphTUN.AddNode(int(nId))
		
	nId1 = m.group(2)
	if(not GraphNEANet.IsNode(int(nId1))) :
		GraphNEANet.AddNode(int(nId1))
		GraphTUN.AddNode(int(nId1))
			
	if(not GraphNEANet.IsEdge(int(nId),int(nId1))) : 
		GraphNEANet.AddEdge(int(nId),int(nId1))
		GraphTUN.AddEdge(int(nId),int(nId1))
		
f.close()
#print "Graph: Nodes %d, Edges %d" % (Graph.GetNodes(), Graph.GetEdges())

	
	 
#reading file.feat and file.featnames
ficfeat = open("414.feat",'r');
ficfeatnames = open("414.featnames",'r');
print "Adding features to the graph ...."

#creation of the list for the features
list_featnames = []
for line in ficfeatnames.readlines():
	mfeatnames = re.search(r"[0-9]+ ([a-z;_]+;anonymized feature [0-9]+)",line)
	e = mfeatnames.group(1)
	#adding all the features in the list
	list_featnames.append(e)


for element in list_featnames :
	GraphNEANet.AddStrAttrN(str(element), "0")

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
	val = list[0]
	if(GraphNEANet.IsNode(nid)) :
		NI = GraphNEANet.GetNI(nid)
		for i in range(0,length-1) : 
			if(list[i] == "1") :
				if(i<length) : 
					GraphNEANet.AddStrAttrDatN(int(nid), list_featnames[i], str(val))
				else :
					GraphNEANet.AddIntAttrDatN(int(nid), "Unknownfeature", str(val))

print "All features added to the graph"
print "Printing graph ... "
DrawGViz(GraphNEANet, gvlNeato, "414graph.png", "graph 414")
PrintInfo(GraphNEANet, "Python type TNEANet Informations : ")
#Returns strongly connected components
print "Weakly connected components : "
Components = TCnComV()
GetSccs(GraphTUN, Components)
for CnCom in Components:
    print "Size of component: %d" % CnCom.Len()

#Computes the average clustering coefficient as defined in Watts and Strogatz, Collective dynamics of small-world networks
GraphClustCoeff = GetClustCf (GraphTUN, -1)
print "Clustering coefficient: %f" % GraphClustCoeff #0.670292

#Get triads
NumTriads = GetTriads(GraphTUN, 150)
print 'Number of triads with 150 sample nodes: %d' % NumTriads

#The more strongly triadic closure is operating in 
#the neighborhood of the node, the higher the 
#clustering coefficient will tend to be. 

#Test of community detection function given in SNAP
#Uses the Clauset-Newman-Moore community detection method for large networks
CmtyV = TCnComV() #contains the vectors of community
modularity = CommunityGirvanNewman(GraphTUN, CmtyV)
print "Community Detection : The modularity of the network is %f" % modularity #0543082 --> 4 communities

#Studying the communities

#Counting the number of features that the nodes have in common
for Cmty in CmtyV :
	listmap = []
	hashmap = []
	for NI in Cmty : 
		nid = int(NI)
		sval = GraphNEANet.GetStrAttrDatN(nid, str(nid))
		if(listmap.count(sval) == 0) :
			tuple = [sval, 1]
			listmap.append(sval)
			hashmap.append(tuple)
		else : 
			for element in hashmap : 
				if (element[0] == sval) : 
					element[1] = element[1]+1
					
	for e in hashmap :
		print "Community characteristics : "
		print "%s : %d" % (e[0], e[1])
	
	print "\n \n "

#Studying with the features of the ego
ficego = open("414.egofeat",'r');
listfeatego = []
for linego in ficego.readlines():
	s = linego.split(" ")
	list = []
	
	for e in s:
		list.append(e)
	
		length = 0
	for element in list:
		length = length +1
		
	for i in range(0,length-1) : 
		if(list[i] == "1") :
			listfeatego.append(list_featnames[i])
			print "Features of ego :"
			print "%s" % list_featnames[i]
		


ficfeat.close()
ficfeatnames.close()	


