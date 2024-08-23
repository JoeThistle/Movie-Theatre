#Title: Change Movie Data
#Author: Joe Thistlethwaite
#Purpose: To allow for staff to change movie data
#Version: 2.5

from tkinter import *
from tkinter import ttk
from datetime import datetime
import json
import time

def grab_data():
    '''Takes the data from the json file'''
    global data
    with open("Movie Data.json") as file:
        data = json.loads(file.read())


def showings():
    '''Makes the showings window appear'''
    grid_clear([".back_btn"])
    global movie_selected
    global movies
    global MAX_SHOWINGS
    grab_data()
    #Creates all the labels in showings
    movies = data['movies&showings']
    showing_main_lbl = Label(window,text="Showings",font="bold")
    showing_lbl = Label(window,text="Showing:")
    showing_num_lbl = Label(window,text="Showing Amount:")
    #Sets max showings and creates combobox
    MAX_SHOWINGS = data['MAX_SHOWINGS']
    movie_selected = StringVar()
    movie_drop_box = ttk.Combobox(window, textvariable=movie_selected, state="readonly")
    movie_drop_box['values'] = list(movies.keys())
    showing_main_lbl.grid(row=0,column=0,columnspan=2)
    showing_lbl.grid(row=2,column=0)
    showing_num_lbl.grid(row=2,column=1)
    movie_drop_box.grid(row=3,column=0)
    #Binds it so that if the user selects something a command is run
    movie_drop_box.bind("<<ComboboxSelected>>", show_showings)


def show_showings(*args):
    '''When the user selects an item in the combo box this shows the number of showings'''
    global showings_ent
    #Avoids a memory leak
    try:
        showings_ent.destroy()
    except:
        pass
    num_of_showings = movies[movie_selected.get()]
    showings_ent = Entry(window)
    #I aquired the following line from https://www.geeksforgeeks.org/how-to-set-the-default-text-of-tkinter-entry-widget/
    showings_ent.insert(0, num_of_showings)
    showings_ent.grid(row=3, column=1)
    save_btn = Button(window,text="Save",command=save_showings)
    save_btn.grid(row=1,column=0,columnspan=2,sticky="WE")


def save_showings():
    '''Attempts to save the new amount of showings'''
    current_movie = movie_selected.get()
    global show_error_lbl
    try:
        #Checks the new number isn't more than the max number of showings
        current_showings = int(showings_ent.get())
        if current_showings >= 0 and current_showings <= MAX_SHOWINGS:
            #Avoids a memory leak
            try:
                show_error_lbl.grid_remove()
            except:
                pass
            movies[current_movie] = current_showings
            #Saves the changes
            with open("Movie Data.json","w") as outfile:
                new_data = json.dumps(data,indent=2)
                outfile.write(new_data)
        else:
            try:
                show_error_lbl.grid_remove()
            except:
                pass
    #If they enter an invalid case
            show_error_lbl = Label(window,text="Number must be\nbetween 0 and 6")
            show_error_lbl.grid(row=4,column=1)
    except:
        try:
                show_error_lbl.grid_remove()
        except:
            pass
        show_error_lbl = Label(window,text="Please Enter A Number")
        show_error_lbl.grid(row=4,column=1)


def grid_clear(exceptions):
    '''Clears the grid apart from exceptions'''
    for widget in window.winfo_children():
        if str(widget) not in exceptions:
            widget.destroy()
    #If the window ever ends up with nothing on it the user is sent to the main menu
    if window.winfo_children() == []:
        main_menu()


def change_max_seats():
    '''This Function Changes The Max Seats'''
    global new_max
    global max_ent
    grab_data()
    grid_clear([".back_btn"])
    #Creates the buttons/labels for changing the max seats
    new_max = StringVar()
    max_main_lbl = Label(window,text="Max Seats In Theatre",font="bold")
    save_max_btn = Button(window,text="Save",command=save_max)
    max_lbl = Label(window,text="What is the new maximum: ")
    max_ent = Entry(window,text=new_max)
    max_main_lbl.grid(row=0,column=0,columnspan=2)
    save_max_btn.grid(row=2,column=0,sticky="WE")
    max_lbl.grid(row=1,column=0)
    max_ent.grid(row=1,column=1)


