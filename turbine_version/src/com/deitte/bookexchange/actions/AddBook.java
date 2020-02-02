package com.deitte.bookexchange.actions;
 
// JDK Stuff
import java.io.*;
import java.sql.*;
import java.util.*;

// Servlet Stuff
import javax.servlet.*;
import javax.servlet.http.*;

// External Stuff
import com.deitte.bookexchange.peers.*;
import org.apache.turbine.modules.*;
import org.apache.turbine.util.*;
import org.apache.turbine.util.db.*;
import com.workingdogs.village.*;

/**
*/
public class AddBook extends Action
{
    public void build( RunData data ) throws Exception
    {
    	// my lame security model (works at least...)
        boolean guest = ((Boolean) data.user.getTemp("guest", new Boolean(false))).booleanValue();
        if ( guest || ! data.getUser().hasLoggedIn() )
        {
        	data.setMessage( "You must login before you change user info!");
			// send them to the default login screen
            data.setScreen( TurbineResources.getInstance().getString("screen.login") );
            return;
        }

        Criteria crit = new Criteria();
        ParameterParser p = data.getParameters();
        crit.add ( BookPeer.TITLE, p.getString("title") );
        crit.add ( BookPeer.AUTHOR, p.getString("author") );
        crit.add ( BookPeer.AREA_ID, p.getInt("area") );
        crit.add ( BookPeer.CONDITION_ID, p.getInt("condition") );
        crit.add ( BookPeer.ISBN, p.getString("isbn") );
        crit.add ( BookPeer.OTHER, p.getString("other") );
        crit.add ( BookPeer.PRICE, p.getString("price") );

        int bookNum = BookPeer.doInsert(crit);
		int userNum = data.getUser().getId();

		crit = new Criteria();
		crit.add( BookListPeer.BOOK_ID, bookNum);
		crit.add( BookListPeer.VISITOR_ID, userNum);
		BookListPeer.doInsert(crit);
		
        data.setMessage("Your book has been added!");
                
    }
}
