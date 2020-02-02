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

public class Login extends Screen
{
    public ConcreteElement build( RunData data ) throws Exception
    {
        data.setTitle("login");
        
        String screen = data.parameters.getString("nextscreen", null);
        if ( screen == null )
            screen = "Main";

        Form form = new Form ( new DynamicURI ( data, screen, "LoginUser", true ).toString()
            , Form.POST );

        form.addElement ( new Input ( Input.hidden, "nextscreen", screen ) );

        form.addElement ( new StringElement ( "Email:" ));
        form.addElement ( new BR() );

        form.addElement ( 
            new Input ( Input.text, "username", 
                data.parameters.getString("username", ""))
                .setSize(12).setMaxlength(25));

        form.addElement ( new BR() );
        
        form.addElement ( new StringElement ( "Password:" ));
        form.addElement ( new BR() );
        form.addElement ( 
            new Input ( Input.password, "password", "" )
                .setSize(12).setMaxlength(25));

        form.addElement ( new BR() );

        form.addElement ( 
            new Input ( Input.submit, "submit", "login" ));

        A a = new A();
        a.setHref(
            new DynamicURI(data, "NewAccount")
                .addPathInfo("nextscreen", screen )
                .toString()
                ).addElement("Create a new account");
        
        form.addElement ( new P() );
        form.addElement ( a );
        return form;
    }
}
