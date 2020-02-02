package com.deitte.bookexchange.layouts;
 
// Java Core Classes
import java.io.*;
import java.sql.*;
import java.util.*;

// Java Servlet Classes
import javax.servlet.*;
import javax.servlet.http.*;

// Turbine Modules
import org.apache.turbine.modules.*;

// Turbine Utility Classes
import org.apache.turbine.util.*;

// ECS Classes
import org.apache.ecs.*;
import org.apache.ecs.html.*;

// Village Database Classes
import com.workingdogs.village.*;

public class DefaultLayout extends Layout
{
    public void build( RunData data ) throws Exception
    {
        // get an EC and stick it at the top of the body
        // this EC is then used later on if there is a message to display
        // otherwise it ends up being blank. This is so that a Screen can
        // also data.setMessage() to give information to the user.
        ElementContainer sm = new ElementContainer();
        data.getPage().getBody().addElement ( sm );
        
        // Now execute the Screen portion of the page
        ConcreteElement screen = ScreenLoader.getInstance().eval ( data, data.getScreen() );
        if (screen != null)
            data.getPage().getBody().addElement( screen );

        // If an Action has defined a message, attempt to display it here
        // see above for why it is here
        if ( data.getMessage() != null )
        {
            sm.addElement(new P());
            sm.addElement( data.getMessage() );
            sm.addElement(new P());
        }
        
        // The screen should have attempted to set a Title 
        // for itself, otherwise, a default title is set
        data.getPage().getTitle()
            .addElement( data.getTitle() );

        // The screen should have attempted to set a Body bgcolor 
        // for itself, otherwise, a default body bgcolor is set
        data.getPage().getBody()
            .setBgColor(HtmlColor.white);

        ConcreteElement bottomNav = 
        	NavigationLoader.getInstance().eval ( data, "OptionsFooter" );
        if ( bottomNav != null)
            data.getPage().getBody().addElement( bottomNav );
    }
}
