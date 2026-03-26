# This file is entry point protection 

from views import HospitalApp

# name guard: it is a way to prevent the application from running if it is not the main program 
# import app.py in another file will not run the application as we use name guard
if __name__ == "__main__":  
    # create the main window of the application
    app = HospitalApp()
    # start the application and keep it running until the user closes it based on event loop 
    # the event loop is a loop that keeps the application running and responsive to user interactions
    # it listens for events such as mouse clicks, key presses, and window resize events
    # if removed the application will close immediately after opening
    app.mainloop() 
