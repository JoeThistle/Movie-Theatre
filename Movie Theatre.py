#Title: Movie Theatre
#Author: Joe Thistlethwaite
#Purpose: To allow for users to book tickets for a movie
#Version: 4.5

from tkinter import *
from tkinter import ttk
import random
import time
import json
from datetime import date, timedelta

#PLEASE DO "pip install pillow" IN THE TERMINAL FOR THE FOLLOWING LINE TO WORK
from PIL import Image, ImageTk

#Opens the movie data file and sets all the variables
with open("Movie Data.json") as file:
    data = json.loads(file.read())
MAX_SEATS = data["max_seats"]
MOVIES = data["movies&showings"]
TIMES = data["timeslots"]
PRICING = data["pricing"]

#Gets the date the program starts at using the system's time
start_date = date.today() + timedelta(days=1)
new_date = start_date
stored_times = {}
booked_seats = {}

class MovieBookings:
    def __init__(self, master, movie_name, times):
        '''This function initializes all the variables'''
        self.master = master
        self.movie_name = movie_name
        self.times = times
        #Creates buttons for the grid
        self.create_movie_times()

    def validate_entry(self, value):
        '''Ensures that the entry value is a non-negative integer'''
        if value == "":
            return True
        if value.isdigit() and int(value) >= 0:
            return True
        return False

    def create_movie_times(self):
        '''Creates the times for ticket selection based on movie choice'''
        #Create the frame to hold the time buttons and place it to the right of the movies frame
        times_frame = Frame(self.master, bg="#077deb")
        times_frame.grid(row=3, column=2, sticky="NWE")

        #Configure the grid columns in times_frame to expand equally
        times_frame.grid_columnconfigure(0, weight=1)
        for i in range(len(self.times)):
            times_frame.grid_columnconfigure(i, weight=1)

        #Create the movie label and span it across all columns
        current_movie_lbl = Label(times_frame, text=movie_selected.get(), bg="light blue", fg="#077deb", height=4, font=("arial",50,"bold"))
        current_movie_lbl.grid(padx=100, pady=30, row=0, column=0, columnspan=len(self.times), sticky="WE")

        #Create buttons for each time slot
        for num, time in enumerate(self.times):
            Button(times_frame, text=time, command=lambda t=time: self.ticket_booking(t), fg="light blue", bg="#077deb", width=10, cursor="hand2", font=("arial",18,"bold")).grid(padx=10, pady=5, row=1, column=num, sticky="WE")
            

    def ticket_booking(self, time):
        '''This function does all of the tasks related to booking tickets'''
        tickets = {i: StringVar(value='0') for i in PRICING}

        def calculate_total(*args):
            '''Calculates the total cost of the users order'''
            total_tickets = 0
            total_cost = 0
            try:
                #Gets the total number of tickets
                for i in PRICING:
                    #Checks if any entries are blank
                    if tickets[i].get() != "":
                        total_tickets += int(tickets[i].get())
                #Checks to make sure there aren't too many tickets
                if total_tickets > MAX_SEATS:
                    total_lbl.config(text="Too many tickets")
                else:
                    #Prints the total 
                    for i in PRICING:
                        if tickets[i].get() != "":
                            total_cost += int(tickets[i].get()) * PRICING[i]
                    total_lbl.config(text=f"${total_cost:.2f}")
            #If they enter text instead of numbers
            except ValueError:
                total_lbl.config(text="$0.00")
            total_lbl.grid(row=len(PRICING), column=1, sticky="WE", ipady=8, ipadx=15)

        def book():
            '''Books the users ticket'''
            total_tickets = 0
            #Gets the tickets that they are booking
            for i in PRICING:
                if tickets[i].get() != "":
                    total_tickets += int(tickets[i].get())
            #If they book more than the max amount of seats
            if total_tickets > MAX_SEATS:
                success_lbl.grid_remove()
                error_lbl.config(text="Cannot book more than available seats.", bg="red")
                error_lbl.grid(row=len(PRICING) + 2, column=0, columnspan=2, sticky="WE", ipady=8, ipadx=15)
                return
            date_str = new_date.strftime('%d-%m-%y')
            #Creates the key of what they are booking using the movie, date and time
            key = (movie_selected.get(), time, date_str)
            #Checks if they have booked any seats
            if key not in booked_seats:
                booked_seats[key] = 0
            #Checks if there are too many seats being booked
            if booked_seats[key] + total_tickets > MAX_SEATS:
                success_lbl.grid_remove()
                error_lbl.config(text="Not enough seats available.", bg="orange")
                error_lbl.grid(row=len(PRICING) + 2, column=0, columnspan=2, sticky="WE", ipady=8, ipadx=15)
                return
            #Adds the rest of the seats to the booked seats using the key
            booked_seats[key] += total_tickets
            error_lbl.grid_remove()
            success_lbl.config(text="Booking successful!", bg="green", fg="white")
            success_lbl.grid(row=len(PRICING) + 2, column=0, columnspan=2, sticky="WE", ipady=8, ipadx=15)

        #Makes the new window on top
        root = Toplevel(window)
        root.grab_set()
        root.title("Ticket Booking")
        root.bind('<Return>', lambda event:book())
        #Makes all the labels and grid entries
        for i, (type, price) in enumerate(PRICING.items()):
            Label(root, text=f"{type}: ${price}", bg="#077deb").grid(row=i, column=0, sticky="WE", ipady=8, ipadx=15)
            ticket_ent = Entry(root, textvariable=tickets[type])
            ticket_ent.grid(row=i, column=1, sticky="WE", ipady=8, ipadx=15)
            ticket_ent.config(validate="key", validatecommand=(root.register(self.validate_entry), "%P"))
            tickets[type].trace_add('write', calculate_total)

        #Makes the total label and calculates the amount that should be shown
        total_lbl = Label(root, text="$0.00", bg="#077deb")
        total_lbl.grid(row=len(PRICING), column=1, sticky="WE", ipady=8, ipadx=15)
        calculate_total()
        book_btn = ttk.Button(root, text="Book Tickets", command=book)
        book_btn.grid(row=len(PRICING), column=0, sticky="WE", ipady=8, ipadx=15)
        error_lbl = Label(root, text="")
        error_lbl.grid(row=len(PRICING) + 2, column=0, columnspan=2, sticky="WE", ipady=8, ipadx=15)
        success_lbl = Label(root, text="")
        success_lbl.grid(row=len(PRICING) + 3, column=0, columnspan=2, sticky="WE", ipady=8, ipadx=15)


