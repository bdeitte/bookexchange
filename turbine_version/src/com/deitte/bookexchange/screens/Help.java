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

public class Help extends Screen
{
    public ConcreteElement build( RunData data ) throws Exception
    {        
        // Set the Title tag of the page
        data.setTitle("the bookexchange");

        ElementContainer ec = new ElementContainer();
        ec.addElement ( new P() );

		ec.addElement( "This is where help would appear." );
		ec.addElement( new P() );

        return ec;
    }
}