def save_max():
    '''Saves the max seats'''
    grab_data()
    global data
    #Grabs what they are tring to save
    saving = new_max.get()
    try:
        if int(saving) > 0:
            data["max_seats"] = int(saving)
            #Writes it back to the JSON file
            with open("Movie Data.json","w") as outfile:
                data = json.dumps(data,indent=2)
                outfile.write(data)
            max_success = Label(window,text="Saved Successfully",fg="green")
            max_success.grid(row=2,column=1,sticky="WE")
    except:
        #For invalid inputs
        max_fail = Label(window,text="Failed To Save",fg="red")
        max_fail.grid(row=2,column=1,sticky="WE")


def time_changer():
    '''Opens the time changing window'''
    grid_clear([".back_btn"])
    #Creates all labels and buttons that are needed
    times_main_lbl = Label(window,text="Times",font="bold",name="times_main_lbl")
    times_add_btn = Button(window,text="Add Time",width=10,command=add_time)
    remove_times_btn = Button(window,text="Remove Time",width=10,command=remove_time)
    times_main_lbl.grid(row=0,column=0,columnspan=3)
    times_add_btn.grid(row=1,column=0,sticky="WE")
    remove_times_btn.grid(row=1,column=1,sticky="WE")


def add_time():
    '''Allows the user to enter new tiems'''
    grab_data()
    global time_to_add
    global time_add_ent
    grid_clear([".times_main_lbl",".back_btn"])
    #Creates buttons/entries/labels for entering a new times
    time_to_add = StringVar()
    time_add_lbl = Label(window,text="Enter Time To Add:")
    add_tip_lbl = Label(window,text="Please enter in 24 hour\nformat, e.g. 5:00pm = 1700")
    time_add_ent = Entry(window,text=time_to_add)
    save_add_btn = Button(window,text="Add",command=save_time_add)
    time_add_lbl.grid(row=1,column=0)
    add_tip_lbl.grid(row=2,column=0,columnspan=2)
    time_add_ent.grid(row=1,column=1)
    save_add_btn.grid(row=1,column=2)


def save_time_add():
    '''Saves the new movie to the json file'''
    grab_data()
    global data
    time_choice = time_to_add.get()
    try:
        #Validates that the time is in correct 24hr format
        if len(time_choice) == 4 and int(time_choice[-2:]) < 60 and int(time_choice) >= 0 and int(time_choice) < 2400:
            time_choice = datetime.strptime(time_choice, "%H%M")
            time_choice = str(time_choice.strftime("%I:%M%p"))
            #Adds the new time to the data and then changes it to 12hr time before sorting them
            data["timeslots"].append(time_choice)
            format = '%I:%M%p'
            time_hours = [time.strptime(t, format) for t in data["timeslots"]]
            sorted_times = [time.strftime(format, h) for h in sorted(time_hours)]
            data["timeslots"] = sorted_times
            #Saves the sorted data to the JSON file
            with open("Movie Data.json","w") as outfile:
                    data = json.dumps(data,indent=2)
                    outfile.write(data)
            time_add_ent.delete(0, 'end')
            #Checks and deletes labels if they are already there before creating a new one
            for widget in window.winfo_children():
                if str(widget) == ".success" or str(widget) == ".fail":
                    widget.destroy()
            success_lbl = Label(window,text="Success",fg="green",name="success")
            success_lbl.grid(row=2,column=2)
    #If something goes wrong with the new input
        else:
            raise ValueError
    except:
        for widget in window.winfo_children():
            if str(widget) == ".success" or str(widget) == ".fail":
                widget.destroy()
        fail_lbl = Label(window,text="Error",fg="red",name="fail")
        fail_lbl.grid(row=2,column=2)


def remove_time():
    '''Sets up the GUI for removing movies'''
    global time_removing
    grab_data()
    times = data['timeslots']
    time_removing = StringVar()
    grid_clear([".times_main_lbl",".back_btn"])
    #Makes the combobox with all the current times
    times_box = ttk.Combobox(window, textvariable=time_removing, state="readonly")
    times_box['values'] = times
    times_box.grid(row=1,column=0)
    time_remove_btn = Button(window,text="Remove",command=del_time)
    time_remove_btn.grid(row=1,column=1)


