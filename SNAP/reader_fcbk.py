import re
import os
import time				
from snap import *


#Implementation	of Girvan-Newman algorithm
def AlgoGirvanNewmanStep(G):
	Components = TCnComV()
	GetSccs(G, Components)
	init_ncomp = Components.Len()
	ncomp = init_ncomp
	
	while (ncomp <= init_ncomp):
		Nodes = TIntFltH()
		Edges = TIntPrFltH()
		
		GetBetweennessCentr(G, Nodes, Edges, 1.0)
        #find the edge with max centrality
		max= 0.0 
		for edge in Edges : 
			if Edges[edge] > max :
				max= Edges[edge]
		for e in Edges : 
			if (float(Edges[e]) == max) :
				G.DelEdge(e.GetVal1(),e.GetVal2())
		Cmp = TCnComV()
		GetSccs(G,Cmp)
		ncomp = Cmp.Len()
		#print "init : %d current : %d" %(init_ncomp,ncomp)
	

def GirvanNewmanModularity(G):
	Nodes = TIntV()
	for nodeId in G.Nodes():
		Nodes.Add(nodeId.GetId())

	Mod = GetModularity(G, Nodes, G.GetEdges())
	return Mod
	

def runGirvanNewman(GraphTUN,GraphNEANet):
    #let's find the best split of the graph
	BestQ = 0.0
	Q = 0.0
	BestComps = TCnComV()
	while True:    
		AlgoGirvanNewmanStep(GraphTUN)
		Q = GirvanNewmanModularity(GraphNEANet) #!!!!!ERROR 
		#print "current modularity: %f" % Q
		if Q > BestQ:
			BestQ = Q
			GetSccs(GraphTUN, BestComps)  #Best Split
			print "comps:"
           #print Bestcomps
		if GraphTUN.GetEdges() == 0:
			break
	print "Running GirvanNewman finished"
	if BestQ > 0.0:
		print "Best Q: %f" % BestQ
		for Cmty in BestComps:
			print "Community: "
			for NI in Cmty:
				print NI
	else:
		print "Best Q: %f" % BestQ


def createTNEANetGraph(File):
	Graph = TNEANet.New()
	
	f = open(File,'r')
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
	return Graph
	
def createTUNGraph(File):
	GraphTUN = TUNGraph.New()
	
	f = open(File,'r')
	print "Creating nodes and edges from the file ...."
	for ligne in f.readlines():
		m = re.search(r"([0-9]+) ([0-9]+)", ligne)
		nId = m.group(1)
		if(not GraphTUN.IsNode(int(nId))) :
			GraphTUN.AddNode(int(nId))
			
		nId1 = m.group(2)
		if(not GraphTUN.IsNode(int(nId1))) :
			GraphTUN.AddNode(int(nId1))
			
		if(not GraphTUN.IsEdge(int(nId),int(nId1))) : 
			GraphTUN.AddEdge(int(nId),int(nId1))
			
	f.close()
	return GraphTUN

def addAttributes(FeatFile, FeatNamesFile, GraphTNEANet):
	#reading file.feat and file.featnames
	ficfeat = open(FeatFile,'r');
	ficfeatnames = open(FeatNamesFile,'r');
	print "Adding features to the graph ...."

	#creation of the list for the features
	list_featnames = []
	for line in ficfeatnames.readlines():
		mfeatnames = re.search(r"[0-9]+ ([a-z;_]+;anonymized feature [0-9]+)",line)
		e = mfeatnames.group(1)
		#adding all the features in the list
		list_featnames.append(e)


	for element in list_featnames :
		GraphTNEANet.AddStrAttrN(str(element), "0")

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
		if(GraphTNEANet.IsNode(nid)) :
			NI = GraphTNEANet.GetNI(nid)
			for i in range(0,length-1) : 
				if(list[i] == "1") :
					if(i<length) : 
						GraphTNEANet.AddStrAttrDatN(int(nid), list_featnames[i], str(val))
					else :
						GraphTNEANet.AddIntAttrDatN(int(nid), "Unknownfeature", str(val))

	print "All features added to the graph"
	ficfeat.close()
	ficfeatnames.close()
	return GraphTNEANet
	

	
