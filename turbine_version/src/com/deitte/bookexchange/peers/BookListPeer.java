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

public class BookListPeer extends BasePeer
{
    private static final String BOOKLIST_ID_COLUMN = "BOOKLISTID";
    private static final String VISITOR_ID_COLUMN = "VISITORID";
    private static final String BOOK_ID_COLUMN = "BOOKID";
    private static final String CREATED_COLUMN = "CREATED";
    
    /** The table name for this peer. */
    public static final String TABLE_NAME = "booklist";

    public static final String BOOKLIST_ID = TABLE_NAME + "." + BOOKLIST_ID_COLUMN;
    public static final String VISITOR_ID = TABLE_NAME + "." + VISITOR_ID_COLUMN;
    public static final String BOOK_ID = TABLE_NAME + "." + BOOK_ID_COLUMN;
    public static final String CREATED = TABLE_NAME + "." + CREATED_COLUMN;

    public static int doInsert(Criteria criteria) throws Exception
    {
        DBConnection db = null;
        TableDataSet tds = null;
        Record rec = null;
        try
        {
            // get a connection to the db
            db = DBBroker.getInstance().getConnection();
            Connection connection = db.getConnection();

            tds = new TableDataSet(connection, TABLE_NAME );
            rec = tds.addRecord();

            if ( criteria.containsKey ( VISITOR_ID )
                && criteria.containsKey (BOOK_ID) )
			{
                rec.setValue ( VISITOR_ID_COLUMN, criteria.getInt(VISITOR_ID));
                rec.setValue ( BOOK_ID_COLUMN, criteria.getInt(BOOK_ID) );
                                                                  
           		rec.setValue( CREATED_COLUMN, new Timestamp(System.currentTimeMillis()) );

                rec.save();
            }
        }
        finally
        {
            if ( tds != null ) tds.close();
            DBBroker.getInstance().releaseConnection(db);
        }
        
        return -1;
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

            boolean get_area = false;
            boolean get_condition = false;

// not worrying about this right now

/*
            if ( criteria.containsKey ( AREA_ID ) )
                get_area = true;
            else if ( criteria.containsKey ( CONDITION_ID ) )
                get_condition = true;
            StringBuffer sb = new StringBuffer();
            sb.append ( "SELECT " );
            sb.append ( BOOKLIST_ID_COLUMN );
            sb.append ( ", " );
            sb.append ( BOOKLIST_COLUMN );
            sb.append ( " FROM " );
            sb.append ( TABLE_NAME );

// so this isn't really working right now
            if ( criteria.containsKey ( TITLE_COLUMN ) )
            {
                sb.append ( " WHERE " );
                sb.append ( TITLE );
                sb.append ( " = " );
                sb.append ( criteria.get ( TITLE ) );
            }

            qds = new QueryDataSet(connection, sb.toString() );
            qds.fetchRecords();
            int size = qds.size();
            results = new Vector ( size );
            for ( int i = 0; i < size; i++ )
            {
                Object[] tmp = new Object[2];
                tmp[0] = new Integer(qds.getRecord(i).getValue(BOOKLIST_ID_COLUMN).asInt());
                tmp[1] = (String) qds.getRecord(i).getValue(BOOKLIST_COLUMN).asString();
                results.addElement ( tmp );
            }
*/
        }
        finally
        {
            qds.close();
            DBBroker.getInstance().releaseConnection(db);
        }
        return results;
	}
}