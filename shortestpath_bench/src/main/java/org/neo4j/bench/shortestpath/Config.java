package org.neo4j.bench.shortestpath;

import java.io.IOException;
import java.util.Map;
import java.util.Properties;

public class Config
{
    static
    {
        try
        {
            Map properties = new Properties();
            ( (Properties) properties ).load( Config.class.getResourceAsStream( "/neo4j_config.properties" ) );
            NEO4J_CONFIG = properties;
        }
        catch ( IOException e )
        {
            e.printStackTrace();
        };
    }

    public static Map<String, String> NEO4J_CONFIG;

    public final static String DB_DIR = "db/";

    public final static String RAW_RELATIONSHIP_FILE = "data/raw/facebook/414.edges";

    public final static String NODE_ID_FILE = "data/generated1/nodes.csv";
    public final static String RELATIONSHIP_ID_FILE = "data/generated1/relationships.csv";
    public final static String PATH_START_END_ID_FILE = "data/generated1/path-start-and-end-nodes.csv";
}
