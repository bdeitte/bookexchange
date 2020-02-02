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
import com.workingdogs.village.*;
import org.apache.ecs.*;
import org.apache.ecs.html.*;

public class SearchBooks extends Screen
{
    public ConcreteElement build( RunData data ) throws Exception
    {
        data.setTitle("search for books");
        
        ElementContainer ec = new ElementContainer();

        Form form = new Form ( new DynamicURI ( data, "SearchResults", true ).toString()
            , Form.POST );

        form.addElement ( new StringElement ( "Search: " ));
        form.addElement ( 
            new Input ( Input.text, "search", 
                data.parameters.getString("search", ""))
                .setSize(30).setMaxlength(50));

		form.addElement(" ");

        form.addElement ( 
            new Input ( Input.submit, "submit", "search" ));

        return ec.addElement ( form );
    }
}
