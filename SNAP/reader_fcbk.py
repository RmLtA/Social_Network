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
	Graph = TNGraph.New()
	
	#reading fcbk file
	f = open("C:\Users\Rasata Liantsoa\Documents\4INFO\BigData\projet\snap-1.1-2.3-Win-x64-py2.7\snap-1.1-2.3-Win-x64-py2.7\facebook_combined.txt",'r')
	for ligne in f.readlines():
		m = re.search(r"(?P<FromNodeId>\d+) (?P<ToNodeId>\d+)", ligne)
		#fill the graph
		if m is not None:
			Graph.AddNode(FromNodeId)
			Graph.AddNode(ToNodeId)
			Graph.AddEdge(FromNodeId,ToNodeId)
	f.close()
	print "Graph: Nodes %d, Edges %d" % (Graph.GetNodes(), Graph.GetEdges())
	
	#generating the png graph
	#FOut = TFOut("fcbk.graph")
    #Graph.Save(FOut)
    #FOut.Flush()
	#FIn = TFIn("fcbk.graph")
    #GraphPNG = TNGraph.Load(FIn)
    #print "GraphPNG: Nodes %d, Edges %d" % (GraphPNG.GetNodes(), GraphPNG.GetEdges())
	
	snap.DrawGViz(Graph, snap.gvlDot, "graphFCBK.png", "graph 1")
	
	

if __name__ == '__main__':
    reader_info()

