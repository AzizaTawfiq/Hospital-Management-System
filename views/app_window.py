import tkinter as tk
from .main_view import MainView
from .doctor_view import DoctorView
from .patient_view import PatientView

class HospitalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Management System") # set the title of the window
        # set the size of the window and the position of the window 
        #width=650, height=550, x=600, y=250 px
        self.geometry("580x550+600+250") 
        
        self.container = tk.Frame(self) # create a container frame to hold all the frames
        self.container.pack(fill="both", expand=True) # fill the container with the frame and 
        # create a dictionary to hold all the frames
        self.frames = {
            F.__name__: F(parent=self.container, controller=self)
            for F in (MainView, DoctorView, PatientView)
        }
         
        # place all the frames in the container
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew") 

        # show the default view when the app starts
        self.show_frame("MainView") 

    # method to show a specific frame
    def show_frame(self, page_name):
        # get the frame from the dictionary
        frame = self.frames[page_name]
        # raise the frame to the top
        frame.tkraise()
        # if the frame has an update_view method, call it
        if hasattr(frame, "update_view"):
            frame.update_view()