def del_time():
    '''Deletes the time from the json file'''
    try:
        new_data = data["timeslots"].remove(time_removing.get())
        #Saves the time they wish to remove and deletes it
        with open("Movie Data.json","w") as outfile:
                new_data = json.dumps(data,indent=2)
                outfile.write(new_data)
        remove_time()
    except:
        pass


def movie_main():
    '''Main menu for removing movies'''
    grid_clear([".back_btn"])
    #Creates everything for editing the movies
    movies_main_lbl = Label(window,text="Movies",font="bold",name="movies_main_lbl")
    movies_add_btn = Button(window,text="Add Movie",width=12,command=add_movie)
    movies_remove_btn = Button(window,text="Remove Movie",width=12,command=remove_movie)
    movies_main_lbl.grid(row=0,column=0,columnspan=3)
    movies_add_btn.grid(row=1,column=0,sticky="WE")
    movies_remove_btn.grid(row=1,column=1,sticky="WE")


def remove_movie():
    '''Sets up the GUI for removing movies'''
    global movie_removing
    grab_data()
    movies = list(data['movies&showings'].keys())
    movie_removing = StringVar()
    grid_clear([".movies_main_lbl",".back_btn"])
    #Makes the combobox with all the current movies
    movies_box = ttk.Combobox(window, textvariable=movie_removing, state="readonly")
    movies_box['values'] = movies
    movies_box.grid(row=1,column=0)
    movie_remove_btn = Button(window,text="Remove",command=del_movie)
    movie_remove_btn.grid(row=1,column=1)


def del_movie():
    '''Deletes the movie from the json file'''
    try:
        #Deletes the movie they selected from the dictionary
        new_data = data['movies&showings'].pop(movie_removing.get())
        #Saves the new dictionary
        with open("Movie Data.json","w") as outfile:
                new_data = json.dumps(data,indent=2)
                outfile.write(new_data)
        remove_movie()
    except:
        pass


def add_movie():
    '''Asks the user what movie they wish to add'''
    grab_data()
    global movie_adding
    global movie_add_ent
    grid_clear([".movies_main_lbl",".back_btn"])
    #Creates GUI for adding movies
    movie_adding = StringVar()
    movie_add_lbl = Label(window,text="Enter Movie To Add:")
    movie_add_ent = Entry(window,text=movie_adding)
    save_add_btn = Button(window,text="Add",command=save_movie_add)
    movie_add_lbl.grid(row=1,column=0)
    movie_add_ent.grid(row=1,column=1)
    save_add_btn.grid(row=1,column=2)


def save_movie_add():
    '''Saves the new movie to the json file'''
    try:
        #Saves the movie they are adding and sets the showing number to 0
        new_data = data['movies&showings'][movie_adding.get()] = 0
        with open("Movie Data.json","w") as outfile:
                new_data = json.dumps(data,indent=2)
                outfile.write(new_data)
        add_movie()
    except:
        pass


def main_menu():
    '''Main menu function'''
    global back_btn
    #Creates the buttons for the main window.
    main_lbl = Label(window,text="What do you wish to change?")
    showings_btn = Button(window,text="Showings",width=8,command=showings)
    time_btn = Button(window,text="Time Slots",width=8,command=time_changer)
    movie_btn = Button(window,text="Movies",width=8,command=movie_main)
    seats_btn = Button(window,text="Max Seats",width=8,command=change_max_seats)
    back_btn = Button(window,text="Back",command=lambda:grid_clear([]), name="back_btn")
    back_btn.grid(row=5,column=0,columnspan=4,sticky="WE")
    main_lbl.grid(row=0,column=0,columnspan=4)
    showings_btn.grid(row=1,column=0)
    time_btn.grid(row=1,column=1)
    movie_btn.grid(row=1,column=2)
    seats_btn.grid(row=1,column=3)
    

#Main Program
window = Tk()
window.title("Movie Data")
window.grab_set()
window.geometry("300x325")
main_menu()
window.mainloop()