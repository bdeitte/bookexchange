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

public class AreaPeer extends BasePeer
{
    private static final String AREA_ID_COLUMN = "AREAID";
    private static final String AREA_COLUMN = "AREA";

    /** The table name for this peer. */
    public static final String TABLE_NAME = "area";

    public static final String AREA_ID = TABLE_NAME + "." + AREA_ID_COLUMN;
    public static final String AREA = TABLE_NAME + "." + AREA_COLUMN;

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
            
            if ( criteria.containsKey ( AREA ) )
            {
                rec.setValue ( AREA_COLUMN, (String) criteria.get(AREA) );
                rec.save();
            }
        }
        finally
        {
            tds.close();
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

            StringBuffer sb = new StringBuffer();
            sb.append ( "SELECT " );
            sb.append ( AREA_ID_COLUMN );
            sb.append ( ", " );
            sb.append ( AREA_COLUMN );
            sb.append ( " FROM " );
            sb.append ( TABLE_NAME );
            if ( criteria.containsKey ( AREA_ID ) )
            {
                sb.append ( " WHERE " );
                sb.append ( AREA_ID );
                sb.append ( " = " );
                sb.append ( criteria.get ( AREA_ID ) );
            }

            qds = new QueryDataSet(connection, sb.toString() );
            qds.fetchRecords();
            int size = qds.size();
            results = new Vector ( size );
            for ( int i = 0; i < size; i++ )
            {
                Object[] tmp = new Object[2];
                tmp[0] = new Integer(qds.getRecord(i).getValue(AREA_ID_COLUMN).asInt());
                tmp[1] = (String) qds.getRecord(i).getValue(AREA_COLUMN).asString();
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