def main_menu(movie_list):
    '''This function creates buttons for movie selection and displays the movie image'''
    global movie_selected
    global date_lbl
    global date_frame

    #Create all the stationary labels
    main_movie_lbl = Label(window, text="Movie Selector", bg="#077deb", fg="white", font="Arial 50 bold")
    main_movie_lbl.grid(row=1, column=0, columnspan=3, sticky="WE")

    #Create the frame for the date
    date_frame = Frame(window, bg="#077deb")
    date_frame.grid(row=0, column=0, columnspan=3, sticky="NSEW")

    #Configure rows and columns to expand properly
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(2, weight=1)
    date_frame.grid_columnconfigure(0, weight=1)
    date_frame.grid_columnconfigure(1, weight=1)
    date_frame.grid_columnconfigure(2, weight=1)

    date_lbl = Label(date_frame, text=f"Date: {new_date.strftime('%d-%m-%y')}", bg="#077deb", fg="white", font="Arial 15 bold", pady=20)
    date_lbl.grid(row=0, column=1)

    date_forward = Button(date_frame, text=">", command=future_day)
    date_forward.grid(row=0, column=2)

    date_backward = Button(date_frame, text="<", command=past_day, state="disabled")
    date_backward.grid(row=0, column=0)

    #Create a canvas for scrolling
    canvas = Canvas(window, bg="#077deb")
    canvas.grid(row=3, column=0, sticky="NSEW")

    #Create a scrollbar linked to the canvas
    scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=3, column=1, sticky="NS")
    canvas.configure(yscrollcommand=scrollbar.set)

    #Bind mouse wheel to canvas scroll
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    #Create a frame inside the canvas which will hold the movie buttons and images
    movies_frame = Frame(canvas, bg="#077deb")
    canvas.create_window((0, 0), window=movies_frame, anchor="nw")

    def on_frame_config(event):
        '''Update the scroll region of the canvas when the frame size changes'''
        canvas.configure(scrollregion=canvas.bbox("all"))

    movies_frame.bind("<Configure>", on_frame_config)

    #Create buttons for each movie and load images
    for num, movie in enumerate(movie_list):
        btn = Button(movies_frame, text=movie, cursor="hand2", command=lambda m=movie: choose_times(m))
        btn.grid(row=num, column=0, padx=10, pady=5, sticky="W")
        try:
            #Get and resize the image to fit
            image = Image.open(f"{movie}.png")
            image = image.resize((150, 200))
            movie_image = ImageTk.PhotoImage(image)
            image_label = Label(movies_frame, image=movie_image, bg="#077deb")
            image_label.image = movie_image
            image_label.grid(row=num, column=1, padx=10, pady=5, sticky="W")
        except Exception as e:
            print(f"Error loading image for {movie}: {e}")

    #Ensures that the movies frame expands to fill the canvas
    window.grid_rowconfigure(3, weight=1)
    window.grid_columnconfigure(0, weight=0)

    #Creates the program exit button and admin button and puts them into a frame
    admin_frm = Frame(window)
    exit_btn = Button(admin_frm,text="Close Program",fg="light blue", bg="#077deb", cursor="hand2", font=("arial",18,"bold"),command=exit).grid(padx=10, pady=5, row=0, column=1, sticky="WE")
    admin_btn = Button(admin_frm,text="Edit Movies",fg="light blue", bg="#077deb", cursor="hand2", font=("arial",18,"bold"),command=()).grid(padx=10, pady=5, row=0, column=0, sticky="WE")
    admin_frm.grid(row=4,column=2)


