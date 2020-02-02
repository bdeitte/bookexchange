package com.deitte.bookexchange.actions;

// JDK Stuff
import java.io.*;
import java.sql.*;
import java.util.Hashtable;

// Servlet Stuff
import javax.servlet.*;
import javax.servlet.http.*;

// External Stuff
import org.apache.turbine.modules.*;
import org.apache.turbine.util.*;
import com.workingdogs.village.*;

/**
*/
public class SessionValidator extends Action
{
    public void build( RunData data ) throws Exception
    {
        data.populate();

        if ( ! data.hasScreen() )
        {
            //data.setMessage ("There has been an error, your session is valid, " + 
            //    "but the screen variable is not defined.");
            data.setScreen(TurbineResources.getInstance()
              .getString("screen.homepage"));
        }
        
        // The user may have not logged in, so create a "guest" user
        if ( data.user == null )
        {
            data.user = new TurbineUser();
            data.user.setTemp ( "guest", new Boolean(true) );
            data.save();
        }
    }
}
