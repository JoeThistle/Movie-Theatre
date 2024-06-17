#Title: Movie Theatre
#Author: Joe Thistlethwaite
#Purpose: To allow for users to book tickets for a movie
#Version: 1.5
from tkinter import *
from tkinter import ttk
import random
import time

MAX_SEATS = 150
movies = {"Kingsmen": 6,"Oppenheimer": 3,"The Italian Job": 4,"Doctor Who": 3,"Five Nights At Freddy's": 3,"Despicable Me 4": 5}
times = ["10:00am", "10:10am", "12:30pm", "1:40pm", "2:00pm", "2:30pm", "4:00pm", "4:40pm", "6:10pm", "8:00pm"]

class Movie:
    def __init__(self, master, movie_name, times):
        '''This function initialises all the variables'''
        self.master = master
        self.movie_name = movie_name
        self.times = times
        self.create_movie_times()

    def create_movie_times(self):
        '''Creates the times for ticket selection based on movie choice'''
        btn_clear()
        for num, time in enumerate(self.times):
            time_btn = Button(self.master, text=time, command=())
            time_btn.grid(padx=10, pady=10, column=2, row=(num+2), sticky="WE")

def main_menu(movie_list):
    '''This function creates the dropdown menu based off of what movies there are'''
    global drop_box
    global movie_selected
    movie_selected = StringVar()
    drop_box = ttk.Combobox(window, textvariable=movie_selected, state="readonly")
    drop_box['values'] = movie_list
    drop_box.grid(padx=10, pady=10, row=2, column=0,sticky="WE")
    movie_lbl = Label(window, text="Movie:")
    time_lbl = Label(window, text="Times:")
    movie_lbl.grid(row=1, column=0, sticky="WE")
    time_lbl.grid(row=1, column=2, sticky="WE")

def choose_times(*args):
    '''Selects the time slots for the movie'''
    chosen_times = random.sample(times, movies[movie_selected.get()])
    #The following three lines were used from the following link: https://stackoverflow.com/questions/40187525/how-to-sort-a-list-of-times
    #Format to convert to a time object
    time_format = '%I:%M%p'
    #Creates list and converts them using times chosen
    time_hours = [time.strptime(t, time_format) for t in chosen_times]
    #Sorts the list using the new objects
    chosen_times = [time.strftime(time_format, h) for h in sorted(time_hours)]
    Movie(window, movie_selected.get(), chosen_times)
    global prev
    prev = movie_selected.get()

def btn_clear():
    clear = Frame(window)
    clear.grid(padx=10, pady=10,row=2,column=2,rowspan=6,sticky="NESW")

# Main Program
window = Tk()
window.title("Movie Theatre")
window.geometry(newGeometry="250x300")
main_menu(list(movies.keys()))
movie_selected.trace_add("write", choose_times)
window.mainloop()