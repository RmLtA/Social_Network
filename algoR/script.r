## SCRIPT PROJET BIG DATA
## Utilise la librarie RNeo4j
## Algorithme de Girvan-Newman avec la librairie igraph

## Importation de la librairie
## install.packages("devtools")
## devtools::install_github("nicolewhite/RNeo4j")

## Chargement de la librairie
library(RNeo4j)
## Connexion à la base de graphe
neo4j = startGraph("http://localhost:7474/db/data/")

## Option : donner un label sympa aux nodes (vu qu'ils n'en ont pas avec l'import de neo4j-import)
query = "MATCH (n) SET n:PERSON"
cypher(neo4j,query)

## Requête pour obtenir les nodes 
nodes_query = "
MATCH (n:PERSON)
RETURN DISTINCT ID(n) AS id, ID(n) AS name
"

#nodes_query = "
#MATCH (n:PERSON)
#RETURN DISTINCT ID(n) AS id
#"

edges_query = "
MATCH (n1:PERSON)-[:LINK]->(n2:PERSON)
RETURN ID(n1) as source, ID(n2) as target
"

nodes = cypher(neo4j,nodes_query)
edges = cypher(neo4j,edges_query)

## Clustering
library(igraph)
ig = graph.data.frame(edges, directed = TRUE, nodes)

# Run algo
communities = edge.betweenness.community(ig)

# Extract cluster assignments and merge with nodes data.frame.
memb = data.frame(name = communities$names, cluster = communities$membership)
nodes = merge(nodes, memb)

# Reorder columns.
nodes = nodes[c("id", "name", "cluster")]

nodes_json = paste0("\"nodes\":", jsonlite::toJSON(nodes))
edges_json = paste0("\"edges\":", jsonlite::toJSON(edges))
all_json = paste0("{", nodes_json, ",", edges_json, "}")

sink(file = 'actors.json')
cat(all_json)
sink()

