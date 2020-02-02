package com.deitte.bookexchange.actions;
 
// Java Core CLasses
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
import org.apache.turbine.util.db.*;

// Village Database Classes
import com.workingdogs.village.*;

/**
	This is where we authenticate the user logging into the system
	against a user in the database. If the user exists in the database
	that users last login time will be updated.
*/
public class LoginUser extends Action
{   
 
 	public void build( RunData data ) throws Exception
	{
        // This prevents a db hit on second Action call during page
        // generation.  Turbine removes everything from the Session before
        // calling this method, so in this case we should continue on with
        // the Login procedure
        if ( data.getUserFromSession() != null ) 
        {
            return;
        }
        
        String username = data.parameters.getString ( "username", "" );
		String password = data.parameters.getString ( "password", "" );
        
        String userClassName = TurbineResources.getInstance()
            .getString("user.class", "org.apache.turbine.util.TurbineUser");
            
        User user = ((User)Class.forName(userClassName).newInstance()).retrieveFromStorage( username );

		if ( validateUser(user, password) != 0 )
		{
            data.setMessage("Sorry, your email or password is incorrect.");    
            data.user = new TurbineUser();
			data.user.setUserName("");
            data.setScreen(TurbineResources
                           .getInstance().getString("screen.login"));
		}
		else
		{
			data.user = user;

            // mark the user as being logged in
            user.setHasLoggedIn(new Boolean(true));
            
            // set the last_login date in the database
            user.updateLastLogin();

			// remove the guest from temp
			user.removeTemp("guest");

            // this only happens if the user is valid
            // otherwise, we will get a valueBound in the User
            // object when we don't want to because the username is
            // not set yet.
            // save the User object into the session
            data.save();
		}
	}
    
	/**
		0: username and password is valid<br>
		1: username is not valid<br>
		2: password is not valid
	*/   
	int validateUser(User user, String password)
	{
   
        if ( user != null ) 
        {
            if (  user.getPassword().equals(password) )
            {
                return 0;
            }
		    else
			{
				return 2;
			}
		}
		return 1;
	}
}