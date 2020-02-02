package com.deitte.bookexchange.screens;


// JDK Stuff
import java.io.*;
import java.sql.*;
import java.util.*;

// Servlet Stuff
import javax.servlet.*;
import javax.servlet.http.*;

// External Stuff
import org.apache.turbine.modules.Screen;
import org.apache.turbine.util.*;
import org.apache.turbine.util.access.*;
import com.workingdogs.village.*;
import org.apache.ecs.*;
import org.apache.ecs.html.*;

public class NewAccount extends Screen
{
    public ConcreteElement build( RunData data ) throws Exception
    {
        data.setTitle("create new account");
        
        ElementContainer ec = new ElementContainer();
        ec.addElement ( "To create a new account, please fill in all of the fields below. " );
        ec.addElement ( new P() );
        
        Form form = new Form ( new DynamicURI ( data, "Main", "CreateNewUser", true ).toString()
            , Form.POST );

        form.addElement ( new Input ( Input.hidden, "nextscreen", data.parameters.getString ( "nextscreen", "" ) ));
        Table table = new Table().setCellSpacing(0).setCellPadding(0).setBorder(0);

        table.addElement ( new TR()
             .addElement ( new TD().addElement ( "Email:" )
             .addElement ( new TD().addElement ( new Input(Input.TEXT, "username", data.parameters.getString("username", ""))))));
        table.addElement ( new TR()
             .addElement ( new TD().addElement ( "Password:" )
             .addElement ( new TD().addElement ( new Input(Input.PASSWORD, "password", "")))));
        table.addElement ( new TR()
             .addElement ( new TD().addElement ( "Password (confirm):" )
             .addElement ( new TD().addElement ( new Input(Input.PASSWORD, "password_confirm", "")))));

        String bName = "submit";
        String bValue = "Create New Account";
        
        table.addElement ( new TR().addElement(
            new Input ( Input.submit, bName, bValue ) ));

        form.addElement ( table );
        return ec.addElement (form);
    }
}
