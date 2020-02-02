package com.deitte.bookexchange.screens;

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
import org.apache.turbine.util.access.*;
import com.workingdogs.village.*;
import org.apache.ecs.*;
import org.apache.ecs.html.*;

public class SearchResults extends Screen
{
    public ConcreteElement build( RunData data ) throws Exception
    {
        data.setTitle("search results");

    	ElementContainer ec = new ElementContainer();
		ec.addElement("here are your (pseudo) search results");
		ec.addElement(new P());

        // get the reults (not really getting anything but everything...)
        Vector results = BookPeer.doSelect(new Criteria());

        Enumeration enum = results.elements();
        while ( enum.hasMoreElements() )
        {
            Object[] tmp = (Object[]) enum.nextElement();

			// add fancy html here later
			ec.addElement("title: " + tmp[1]);
			ec.addElement(new BR());
			ec.addElement("author: " + tmp[2]);
			ec.addElement(new BR());
			ec.addElement("area: " + tmp[3]);
			ec.addElement(new BR());
			ec.addElement("condition: " + tmp[4]);
			ec.addElement(new BR());
			ec.addElement("isbn: " + tmp[5]);
			ec.addElement(new BR());
			ec.addElement("other: " + tmp[6]);
			ec.addElement(new BR());
			ec.addElement("price: " + tmp[7]);

			ec.addElement(new P());
        }
        return ec;
    }
}