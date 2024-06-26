#Title: Movie Theatre
#Author: Joe Thistlethwaite
#Purpose: To allow for users to book tickets for a movie
#Version: 2.8
from tkinter import *
from tkinter import ttk
import random
import time
import json
from datetime import date, timedelta

#Opens the movie data file and sets all the variables
with open("Movie Data.json") as file:
    data = json.loads(file.read())
MAX_SEATS = data["max_seats"]
movies = data["movies&showings"]
times = data["timeslots"]

#Gets the date the program starts at using the systems time
start_date = date.today() + timedelta(days=1)
new_date = start_date
stored_times = {}

class Movie:
    def __init__(self, master, movie_name, times):
        '''This function initialises all the variables'''
        self.master = master
        self.movie_name = movie_name
        self.times = times
        #Creates buttons for the grid
        self.create_movie_times()


    def create_movie_times(self):
        '''Creates the times for ticket selection based on movie choice'''
        btn_clear()
        #Loops and ensures that it will word with any number of movie slots (assuming there are enough times)
        for num, time in enumerate(self.times):
            Button(self.master, text=time, command=self.ticket_booking).grid(padx=10, pady=5, column=2, row=(num+2))
    

    def ticket_booking(self):
        print("Test")


def main_menu(movie_list):
    '''This function creates the dropdown menu based off of what movies there are'''
    global movie_selected
    global date_lbl
    
    #Creates the dropbox along with selecting the times if someone selects a different movie within the drop box
    movie_selected = StringVar()
    movie_drop_box = ttk.Combobox(window, textvariable=movie_selected, state="readonly")
    movie_drop_box['values'] = movie_list
    movie_drop_box.grid(padx=10, pady=5, row=2, column=0, sticky="WE")
    movie_drop_box.bind("<<ComboboxSelected>>", choose_times)
    
    #Makes all the stationary labels
    movie_lbl = Label(window, text="Movie:")
    time_lbl = Label(window, text="Times:")
    movie_lbl.grid(row=1, column=0, sticky="WE")
    time_lbl.grid(row=1, column=2, sticky="WE")

    #Makes the labels, buttons and frame for the date
    global date_frame
    date_frame = Frame(window)
    date_frame.grid(row=0, column=0, columnspan=3)
    date_lbl = Label(date_frame, text=f"Date: {new_date.strftime('%d-%m-%y')}")
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
    #Sets the date label to the current date plus one day
    new_date = new_date + timedelta(days=1)
    date_lbl.config(text=f"Date: {new_date.strftime('%d-%m-%y')}")
    choose_times()

def past_day():
    '''This function goes back to a previous day'''
    global new_date
    if (new_date - timedelta(days=2)) == date.today():
        date_backward = Button(date_frame, text="<", command=past_day, state="disabled")
        date_backward.grid(row=0, column=0, sticky="WE")
    new_date = new_date - timedelta(days=1)
    date_lbl.config(text=f"Date: {new_date.strftime('%d-%m-%y')}")
    choose_times()

def choose_times(*args):
    '''Generates times for the selected movie and current date if not already generated'''
    if movie_selected.get():
        movie = movie_selected.get()
        date_str = new_date.strftime('%d-%m-%y')
        if (movie, date_str) not in stored_times:
            chosen_times = random.sample(times, movies[movie])
            # The following three lines were used from the following link: https://stackoverflow.com/questions/40187525/how-to-sort-a-list-of-times
            # Format to convert to a time object
            time_format = '%I:%M%p'
            # Creates list and converts them using times chosen
            time_hours = [time.strptime(t, time_format) for t in chosen_times]
            # Sorts the list using the new objects
            chosen_times = [time.strftime(time_format, h) for h in sorted(time_hours)]
            stored_times[(movie, date_str)] = chosen_times
        else:
            chosen_times = stored_times[(movie, date_str)]
        
        Movie(window, movie, chosen_times)

def btn_clear():
    for widget in window.grid_slaves():
        if int(widget.grid_info()["column"]) == 2 and int(widget.grid_info()["row"]) > 1:
            widget.destroy()

# Main Program
window = Tk()
window.title("Movie Theatre")
window.geometry("250x275")
main_menu(list(movies.keys()))
window.mainloop()