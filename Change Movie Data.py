#Title: Change Movie Data
#Author: Joe Thistlethwaite
#Purpose: To allow for staff to change movie data
#Version: 1.8

from tkinter import *
from tkinter import ttk
import json

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
    movies = data['movies&showings']
    showing_main_lbl = Label(window,text="Showings",font="bold")
    showing_lbl = Label(window,text="Showing:")
    showing_num_lbl = Label(window,text="Showing Amount:")
    MAX_SHOWINGS = data['MAX_SHOWINGS']
    movie_selected = StringVar()
    movie_drop_box = ttk.Combobox(window, textvariable=movie_selected, state="readonly")
    movie_drop_box['values'] = list(movies.keys())
    showing_main_lbl.grid(row=0,column=0,columnspan=2)
    showing_lbl.grid(row=2,column=0)
    showing_num_lbl.grid(row=2,column=1)
    movie_drop_box.grid(row=3,column=0)
    movie_drop_box.bind("<<ComboboxSelected>>", show_showings)


def show_showings(*args):
    '''When the user selects an item in the combo box this shows the number of showings'''
    global showings_ent
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
        current_showings = int(showings_ent.get())
        if current_showings >= 0 and current_showings <= MAX_SHOWINGS:
            try:
                show_error_lbl.grid_remove()
            except:
                pass
            movies[current_movie] = current_showings
            with open("Movie Data.json","w") as outfile:
                new_data = json.dumps(data,indent=2)
                outfile.write(new_data)
        else:
            try:
                show_error_lbl.grid_remove()
            except:
                pass
            show_error_lbl = Label(window,text="Number must be\nbetween 0 and 6")
            show_error_lbl.grid(row=3,column=1)
    except:
        try:
                show_error_lbl.grid_remove()
        except:
            pass
        show_error_lbl = Label(window,text="Please Enter A Number")
        show_error_lbl.grid(row=3,column=1)


def grid_clear(exceptions):
    '''Clears the grid apart from the back button'''
    for widget in window.winfo_children():
        if str(widget) not in exceptions:
            widget.destroy()
    #If the window ever ends up with nothing on it the user is sent to the main menu
    if window.winfo_children() == []:
        main_menu()


def time_changer():
    '''Opens the time changing window'''
    grid_clear([".back_btn"])
    times_main_lbl = Label(window,text="Times",font="bold",name="times_main_lbl")
    times_add_btn = Button(window,text="Add Time",width=10,command=add_time)
    remove_times_btn = Button(window,text="Remove Time",width=10,command=remove_time)
    times_main_lbl.grid(row=0,column=0,columnspan=3)
    times_add_btn.grid(row=1,column=0,sticky="WE")
    remove_times_btn.grid(row=1,column=1,sticky="WE")


def add_time():
    ''''''
    grid_clear([".times_main_lbl",".back_btn"])


def remove_time():
    ''''''
    global time_removing
    grab_data()
    times = data['timeslots']
    time_removing = StringVar()
    grid_clear([".times_main_lbl",".back_btn"])
    times_box = ttk.Combobox(window, textvariable=time_removing, state="readonly")
    times_box['values'] = times
    times_box.grid(row=1,column=0)
    time_remove_btn = Button(window,text="Remove",command=del_time)
    time_remove_btn.grid(row=1,column=1)


def del_time():
    try:
        new_data = data["timeslots"].remove(time_removing.get())
        with open("Movie Data.json","w") as outfile:
                new_data = json.dumps(data,indent=2)
                outfile.write(new_data)
        remove_time()
    except:
        pass




def main_menu():
    global back_btn
    main_lbl = Label(window,text="What do you wish to change?")
    showings_btn = Button(window,text="Showings",width=8,command=showings)
    time_btn = Button(window,text="Time Slots",width=8,command=time_changer)
    back_btn = Button(window,text="Back",command=lambda:grid_clear([]), name="back_btn")
    back_btn.grid(row=4,column=0,columnspan=2,sticky="WE")
    main_lbl.grid(row=0,column=0,columnspan=2)
    time_btn.grid(row=1,column=1)
    showings_btn.grid(row=1,column=0)
    

window = Tk()
window.title("Movie Data")
window.geometry("300x325")
main_menu()
window.mainloop()