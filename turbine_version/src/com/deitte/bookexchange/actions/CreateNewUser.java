package com.deitte.bookexchange.actions;
 
// JDK Stuff
import java.io.*;
import java.sql.*;
import java.util.*;

// Servlet Stuff
import javax.servlet.*;
import javax.servlet.http.*;

// External Stuff
import org.apache.turbine.modules.*;
import org.apache.turbine.util.*;
import org.apache.turbine.util.db.*;
import com.workingdogs.village.*;

/**
*/
public class CreateNewUser extends Action
{
    public void build( RunData data ) throws Exception
    {
    	// in case people aren't playing nice
        String submit = "submit";
        String str = (String) data.user.getTemp ( submit, "asdfasdf" );
        if ( str != null && str
            .equalsIgnoreCase( data.parameters.getString(submit, "")) )
        {
            data.user.removeTemp(submit);
            data.setScreen ( TurbineResources.getInstance()
              .getString("screen.homepage") );
            return;            
        }
        
        String pass1 = data.parameters.getString("password", "");
        String pass2 = data.parameters.getString("password_confirm", "");
        
        if ( (pass1.length() == 0 || pass2.length() == 0 )
            || ! pass1.equals ( pass2 ) )
        {
            data.setMessage("Sorry, the passwords do not match.");
            data.setScreen("NewAccount");
            return;
        }
        
        String username = data.parameters.getString("username", "");
        if ( username.length() < 3 || username.indexOf('@') == -1)
        {
            data.setMessage("Sorry, you must supply a valid email address.");
            data.setScreen("NewAccount");
            return;
        }            

        Criteria testcrit = new Criteria();
        testcrit.add ( TurbineUserPeer.getColumnName("LOGINID"), username );
        Vector output = TurbineUserPeer.doSelect(testcrit);
        // Make sure that the user doesn't already exist 
        if (output == null || output.size() == 0)
        {
            // get a connection to the db
            DBConnection db = DBBroker.getInstance().getConnection();
            Connection connection = db.getConnection();
    
            // execute the query
            TableDataSet tds = new TableDataSet( connection, TurbineUserPeer.getTableName() );
            QueryDataSet qds = null;
            try
            {
                Record rec = tds.addRecord();
                rec.setValue ( "LOGINID", username );
                rec.setValue ( "PASSWORD_VALUE", data.parameters.getString("password") );
                rec.save();

                data.setMessage("Your new account has been created!");                
            }
            finally
            {
                if ( tds != null ) tds.close();
                if ( qds != null ) qds.close();
                DBBroker.getInstance().releaseConnection(db);
            }
        }
        else
        {
            data.setMessage("Sorry, that username already exists. Please choose another.");
            data.setScreen("NewAccount");
            data.parameters.add("username", "");
        }
    }
}
