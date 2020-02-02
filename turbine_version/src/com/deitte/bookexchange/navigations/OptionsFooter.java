package com.deitte.bookexchange.navigations;
 
// Java Core Classes
import java.io.*;
import java.sql.*;
import java.util.*;

// Java Servlet Classes
import javax.servlet.*;
import javax.servlet.http.*;

// External Stuff
import org.apache.turbine.modules.*;
import org.apache.turbine.util.*;
import org.apache.turbine.util.db.*;
import org.apache.turbine.util.access.*;
import com.workingdogs.village.*;
import org.apache.ecs.*;
import org.apache.ecs.html.*;

public class OptionsFooter extends Navigation
{
    public ConcreteElement build( RunData data ) throws Exception
    {
        // show the options stuff
        ElementContainer ec = new ElementContainer();

		ec.addElement(new P());

        // show the menu of options for logged-in user
        if ( data.user.hasLoggedIn() )
        {
	        Table table = new Table().setBorder(0).setCellPadding(5).setCellSpacing(0);
    	    TR tr = new TR();

        	table.addElement( tr.addElement(new TD (
            	new A().setHref(
            	new DynamicURI(data, "AddBookForm")
                	.toString()
                	).addElement("[add book]")
                	).setColSpan(2)));

        	table.addElement( tr.addElement(new TD (
            	new A().setHref(
            	new DynamicURI(data, "EditBook")
                	.toString()
                	).addElement("[edit book]")
                	).setColSpan(2)));

        	table.addElement( tr.addElement(new TD (
            	new A().setHref(
            	new DynamicURI(data, "RemoveBook")
                	.toString()
                	).addElement("[remove book]")
                	).setColSpan(2)));

        	table.addElement( tr.addElement(new TD (
            	new A().setHref(
            	new DynamicURI(data, "ChangeAccountInfo")
                	.toString()
                	).addElement("[edit user info]")
                	).setColSpan(2)));


	        ec.addElement ( table );
		}
        
        String loginText = null;
        String loginAction = "";
        String loginScreen = "";
        if ( data.user.hasLoggedIn() )
        {
            loginText = "[Logout]";
            loginAction = "LogoutUser";
        }
        else
        {
            loginText = "[Login]";
            loginScreen = "Login";            
        }

        // show the menu of options
        Table table = new Table().setBorder(0).setCellPadding(5).setCellSpacing(0);
        TR tr = new TR();

        table.addElement( tr.addElement(new TD (
            new A().setHref(
            new DynamicURI(data, "Main")
                .toString()
                ).addElement("[Home]")
                ).setColSpan(2)));

        table.addElement( tr.addElement(new TD (
            new A().setHref(
            new DynamicURI(data, "SearchBooks")
                .toString()
                ).addElement("[Search]")
                ).setColSpan(2)));

        table.addElement( tr.addElement(new TD (
            new A().setHref(
            new DynamicURI(data, "Help")
                .toString()
                ).addElement("[Help]")
                ).setColSpan(2)));

        table.addElement( tr.addElement(new TD (
            new A().setHref(
            new DynamicURI(data, loginScreen, loginAction)
                .addPathInfo("nextscreen", data.getScreen() )
                .toString()
                ).addElement(loginText)
                ).setColSpan(2)));

        ec.addElement ( table );
        
        return ( ec );
    }
}
