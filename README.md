# Social_Network
Big Data project - 4INFO - INSA Rennes

## Using Neo4j with this project
(please go and read text file in the appropriate directory)

Consider use 4 main steps :  

### Change the startup database
If `import.db` is not you default database, you can change it by editing the file `conf/neo4j-server.properties` and modify the line :

```
org.neo4j.server.database.location=path/to/import.db

```

### Make the data from SNAP readable for Neo4j  

You have to run the two scripts `compile` and `run` in order to generate data files in correct format for Neo4j. Please consider change paths in that scripts to make them corresponding to your configuration.  
If you want to change the used dataset, open `Config.java` from `shortestpath-bench` folder. 


### Import the data in Neo4j
In order to use the generated data in you instance of Neo4j server, use the `neo4j-import` command. This command is encapsulated in `import` script. So run that script. 

The data for Neo4j is in `import.db` database.

### Start Neo4j server
When all is ok, you can start Neo4j server by running

	neo4j start


### Run R script
To compute clusters, use the R script `algoR/script.r`.  
With new versions of Neo4j, you can have errors with security measures. If it occurs, please disable login in `conf/neo4j-server.properties`.

### See the result
Run a simple http server with python

	python -m SimpleHTTPServer
	
the web page with the result can be reached at 

	localhost:8000/graph.hmtl
	
It can take a long if there is a lot of nodes to display.

## Bonus ! :)
### Styling graph in Neo4j web browser
It may occur that no information are displayed on nodes in a vizualisation window on Neo4j browser. Indeed, we have no information about nodes, except `ID`.  
To display node `ID` you can modify the style file according to following :

	node {
	  /* what is normally */
	  caption: '{id}'
	}


		