if __name__ == "__main__":
	#create a new graph: TNEANet : Returns a new directed multigraph with node and edge attributes
	#GraphTNEANet = createTNEANetGraph("414.edges")
	#create an undirected graph
	listfic=["0.edges","107.edges","348.edges","414.edges","686.edges","698.edges","1684.edges","1912.edges","3437.edges","3980.edges"]
	
	#for i in range(1,9) :
	
	i=5
	print str(listfic[i])
	GraphTUN = createTUNGraph(str(listfic[i]))
	print "Graph: Nodes %d, Edges %d" % (GraphTUN.GetNodes(), GraphTUN.GetEdges())
	print "Printing graph ... "
	DrawGViz(GraphTUN, gvlNeato, str(listfic[i])+".png", "graph"+str(listfic[i]))
	t1 = time.time()
	
	#Test of community detection function given in SNAP
	#Uses the Girvan-Newmann community detection method for large networks
	CmtyV = TCnComV() #contains the vectors of community
	modularity = CommunityGirvanNewman(GraphTUN, CmtyV)
	t2 = time.time() - t1
	print "Execution time : %f" %t2
	length = 0
	for element in CmtyV:
		length = length +1
		
	print "Communities detected : %d"%length
	print "The modularity of the network is %f" % modularity 	

	#Adding features to the graph (TNEANet)
	#GraphTNEANet = addAttributes("414.feat", "414.featnames", GraphTNEANet)

	
	#labels = TIntStrH()
	#for NI in GraphNEANet.Nodes():
	#	labels[NI.GetId()] = str(NI.GetId())
	#DrawGViz(GraphTNEANet, gvlNeato, "414graph.png", "graph 414 Net")
	#PrintInfo(GraphTNEANet, "Python type TNEANet Informations : ")
	
	

	
	#Returns strongly connected components
	#print "Weakly connected components : "
	#Components = TCnComV()
	#GetSccs(GraphTUN, Components)
	#print "Number of connected components : %d" %Components.Len()
	#for CnCom in Components:
	#   print "Size of component: %d" % CnCom.Len()

	#Computes the average clustering coefficient as defined in Watts and Strogatz, Collective dynamics of small-world networks
	#GraphClustCoeff = GetClustCf (GraphTUN, -1)
	#print "Clustering coefficient: %f" % GraphClustCoeff #0.670292

	#Get triads
	#NumTriads = GetTriads(GraphTUN, 150)
	#print 'Number of triads with 150 sample nodes: %d' % NumTriads
	
	#Running algo Girvan Newman
	#print "Running algo Girvan Newmann lookiing for communities ...."
	#runGirvanNewman(GraphTUN,GraphNEANet)

	#The more strongly triadic closure is operating in 
	#the neighborhood of the node, the higher the 
	#clustering coefficient will tend to be. 

	#Test of community detection function given in SNAP
	#Uses the Girvan-Newmann community detection method for large networks
	#CmtyV = TCnComV() #contains the vectors of community
	#modularity = CommunityGirvanNewman(GraphTUN, CmtyV)
	#print "Community Detection : The modularity of the network is %f" % modularity 

	#Studying the communities

	#Counting the number of features that the nodes have in common
	#for Cmty in CmtyV :
	#	listmap = []
	#	hashmap = []
	#	for NI in Cmty : 
	#		nid = int(NI)
	#		sval = GraphNEANet.GetStrAttrDatN(nid, str(nid))
	#		if(listmap.count(sval) == 0) :
	#			tuple = [sval, 1]
	#			listmap.append(sval)
	#			hashmap.append(tuple)
	#		else : 
	#			for element in hashmap : 
	#				if (element[0] == sval) : 
	#					element[1] = element[1]+1
	#					
	#	for e in hashmap :
	#		print "Community characteristics : "
	#		print "%s : %d" % (e[0], e[1])
		
	#	print "\n \n "

	#Studying the features of the ego
	#ficego = open("414.egofeat",'r');
	#listfeatego = []
	#for linego in ficego.readlines():
	#	s = linego.split(" ")
	#	list = []
		
	#	for e in s:
	#		list.append(e)
		
	#		length = 0
	#	for element in list:
	#		length = length +1
			
	#	for i in range(0,length-1) : 
	#		if(list[i] == "1") :
	#			listfeatego.append(list_featnames[i])
	#			print "Features of ego :"
	#			print "%s" % list_featnames[i]
			



