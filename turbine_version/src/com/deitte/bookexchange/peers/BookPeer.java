package com.deitte.bookexchange.peers;

// Java Core Classes 
import java.util.*;
import java.sql.*;
import java.io.*;

// Turbine Utility Classes
import org.apache.turbine.util.*;
import org.apache.turbine.util.db.*;

// Village Database Classes
import com.workingdogs.village.*;

public class BookPeer extends BasePeer
{
    private static final String BOOK_ID_COLUMN = "BOOKID";
    private static final String TITLE_COLUMN = "TITLE";
    private static final String AUTHOR_COLUMN = "AUTHOR";
    private static final String AREA_ID_COLUMN = "AREAID";
    private static final String CONDITION_ID_COLUMN = "CONDITIONID";
    private static final String ISBN_COLUMN = "ISBN";
    private static final String OTHER_COLUMN = "OTHER";
    private static final String PRICE_COLUMN = "PRICE";
    
    /** The table name for this peer. */
    public static final String TABLE_NAME = "book";

    public static final String BOOK_ID = TABLE_NAME + "." + BOOK_ID_COLUMN;
    public static final String TITLE = TABLE_NAME + "." + TITLE_COLUMN;
    public static final String AUTHOR = TABLE_NAME + "." + AUTHOR_COLUMN;
    public static final String AREA_ID = TABLE_NAME + "." + AREA_ID_COLUMN;
    public static final String CONDITION_ID = TABLE_NAME + "." + CONDITION_ID_COLUMN;
    public static final String ISBN = TABLE_NAME + "." + ISBN_COLUMN;
    public static final String OTHER = TABLE_NAME + "." + OTHER_COLUMN;
    public static final String PRICE = TABLE_NAME + "." + PRICE_COLUMN;

    public static int doInsert(Criteria criteria) throws Exception
    {
        DBConnection db = null;
        TableDataSet tds = null;
        Record rec = null;
        int recNum = -1;
        try
        {
            // get a connection to the db
            db = DBBroker.getInstance().getConnection();
            Connection connection = db.getConnection();

			// the reason for the mess below:
			// since I need to return the actual BOOK_ID for a different
			// class, and since the Village stuff doesn't actually give me
			// this (and there seems to be no way to positively get it)
			// I have to create the Statement myself
            if ( criteria.containsKey ( AREA_ID )
                && criteria.containsKey (CONDITION_ID) )
			{
				String title = null;
            	if ( criteria.containsKey( TITLE ) && 
            		 criteria.getString(TITLE).trim().length() != 0)
					title = criteria.getString(TITLE);
				String author = null;
            	if ( criteria.containsKey( AUTHOR ) &&
            		 criteria.getString(AUTHOR).trim().length() != 0)
					author = criteria.getString(AUTHOR);
				String isbn = null;
            	if ( criteria.containsKey( ISBN ) &&
            		 criteria.getString(ISBN).trim().length() != 0)
				isbn = criteria.getString(ISBN);
				String other = null;
            	if ( criteria.containsKey( OTHER ) &&
            		 criteria.getString(OTHER).trim().length() != 0)
				other = criteria.getString(OTHER);
				String price = null;
            	if ( criteria.containsKey( PRICE ) &&
            		 criteria.getString(PRICE).trim().length() != 0)
				price = criteria.getString(PRICE);
				
				StringBuffer sb = new StringBuffer();

				sb.append("INSERT into ");
				sb.append(TABLE_NAME);

				sb.append(" (");
				sb.append(AREA_ID_COLUMN); sb.append(", ");
				sb.append(CONDITION_ID_COLUMN);
            	if ( title != null )
				{ 	sb.append(", "); sb.append(TITLE_COLUMN); }
            	if ( author != null )
				{	 sb.append(", "); sb.append(AUTHOR_COLUMN); }
            	if ( isbn != null )
				{	 sb.append(", "); sb.append(ISBN_COLUMN); }
            	if ( other != null )
				{	 sb.append(", "); sb.append(OTHER_COLUMN); }
            	if ( price != null )
				{	 sb.append(", "); sb.append(PRICE_COLUMN); }

				sb.append(") VALUES (");

				sb.append(criteria.getInt(AREA_ID)); sb.append(", ");
				sb.append(criteria.getInt(CONDITION_ID));
            	if ( title != null )
				{ 	sb.append(", "); sb.append(title); }
            	if ( author != null )
				{	 sb.append(", "); sb.append(author); }
            	if ( isbn!= null )
				{	 sb.append(", "); sb.append(isbn); }
            	if ( other != null )
				{	 sb.append(", "); sb.append(other); }
            	if ( price != null )
				{	 sb.append(", "); sb.append(price); }
				sb.append(") ");

				/*
                rec.setValue ( AREA_ID_COLUMN, criteria.getInt(AREA_ID) );
                rec.setValue ( CONDITION_ID_COLUMN, criteria.getInt(CONDITION_ID) );
            	if ( criteria.containsKey( TITLE ) )
            		rec.setValue( TITLE_COLUMN, criteria.getString(TITLE) );
            	if ( criteria.containsKey(AUTHOR) )
            		rec.setValue( AUTHOR_COLUMN, criteria.getString(AUTHOR) );
            	if ( criteria.containsKey(ISBN) )
            		rec.setValue( ISBN_COLUMN, criteria.getString(ISBN) );
            	if ( criteria.containsKey(OTHER) )
            		rec.setValue( OTHER_COLUMN, criteria.getString(OTHER) );
            	if ( criteria.containsKey(PRICE) )
            		rec.setValue( PRICE_COLUMN, criteria.getString(PRICE) );
				*/

				Statement s = connection.createStatement();
				recNum = s.executeUpdate(sb.toString());

            }
        }
        finally
        {
            DBBroker.getInstance().releaseConnection(db);
        }
        
        return recNum;
    }

    public static Vector doSelect(Criteria criteria) throws Exception
    {
        DBConnection db = null;
        QueryDataSet qds = null;
        Record rec = null;
        Vector results = null;
        try
        {
            // get a connection to the db
            db = DBBroker.getInstance().getConnection();
            Connection connection = db.getConnection();

            StringBuffer sb = new StringBuffer();
            sb.append ( "SELECT * " );
            sb.append ( " FROM " );
			sb.append (TABLE_NAME);

            qds = new QueryDataSet(connection, sb.toString() );
            qds.fetchRecords();
            int size = qds.size();
            results = new Vector ( size );
            for ( int i = 0; i < size; i++ )
            {
                Object[] tmp = new Object[8];
                tmp[0] = new Integer(qds.getRecord(i).getValue(BOOK_ID_COLUMN).asInt());
                tmp[1] = (String) qds.getRecord(i).getValue(TITLE_COLUMN).asString();
                tmp[2] = (String) qds.getRecord(i).getValue(AUTHOR_COLUMN).asString();
                tmp[3] = new Integer(qds.getRecord(i).getValue(AREA_ID_COLUMN).asInt());
                tmp[4] = new Integer(qds.getRecord(i).getValue(CONDITION_ID_COLUMN).asInt());
                tmp[5] = (String) qds.getRecord(i).getValue(ISBN_COLUMN).asString();
                tmp[6] = (String) qds.getRecord(i).getValue(OTHER_COLUMN).asString();
                tmp[7] = (String) qds.getRecord(i).getValue(PRICE_COLUMN).asString();

                results.addElement ( tmp );
            }

        }
        finally
        {
            qds.close();
            DBBroker.getInstance().releaseConnection(db);
        }
        return results;
	}
}