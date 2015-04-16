package org.neo4j.bench.shortestpath;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Iterator;
import java.util.NoSuchElementException;
import java.util.regex.Pattern;

import org.apache.log4j.Logger;

public class CsvFileReader implements Iterator<String[]>
{
    private static final Logger logger = Logger.getLogger( CsvFileReader.class );
    private final Pattern columnSeparatorPattern;

    private final BufferedReader csvReader;

    private String[] next = null;
    private boolean closed = false;

    public CsvFileReader( File csvFile ) throws FileNotFoundException
    {
        this( csvFile, "\\ " );
    }

    public CsvFileReader( File csvFile, String regexSeparator ) throws FileNotFoundException
    {
        this.csvReader = new BufferedReader( new FileReader( csvFile ) );
        this.columnSeparatorPattern = Pattern.compile( regexSeparator );
    }

    @Override
    public boolean hasNext()
    {
        if ( true == closed ) return false;
        next = ( next == null ) ? nextLine() : next;
        if ( null == next ) closed = closeReader();
        return ( null != next );
    }

    @Override
    public String[] next()
    {
        next = ( null == next ) ? nextLine() : next;
        if ( null == next ) throw new NoSuchElementException( "No more lines to read" );
        String[] tempNext = next;
        next = null;
        return tempNext;
    }

    @Override
    public void remove()
    {
        throw new UnsupportedOperationException();
    }

    private String[] nextLine()
    {
        String csvLine = null;
        try
        {
            csvLine = csvReader.readLine();
            if ( null == csvLine ) return null;
            return parseLine( csvLine );
        }
        catch ( IOException e )
        {
            String errMsg = String.format( "Error retrieving next csv entry from file [%s]", csvReader );
            logger.error( errMsg, e );
            throw new RuntimeException( errMsg, e.getCause() );
        }
    }

    private String[] parseLine( String csvLine )
    {
        return columnSeparatorPattern.split( csvLine, -1 );
    }

    private boolean closeReader()
    {
        if ( true == closed )
        {
            String errMsg = "Can not close file multiple times";
            logger.error( errMsg );
            throw new RuntimeException( errMsg );
        }
        if ( null == csvReader )
        {
            String errMsg = "Can not close file - reader is null";
            logger.error( errMsg );
            throw new RuntimeException( errMsg );
        }
        try
        {
            csvReader.close();
        }
        catch ( IOException e )
        {
            String errMsg = String.format( "Error closing file [%s]", csvReader );
            logger.error( errMsg, e );
            throw new RuntimeException( errMsg, e.getCause() );
        }
        return true;
    }
}
