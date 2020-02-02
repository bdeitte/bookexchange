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

public class ConditionPeer extends BasePeer
{
    private static final String CONDITION_ID_COLUMN = "CONDITIONID";
    private static final String CONDITION_COLUMN = "CONDITION";

    /** The table name for this peer. */
    public static final String TABLE_NAME = "condition";

    public static final String CONDITION_ID = TABLE_NAME + "." + CONDITION_ID_COLUMN;
    public static final String CONDITION = TABLE_NAME + "." + CONDITION_COLUMN;

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
            
            if ( criteria.containsKey ( CONDITION ) )
            {
                rec.setValue ( CONDITION_COLUMN, (String) criteria.get(CONDITION) );
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
            sb.append ( CONDITION_ID_COLUMN );
            sb.append ( ", " );
            sb.append ( CONDITION_COLUMN );
            sb.append ( " FROM " );
            sb.append ( TABLE_NAME );
            if ( criteria.containsKey ( CONDITION_ID ) )
            {
                sb.append ( " WHERE " );
                sb.append ( CONDITION_ID );
                sb.append ( " = " );
                sb.append ( criteria.get ( CONDITION_ID ) );
            }

            qds = new QueryDataSet(connection, sb.toString() );
            qds.fetchRecords();
            int size = qds.size();
            results = new Vector ( size );
            for ( int i = 0; i < size; i++ )
            {
                Object[] tmp = new Object[2];
                tmp[0] = new Integer(qds.getRecord(i).getValue(CONDITION_ID_COLUMN).asInt());
                tmp[1] = (String) qds.getRecord(i).getValue(CONDITION_COLUMN).asString();
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