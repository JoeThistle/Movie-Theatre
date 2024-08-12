#Title: Movie Theatre
#Author: Joe Thistlethwaite
#Purpose: To allow for users to book tickets for a movie
#Version: 3.6
from tkinter import *
from tkinter import ttk
import random
import time
import json
from datetime import date, timedelta

# Opens the movie data file and sets all the variables
with open("Movie Data.json") as file:
    data = json.loads(file.read())
MAX_SEATS = data["max_seats"]
MOVIES = data["movies&showings"]
TIMES = data["timeslots"]
PRICING = data["pricing"]

# Gets the date the program starts at using the system's time
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
        # Creates buttons for the grid
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
        btn_clear()
        # Loops and ensures that it will work with any number of movie slots (assuming there are enough times)
        for num, time in enumerate(self.times):
            ttk.Button(self.master, text=time, command=lambda t=time: self.ticket_booking(t)).grid(padx=10, pady=5, column=2, row=(num + 2))


    def ticket_booking(self, time):
        '''This function does all of the tasks related to booking tickets'''
        tickets = {i: StringVar(value='0') for i in PRICING}


        def calculate_total(*args):
            '''Calculates the total cost of the users order'''
            total_tickets = 0
            total_cost = 0
            try:
                # Gets the total number of tickets
                for i in PRICING:
                    # Checks if any entries are blank
                    if tickets[i].get() != "":
                        total_tickets += int(tickets[i].get())
                # Checks to make sure there aren't too many tickets
                if total_tickets > MAX_SEATS:
                    total_lbl.config(text="Too many tickets")
                else:
                    # Prints the total 
                    for i in PRICING:
                        if tickets[i].get() != "":
                            total_cost += int(tickets[i].get()) * PRICING[i]
                    total_lbl.config(text=f"${total_cost:.2f}")
            # If they enter text instead of numbers
            except ValueError:
                total_lbl.config(text="$0.00")
            total_lbl.grid(row=len(PRICING), column=1, sticky="WE", ipady=8, ipadx=15)

        def book():
            '''Books the users ticket'''
            total_tickets = 0
            # Gets the tickets that they are booking
            for i in PRICING:
                if tickets[i].get() != "":
                    total_tickets += int(tickets[i].get())
            # If they book more than the max amount of seats
            if total_tickets > MAX_SEATS:
                success_lbl.grid_remove()
                error_lbl.config(text="Cannot book more than available seats.", bg="red")
                error_lbl.grid(row=len(PRICING) + 2, column=0, columnspan=2, sticky="WE", ipady=8, ipadx=15)
                return
            date_str = new_date.strftime('%d-%m-%y')
            # Creates the key of what they are booking using the movie, date and time
            key = (movie_selected.get(), time, date_str)
            # Checks if they have booked any seats
            if key not in booked_seats:
                booked_seats[key] = 0
            # Checks if there are too many seats being booked
            if booked_seats[key] + total_tickets > MAX_SEATS:
                success_lbl.grid_remove()
                error_lbl.config(text="Not enough seats available.", bg="orange")
                error_lbl.grid(row=len(PRICING) + 2, column=0, columnspan=2, sticky="WE", ipady=8, ipadx=15)
                return
            # Adds the rest of the seats to the booked seats using the key
            booked_seats[key] += total_tickets
            error_lbl.grid_remove()
            success_lbl.config(text="Booking successful!", bg="green", fg="white")
            success_lbl.grid(row=len(PRICING) + 2, column=0, columnspan=2, sticky="WE", ipady=8, ipadx=15)

        # Makes the new window on top
        root = Toplevel(window)
        root.title("Ticket Booking")
        # Makes all the labels and grid entries
        for i, (type, price) in enumerate(PRICING.items()):
            Label(root, text=f"{type}: ${price}",bg="#b3ff00").grid(row=i, column=0, sticky="WE", ipady=8, ipadx=15)
            ticket_ent = Entry(root, textvariable=tickets[type])
            ticket_ent.grid(row=i, column=1, sticky="WE", ipady=8, ipadx=15)
            ticket_ent.config(validate="key", validatecommand=(root.register(self.validate_entry), "%P"))
            tickets[type].trace_add('write', calculate_total)

        # Makes the total label and calculates the amount that should be shown
        total_lbl = Label(root, text="$0.00",bg="#b3ff00")
        total_lbl.grid(row=len(PRICING), column=1, sticky="WE", ipady=8, ipadx=15)
        calculate_total()
        book_btn = ttk.Button(root, text="Book Tickets", command=book)
        book_btn.grid(row=len(PRICING), column=0, sticky="WE", ipady=8, ipadx=15)
        error_lbl = Label(root, text="")
        error_lbl.grid(row=len(PRICING) + 2, column=0, columnspan=2, sticky="WE", ipady=8, ipadx=15)
        success_lbl = Label(root, text="")
        success_lbl.grid(row=len(PRICING) + 3, column=0, columnspan=2, sticky="WE", ipady=8, ipadx=15)



