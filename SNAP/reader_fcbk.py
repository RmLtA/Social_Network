import re
import os
from snap import *

#download : http://snap.stanford.edu/snappy/
#download datasets : http://snap.stanford.edu/data/egonets-Facebook.html
#documentation : http://snap.stanford.edu/snappy/doc/tutorial/index-tut.html
#test if snap.py work well : http://snap.stanford.edu/snappy/file/quick_test.py
#example of a script : http://snap.stanford.edu/snappy/file/intro.py

#Read the informations stored in the facebook_combined.txt

def reader_info():	
	#create a new graph
	Graph = TUNGraph.New()

	#reading fcbk file
	f = open("facebook_combined.txt",'r')
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
	
	#generating the png graph
	#FOut = TFOut("fcbk.graph")
    #Graph.Save(FOut)
    #FOut.Flush()
	#FIn = TFIn("fcbk.graph")
    #GraphPNG = TNGraph.Load(FIn)
    #print "GraphPNG: Nodes %d, Edges %d" % (GraphPNG.GetNodes(), GraphPNG.GetEdges())
	
	DrawGViz(Graph, gvlDot, "graphFCBK.png", "graph 1")
	print "Graph Viz generated ... "
	

if __name__ == '__main__':
    reader_info()

