import re
import os
import time
from reader_fcbk import createTUNGraph				
from snap import *

#Run community detection algo

if __name__ == "__main__":
	fic = "3980.edges"
	GraphTUN1 = createTUNGraph(fic)
	GraphTUN2 = createTUNGraph(fic)
	
	t1 = time.time()
	
	CmtyV = TCnComV() #contains the vectors of community
	#run GirvanNewman Algorithm
	modularity = CommunityGirvanNewman(GraphTUN1, CmtyV)
	t2 = time.time() - t1
	length = 0
	for element in CmtyV:
		length = length +1
	
	print "Girvan-Newman Algo"
	print "Communities detected : %d"%length
	print "The modularity of the network is %f" % modularity 	
	print "Execution time : %f\n" %t2
	
	t1 = time.time()
	
	CmtyV = TCnComV() #contains the vectors of community
	#run CNM Algorithm
	modularity = CommunityCNM(GraphTUN2, CmtyV)
	t2 = time.time() - t1
	
	length = 0
	for element in CmtyV:
		length = length +1
	
	print "Clauset-Newman-Moore Algo"
	print "Communities detected : %d"%length
	print "The modularity of the network is %f" % modularity 
	print "Execution time : %f" %t2