def main_menu(movie_list):
    '''This function creates the dropdown menu based off of what movies there are'''
    global movie_selected
    global date_lbl

    # Creates the dropbox along with selecting the times if someone selects a different movie within the drop box
    movie_selected = StringVar()
    movie_drop_box = ttk.Combobox(window, textvariable=movie_selected, state="readonly")
    movie_drop_box['values'] = movie_list
    movie_drop_box.grid(padx=10, pady=5, row=2, column=0, sticky="WE")
    movie_drop_box.bind("<<ComboboxSelected>>", choose_times)

    # Makes all the stationary labels
    movie_lbl = Label(window, text="Movie:",bg="#077deb", fg="white", font="Arial 12 bold")
    time_lbl = Label(window, text="Times:",bg="#077deb", fg="white", font="Arial 12 bold")
    movie_lbl.grid(row=1, column=0, sticky="WE")
    time_lbl.grid(row=1, column=2, sticky="WE")

    # Makes the labels, buttons and frame for the date
    global date_frame
    date_frame = Frame(window,bg="#077deb")
    date_frame.grid(row=0, column=0, columnspan=3,sticky="WE")
    date_lbl = Label(date_frame, text=f"Date: {new_date.strftime('%d-%m-%y')}",bg="#077deb", fg="white", font="Arial 10 bold")
    date_lbl.grid(row=0, column=1, sticky="WE")
    date_forward = Button(date_frame, text=">", command=future_day)
    date_forward.grid(row=0, column=2, sticky="WE")
    date_backward = Button(date_frame, text="<", command=past_day, state="disabled")
    date_backward.grid(row=0, column=0, sticky="WE")


def future_day():
    '''This function creates a new day with different timeslots'''
    global new_date
    global date_lbl
    date_backward = Button(date_frame, text="<", command=past_day, state="active")
    date_backward.grid(row=0, column=0, sticky="WE")
    # Sets the date label to the current date plus one day
    new_date = new_date + timedelta(days=1)
    date_lbl.config(text=f"Date: {new_date.strftime('%d-%m-%y')}")
    choose_times()


def past_day():
    '''This function goes back to a previous day'''
    global new_date
    #Checks to make sure the day isn't today
    if (new_date - timedelta(days=2)) == date.today():
        date_backward = Button(date_frame, text="<", command=past_day, state="disabled")
        date_backward.grid(row=0, column=0, sticky="WE")
    new_date = new_date - timedelta(days=1)
    #Configures the date label to show the new date
    date_lbl.config(text=f"Date: {new_date.strftime('%d-%m-%y')}")
    choose_times()


def choose_times(*args):
    '''Generates times for the selected movie and current date if not already generated'''
    if movie_selected.get():
        movie = movie_selected.get()
        date_str = new_date.strftime('%d-%m-%y')
        if (movie, date_str) not in stored_times:
            chosen_times = random.sample(TIMES, MOVIES[movie])
            # Format to convert to a time object
            time_format = '%I:%M%p'
            # Creates list and converts them using times chosen
            time_hours = [time.strptime(t, time_format) for t in chosen_times]
            # Sorts the list using the new objects
            chosen_times = [time.strftime(time_format, h) for h in sorted(time_hours)]
            stored_times[(movie, date_str)] = chosen_times
        else:
            chosen_times = stored_times[(movie, date_str)]
        MovieBookings(window, movie, chosen_times)


def btn_clear():
    '''Used to clear all widgets'''
    for widget in window.grid_slaves():
        if int(widget.grid_info()["column"]) == 2 and int(widget.grid_info()["row"]) > 1:
            widget.destroy()


# Main Program
window = Tk()
window.title("Movie Theatre")
window.attributes('-fullscreen',True)
window.configure(bg="#077deb")
main_menu(list(MOVIES.keys()))
window.mainloop()