package com.deitte.bookexchange.screens;

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
import org.apache.turbine.util.access.*;
import org.apache.ecs.*;
import org.apache.ecs.html.*;

public class ChangeAccountInfo extends Screen
{
    public ConcreteElement build( RunData data ) throws Exception
    {
        ElementContainer ec = new ElementContainer();

    	// my lame security model (works at least...)
        boolean guest = ((Boolean) data.user.getTemp("guest", new Boolean(false))).booleanValue();
        if ( guest || ! data.getUser().hasLoggedIn() )
        {
        	data.setMessage( "You must login before you change user info!");
			// send them to the default login screen
            return ScreenLoader.getInstance().eval ( data, 
            					TurbineResources.getInstance().getString("screen.login") );
        }

        data.setTitle("edit user info");
        
        Form form = new Form ( new DynamicURI ( data, "Main", "ChangeUserInfo", true ).toString()
            , Form.POST );

        form.addElement ( new Input ( Input.hidden, "nextscreen", data.getParameters().getString ( "nextscreen", "" ) ));
        Table table = new Table().setCellSpacing(0).setCellPadding(0).setBorder(0);

		String username = (String)data.getUser().getPerm(TurbineUserPeer.USERNAME);
		String password = (String)data.getUser().getPerm(TurbineUserPeer.PASSWORD);

        table.addElement ( new TR()
             .addElement ( "Email: " )
             .addElement ( new Input(Input.TEXT, "username", username )));

        table.addElement ( new TR()
             .addElement ( "Password:" )
             .addElement ( new Input(Input.PASSWORD, "password", password )));

        String bName = "submit";
        String bValue = "Change";
        
        table.addElement ( new TR().addElement ( 
        	new Input ( Input.submit, bName, bValue )));

        form.addElement ( table );
        return ec.addElement (form);
    }
}
