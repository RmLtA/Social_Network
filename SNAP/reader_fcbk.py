import re
import os
import time				
from snap import *

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
	
def GirvanNewmanModularity(G):
	Nodes = TIntV()
	for nodeId in G.Nodes():
		Nodes.Add(nodeId.GetId())

	Mod = GetModularity(G, Nodes, G.GetEdges())
	return Mod
