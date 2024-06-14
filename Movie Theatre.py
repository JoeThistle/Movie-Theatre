#Title: Movie Theatre
#Author: Joe Thistlethwaite
#Purpose: To allow for users to book tickets for a movie
#Version: 1.0
from tkinter import *
from tkinter import ttk
import random
MAX_SEATS = 150
movies = {"Kingsmen":6,"Oppenheimer":3,"The Italian Job":4,"Doctor Who":3,"Five Nights At Freddy's":3,"Despicable Me 4":5}
times = ["10:00am","10:10am","12:30pm","1:40pm","2:00pm","2:30pm","4:00pm","4:40pm","6:10pm","8:00pm"]

class Movie:
    def __init__(self,times,seats=MAX_SEATS,*args):
        '''This function initialises all the variables'''
        self.movie = drop_box.get()
        self.times = times
        self.seats = seats
        self.create_movie_window()
    
    def create_movie_window(self):
        '''Creates the window for ticket selection based on movie choice'''
        self.movie_window = Tk()
        self.movie_window.title(self.movie)
        for i in range(len(self.times)):
            print(i)
        self.movie_window.mainloop()


def dropdown(movie_list):
    '''This function creates the dropdown menu based off of what movies there are'''
    global drop_box
    global movie_selected
    movie_selected = StringVar()
    drop_box = ttk.Combobox(window,textvariable=movie_selected,state="readonly")
    drop_box['values'] = movie_list
    drop_box.grid(padx=10,pady=10,row=2,column=0)

def choose_times(*args):
    '''Selects the time slots for the movie'''
    print("test")
    usable_times = times
    time_slots = []
    for i in range(movies[movie_selected.get()]):
        time_slots.append(random.choice(usable_times))
        usable_times.remove(time_slots[-1])
    Movie(time_slots)

#Main Program
window = Tk()
window.title("Movie Theatre")
dropdown(list(movies.keys()))
movie_selected.trace_add("write",choose_times)
window.mainloop()