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

public class AddBookForm extends Screen
{
    public ConcreteElement build( RunData data ) throws Exception
    {
    	// my lame security model (works at least...)
        boolean guest = ((Boolean) data.user.getTemp("guest", new Boolean(false))).booleanValue();
        if ( guest || ! data.getUser().hasLoggedIn() )
        {
        	data.setMessage( "You must login before you add a book!");
			// send them to the default login screen
            return ScreenLoader.getInstance().eval ( data, 
            					TurbineResources.getInstance().getString("screen.login") );
        }

        // Set the Title tag of the page
        data.setTitle("add book");

        Form form = new Form ( 
            new DynamicURI ( data, "AddBookForm", "AddBook", true ).toString()
            , Form.POST );

		form.addElement("Title ");
		form.addElement(new BR());
        form.addElement ( 
            new Input ( Input.text, "title", "")
                .setSize(25).setMaxlength(35));
		form.addElement(new BR());
		form.addElement("Author ");
		form.addElement(new BR());
        form.addElement ( 
            new Input ( Input.text, "author", "")
                .setSize(25).setMaxlength(35));

		form.addElement(new BR());
		form.addElement("Area ");
		form.addElement(new BR());

		Select areas = new Select("area");
		// set up the areas pop-up by getting the area
		// names from the database
        Criteria crit = new Criteria()
            .add ( "table_name", AreaPeer.TABLE_NAME );

        Vector results = AreaPeer.doSelect(crit);
        Enumeration enum = results.elements();
        while ( enum.hasMoreElements() )
        {
            Object[] tmp = (Object[]) enum.nextElement();
            Integer areaid = (Integer) tmp[0];
            String area = (String) tmp[1];

			areas.addElement(new Option(areaid.toString()));
			areas.addElement(area);
        }
		form.addElement(areas);

		form.addElement(new BR());
		form.addElement("Condition ");
		form.addElement(new BR());

		Select conditions = new Select("condition");
		// set up the conditions pop-up by getting the condition
		// names from the database
        crit = new Criteria()
            .add ( "table_name", ConditionPeer.TABLE_NAME );

        results = ConditionPeer.doSelect(crit);
        enum = results.elements();
        while ( enum.hasMoreElements() )
        {
            Object[] tmp = (Object[]) enum.nextElement();
            Integer cid = (Integer) tmp[0];
            String c = (String) tmp[1];

			conditions.addElement(new Option(cid.toString()));
			conditions.addElement(c);
        }
		form.addElement(conditions);
 
		form.addElement(new BR());
		form.addElement("ISBN ");
		form.addElement(new BR());
        form.addElement ( 
            new Input ( Input.text, "isbn", "") 
                .setSize(25).setMaxlength(70));

 		form.addElement(new BR());
		form.addElement("Price ");
		form.addElement(new BR());
        form.addElement ( 
            new Input ( Input.text, "price", "" )
                .setSize(25).setMaxlength(35));

		form.addElement(new BR());
		form.addElement("Other Information ");
		form.addElement(new BR());
        form.addElement ( 
            new TextArea ( "other", 5, 30));
        form.addElement(new P());

		String submit = "add book";
		form.addElement(new Input(Input.submit, "submit", submit));

        return form;
    }
}