def future_day():
    '''This function creates a new day with different timeslots'''
    global new_date
    global date_lbl
    date_backward = Button(date_frame, text="<", command=past_day, state="active")
    date_backward.grid(row=0, column=0)
    #Sets the date label to the current date plus one day
    new_date = new_date + timedelta(days=1)
    date_lbl.config(text=f"Date: {new_date.strftime('%d-%m-%y')}")
    choose_times(movie_selected.get())


def past_day():
    '''This function goes back to a previous day'''
    global new_date
    #Checks to make sure the day isn't today
    if (new_date - timedelta(days=2)) == date.today():
        date_backward = Button(date_frame, text="<", command=past_day, state="disabled")
        date_backward.grid(row=0, column=0)
    new_date = new_date - timedelta(days=1)
    #Configures the date label to show the new date
    date_lbl.config(text=f"Date: {new_date.strftime('%d-%m-%y')}")
    choose_times(movie_selected.get())

def choose_times(movie):
    '''Generates times for the selected movie and current date if not already generated'''
    global movie_selected
    movie_selected = StringVar(value=movie)
    date_str = new_date.strftime('%d-%m-%y')
    if (movie, date_str) not in stored_times:
        chosen_times = random.sample(TIMES, MOVIES[movie])
        #Format to convert to a time object
        time_format = '%I:%M%p'
        #Creates list and converts them using times chosen
        time_hours = [time.strptime(t, time_format) for t in chosen_times]
        #Sorts the list using the new objects
        chosen_times = [time.strftime(time_format, h) for h in sorted(time_hours)]
        stored_times[(movie, date_str)] = chosen_times
    else:
        chosen_times = stored_times[(movie, date_str)]
    MovieBookings(window, movie, chosen_times)


#Main Program
window = Tk()
window.title("Movie Theatre")
window.attributes('-fullscreen', True)
window.configure(bg="#077deb")
main_menu(list(MOVIES.keys()))
window.mainloop()