

# -*- coding: utf8 -*-
'''
Title:  Student Organiser
Project: Student Organiser
Author: Chester Lloyd
Date Created: 05-08-2016
'''
from __future__ import division
from tkinter import *
from tkinter import ttk
import random
#import tkFont
#import ttk
import os
#import messagebox
import time
import sqlite3
import webbrowser
from datetime import datetime, date
import os.path

class StudentOrganiser(Tk):

    def __init__(self):
        Tk.__init__(self)

        self.title(" Student Organiser")
#        self.iconbitmap('favicon.ico')

        # Configure the program with external image files for each button
        self.greenAdd = PhotoImage(file="buttons/green_add.gif")
        self.blueAdd = PhotoImage(file="buttons/blue_add.gif")
        self.yellowAdd = PhotoImage(file="buttons/yellow_add.gif")
        self.redAdd = PhotoImage(file="buttons/red_add.gif")
        
        self.greenUp = PhotoImage(file="buttons/green_up.gif")
        self.blueUp = PhotoImage(file="buttons/blue_up.gif")
        self.yellowUp = PhotoImage(file="buttons/yellow_up.gif")
        self.redUp = PhotoImage(file="buttons/red_up.gif")
        
        self.greenDown = PhotoImage(file="buttons/green_down.gif")
        self.blueDown = PhotoImage(file="buttons/blue_down.gif")
        self.yellowDown = PhotoImage(file="buttons/yellow_down.gif")
        self.redDown = PhotoImage(file="buttons/red_down.gif")
        
        self.greenDone = PhotoImage(file="buttons/green_done.gif")
        self.blueDone = PhotoImage(file="buttons/blue_done.gif")
        self.yellowDone = PhotoImage(file="buttons/yellow_done.gif")
        self.redDone = PhotoImage(file="buttons/red_done.gif")

        self.greenDelete = PhotoImage(file="buttons/green_delete.gif")
        self.blueDelete = PhotoImage(file="buttons/blue_delete.gif")
        self.yellowDelete = PhotoImage(file="buttons/yellow_delete.gif")
        self.redDelete = PhotoImage(file="buttons/red_delete.gif")

        #self.greenRemove = PhotoImage(file="buttons/green_remove.gif")
        #self.blueRemove = PhotoImage(file="buttons/blue_remove.gif")
        #self.yellowRemove = PhotoImage(file="buttons/yellow_remove.gif")
        #self.redRemove = PhotoImage(file="buttons/red_remove.gif")
        
        self.greenBack = PhotoImage(file="buttons/green_back.gif")
        self.blueBack = PhotoImage(file="buttons/blue_back.gif")
        self.yellowBack = PhotoImage(file="buttons/yellow_back.gif")
        self.redBack = PhotoImage(file="buttons/red_back.gif")

        self.greenSave = PhotoImage(file="buttons/green_save.gif")
        self.blueSave = PhotoImage(file="buttons/blue_save.gif")
        self.yellowSave = PhotoImage(file="buttons/yellow_save.gif")
        self.redSave = PhotoImage(file="buttons/red_save.gif")

        self.greenEdit = PhotoImage(file="buttons/green_edit.gif")
        self.blueEdit = PhotoImage(file="buttons/blue_edit.gif")
        self.yellowEdit = PhotoImage(file="buttons/yellow_edit.gif")
        self.redEdit = PhotoImage(file="buttons/red_edit.gif")           

        # Create global page counter variables
        self.ovpage=0
        self.hwpage=0
        self.cwpage=0
        self.expage=0

        # Set default insert mode as False
        # (will insert tasks unless value becomes true and will allow modifying them)
        self.editPage=False

        # Set default sorting permission to allowed (False)
        self.outside=False

        # Disallow altering the size of the program's window
        self.resizable(width=False, height=False)

        # Insert a canvas to fill the entire area of the program's window
        self.canvas = Canvas(self, width=575, height=380, bg="#FFFFFF")
        self.canvas.pack()

        # Define global fonts
        self.tab_font = font.Font(family="Arial", size=15, weight="normal")
        self.box_heading_font = font.Font(family="Arial", size=12, weight="normal")
        self.box_content_font = font.Font(family="Arial", size=10, weight="bold")
        self.body_font = font.Font(family="Arial", size=12, weight="normal")
        self.header_font = font.Font(family="Arial", size=12, weight="bold")

        # Check if the database file exists.
        # If it does not, then create a databse with the following tasks table
        databasePresent = os.path.isfile("./tasks.db")
        if databasePresent == False:
            conn = sqlite3.connect('tasks.db')
            conn.execute('''CREATE TABLE TASKS
                   (ID INT PRIMARY KEY         NOT NULL,
                   TASK               TEXT     NOT NULL,
                   SUBJECT            TEXT     NOT NULL,
                   DATE               DATE     NOT NULL,
                   TAB                TEXT     NOT NULL,
                   NOTES              TEXT);''')
            conn.close()

        self.menu_bar()
        self.setup_overview()

    def menu_bar(self):
        # Creates the menu bar
        menu_bar = Menu(self)
        afile = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=afile)
        afile.add_command(label="New Task", command=self.add_item)
        afile.add_command(label="Home", command=self.setup_overview)
        afile.add_separator()
        afile.add_command(label="Exit", command=self.close)
        '''
        bhelp = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=bhelp)
        bhelp.add_command(label="About", command=self.donothing)
        bhelp.add_separator()
        bhelp.add_command(label="Help", command=self.donothing)
        '''
        csort = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Sort", menu=csort)
        csort.add_command(label="Time: Soonest (Default)", command=self.sort_1)        
        csort.add_command(label="Time: Oldest", command=self.sort_2)
        csort.add_command(label="Time: Task added", command=self.sort_7)
        
        csort.add_separator()        
        csort.add_command(label="Task: A-Z", command=self.sort_3)        
        csort.add_command(label="Task: Z-A", command=self.sort_4)
        csort.add_separator()        
        csort.add_command(label="Subject: A-Z", command=self.sort_5)        
        csort.add_command(label="Subject: Z-A", command=self.sort_6)        
        
        ddata = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Information", menu=ddata)
        menu_map = Menu(self)
        menu_map.add_command(label="St George's Academy", command=self.map_sga)
        menu_map.add_command(label="Carre's Grammar School", command=self.map_cgs)
        ddata.add_cascade(label="School Maps", menu=menu_map)
        ddata.add_command(label="Contact Details", command=self.contact)
        ddata.add_command(label="Useful Websites", command=self.websites)
        
        '''
        egenerate = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Generate", menu=egenerate)
        egenerate.add_command(label="Fill Database", command=self.generate_sample_data)
        egenerate.add_command(label="Add Sample Task", command=self.generate_sample_task)  
        egenerate.add_command(label="Nuke Database", command=self.nuke_database)
        '''
        self.config(menu=menu_bar)

    def close(self):
        # Closes the program
        self.destroy()

    def draw_title_bar(self):
        # Create a diagnal shadow behind the title bar
        self.canvas.create_rectangle(0, 45, 605, 5, fill="#f1f1f2", outline="#f1f1f2")
        self.canvas.create_rectangle(0, 44, 604, 4, fill="#e4e4e5", outline="#e4e4e5")
        self.canvas.create_rectangle(0, 43, 603, 3, fill="#d7d7d9", outline="#d7d7d9")
        self.canvas.create_rectangle(0, 42, 602, 2, fill="#cacacd", outline="#cacacd")
        self.canvas.create_rectangle(0, 41, 601, 1, fill="#bdbdc0", outline="#bdbdc0")
        #self.canvas.create_rectangle(0, 40, 600, 0, fill="#4caf50", outline="#4caf50")

    def draw_tabs(self):
        # Creates the four tabs used for selecting each page
        # TAB 1: Overview
        self.canvas.create_rectangle(33, 45, 158, 59, fill="#e0e0e0", outline="#e0e0e0")
        self.canvas.create_rectangle(32, 44, 157, 58, fill="#ededed", outline="#ededed")
        self.canvas.create_rectangle(31, 20, 156, 57, fill="#f9f9f9", outline="#f9f9f9")
        self.canvas.create_rectangle(30, 20, 155, 56, fill="#FFFFFF", outline="#FFFFFF")

        # TAB 2: Homework
        self.canvas.create_rectangle(163, 45, 288, 59, fill="#e0e0e0", outline="#e0e0e0")
        self.canvas.create_rectangle(162, 44, 287, 58, fill="#ededed", outline="#ededed")
        self.canvas.create_rectangle(161, 20, 286, 57, fill="#f9f9f9", outline="#f9f9f9")
        self.canvas.create_rectangle(160, 20, 285, 56, fill="#FFFFFF", outline="#FFFFFF")

        # TAB 3: Coursework
        self.canvas.create_rectangle(293, 45, 418, 59, fill="#e0e0e0", outline="#e0e0e0")
        self.canvas.create_rectangle(292, 44, 417, 58, fill="#ededed", outline="#ededed")
        self.canvas.create_rectangle(291, 20, 416, 57, fill="#f9f9f9", outline="#f9f9f9")
        self.canvas.create_rectangle(290, 20, 415, 56, fill="#FFFFFF", outline="#FFFFFF")

        # TAB 4: Exams
        self.canvas.create_rectangle(423, 45, 548, 59, fill="#e0e0e0", outline="#e0e0e0")
        self.canvas.create_rectangle(422, 44, 547, 58, fill="#ededed", outline="#ededed")
        self.canvas.create_rectangle(421, 20, 546, 57, fill="#f9f9f9", outline="#f9f9f9")
        self.canvas.create_rectangle(420, 20, 545, 56, fill="#FFFFFF", outline="#FFFFFF")

        # The buttons that link the tab to the correct function
        # BUTTON 1: Overview
        button_overview = Button(self, text="Overview", font=self.tab_font, command=self.setup_overview, anchor = W)
        button_overview.configure(border=0, relief=FLAT, fg="#4caf50", activeforeground="#4caf50", bg="white", activebackground="white")   
        button_overview_window = self.canvas.create_window(46, 20, anchor=NW, window=button_overview)

        # BUTTON 2: Homework
        button_homework = Button(self, text="Homework", font=self.tab_font, command=self.setup_homework, anchor = W)
        button_homework.configure(border=0, relief=FLAT, fg="#4472C4", activeforeground="#4472C4", bg="white", activebackground="white")   
        button_homework_window = self.canvas.create_window(173, 20, anchor=NW, window=button_homework)

        # BUTTON 3: Coursework
        button_coursework = Button(self, text="Coursework", font=self.tab_font, command=self.setup_coursework, anchor = W)
        button_coursework.configure(border=0, relief=FLAT, fg="#ff9800", activeforeground="#ff9800", bg="white", activebackground="white")   
        button_coursework_window = self.canvas.create_window(298, 20, anchor=NW, window=button_coursework)

        # BUTTON 4: Exams
        button_exams = Button(self, text="Exams", font=self.tab_font, command=self.setup_exams, anchor = W)
        button_exams.configure(border=0, relief=FLAT, fg="#ff5722", activeforeground="#ff5722", bg="white", activebackground="white")   
        button_exams_window = self.canvas.create_window(449, 20, anchor=NW, window=button_exams)

    def setup_overview(self):
        self.tab = "Overview"
        self.setup_data()
        
    def setup_homework(self):
        self.tab = "Homework"
        self.setup_data()        
        
    def setup_coursework(self):
        self.tab = "Coursework"
        self.setup_data()

    def setup_exams(self):
        self.tab = "Exam"
        self.setup_data()

    def setup_data(self):
        # Set up the function's variables based on the current tab
        if self.tab == "Overview":
            self.colour = "#4caf50"
            self.rowColour = "#c8e6c9"
            self.add = self.greenAdd
            self.delete = self.greenDelete
            #self.remove = self.greenRemove
            self.hwpage=0
            self.cwpage=0
            self.expage=0
            
        if self.tab == "Homework":
            self.colour = "#4472C4"
            self.rowColour = "#bbdefb"
            self.add = self.blueAdd
            self.delete = self.blueDelete
            #self.remove = self.blueRemove            
            #self.path = "./users/test/homework.txt"
            self.ovpage=0
            self.cwpage=0
            self.expage=0
            
        if self.tab == "Coursework":
            self.colour = "#ff9800"
            self.rowColour = "#ffe0b2"
            self.add = self.yellowAdd
            self.delete = self.yellowDelete
            #self.remove = self.yellowRemove            
            #self.path = "./users/test/coursework.txt"
            self.ovpage=0
            self.hwpage=0
            self.expage=0
            
        if self.tab == "Exam":
            self.colour = "#ff5722"
            self.rowColour = "#ffcdd2"
            self.add = self.redAdd
            self.delete = self.redDelete
            #self.remove = self.redRemove        
            #self.path = "./users/test/exams.txt"
            self.ovpage=0
            self.hwpage=0
            self.cwpage=0
            
        self.canvas.delete(ALL)
        self.draw_title_bar()
        self.canvas.create_rectangle(0, 40, 600, 0, fill=self.colour, outline=self.colour)
        self.draw_tabs()

        button_add = Button(self, image=self.add, command=self.add_item, anchor = W)
        button_add.configure(border=0, relief = FLAT, highlightthickness=0)
        button_add_window = self.canvas.create_window(502, 315, anchor=NW, window=button_add)
        # Creates a grid of 3 x 4 of set width entry boxes to display data for the tasks
        
        # TASK NAME           SUBJECT   DATE
        # ##################  ########  ######
        # ##################  ########  ######
        # ##################  ########  ######
        # ##################  ########  ######

        # Row 1           
        self.name_1 = Entry(self,width=45)
        self.name_1.configure(border=0, relief=FLAT, bg="white")
        name_1_window = self.canvas.create_window(40, 97, anchor=NW, window=self.name_1)
        self.subject_1 = Entry(self,width=20)
        self.subject_1.configure(border=0, relief=FLAT, bg="white")
        subject_1_window = self.canvas.create_window(320, 97, anchor=NW, window=self.subject_1)
        self.date_1 = Entry(self,width=15)
        self.date_1.configure(border=0, relief=FLAT, bg="white")
        date_1_window = self.canvas.create_window(450, 97, anchor=NW, window=self.date_1)

        # Row 2           
        self.name_2 = Entry(self,width=45)
        self.name_2.configure(border=0, relief=FLAT, bg="white")
        name_2_window = self.canvas.create_window(40, 157, anchor=NW, window=self.name_2)
        self.subject_2 = Entry(self,width=20)
        self.subject_2.configure(border=0, relief=FLAT, bg="white")
        subject_2_window = self.canvas.create_window(320, 157, anchor=NW, window=self.subject_2)
        self.date_2 = Entry(self,width=15)
        self.date_2.configure(border=0, relief=FLAT, bg="white")
        date_2_window = self.canvas.create_window(450, 157, anchor=NW, window=self.date_2)
        
        # Row 3           
        self.name_3 = Entry(self,width=45)
        self.name_3.configure(border=0, relief=FLAT, bg="white")
        name_3_window = self.canvas.create_window(40, 217, anchor=NW, window=self.name_3)
        self.subject_3 = Entry(self,width=20)
        self.subject_3.configure(border=0, relief=FLAT, bg="white")
        subject_3_window = self.canvas.create_window(320, 217, anchor=NW, window=self.subject_3)
        self.date_3 = Entry(self,width=15)
        self.date_3.configure(border=0, relief=FLAT, bg="white")
        date_3_window = self.canvas.create_window(450, 217, anchor=NW, window=self.date_3)
        
        # Row 4
        self.name_4 = Entry(self,width=45)
        self.name_4.configure(border=0, relief=FLAT, bg="white")
        name_4_window = self.canvas.create_window(40, 277, anchor=NW, window=self.name_4)
        self.subject_4 = Entry(self,width=20)
        self.subject_4.configure(border=0, relief=FLAT, bg="white")
        subject_4_window = self.canvas.create_window(320, 277, anchor=NW, window=self.subject_4)
        self.date_4 = Entry(self,width=15)
        self.date_4.configure(border=0, relief=FLAT, bg="white")
        date_4_window = self.canvas.create_window(450, 277, anchor=NW, window=self.date_4)

        # Clears the contents of every row (entry box)
        self.name_1.delete(0, END)
        self.subject_1.delete(0, END)
        self.date_1.delete(0, END)
        self.name_2.delete(0, END)
        self.subject_2.delete(0, END)
        self.date_2.delete(0, END)
        self.name_3.delete(0, END)
        self.subject_3.delete(0, END)
        self.date_3.delete(0, END)
        self.name_4.delete(0, END)
        self.subject_4.delete(0, END)
        self.date_4.delete(0, END)

        # Get tasks from the database based on the tab selected        
        conn = sqlite3.connect('tasks.db')
        self.tasks = []
        if self.tab == "Overview":
            cursor = conn.execute("SELECT * FROM tasks ORDER BY DATE ASC")
        else:
            cursor = conn.execute("SELECT * FROM tasks WHERE TAB='"+str(self.tab)+"' ORDER BY DATE ASC")

        # Add data selected to a 2D tasks array
        for row in cursor:
            single = []                 #Create an array for each task
            single.append(row[1])       #Add name
            single.append(row[2])       #Add subject
            # Reverse the date format (YYYY/MM/DD => DD/MM/YYYY)
            dateData = (row[3].strip().split('/'))
            dateDay = dateData[2]
            dateMonth = dateData[1]
            dateYear = dateData[0]
            dateNew = dateDay + "/" + dateMonth + "/" + dateYear
            single.append(dateNew)      #Add date
            single.append(row[4])       #Add type
            single.append(row[0])       #Add ID
            single.append(row[5])       #Add notes
            self.tasks.append(single)   #Create an array of each task's array
        conn.close()
   
        # Get number of tasks
        self.tasknumber = 0
        for i in self.tasks:
            self.tasknumber += 1
        # Get number of pages
        self.setsremainder = self.tasknumber % 4
        if self.tasknumber == 0:
            self.sets = 0
        elif self.tasknumber < 5:
            self.sets = 1
        elif self.setsremainder > 0:
            self.sets = self.tasknumber // 4
            self.sets += 1
        elif self.setsremainder == 0:
            self.sets = self.tasknumber // 4
        
        # Create sets of data
        # All tasks will be divided into groups of upto 4, where only the final group may be less than 4
        # A progress array is made using pointers that can be used to select the relevant tasks from an array
        # when given a page number
        self.progress=[]
        for i in range(self.sets):
            self.mintask = (i) * 4
            self.maxtask = self.mintask + 3
            self.progress.append(self.mintask)
            self.progress.append(self.maxtask)
        self.load_rows()
      
    def load_rows(self):
        # Allow page sorting
        self.outside=False
        self.canvas.delete("page")
        # Set up the function's variables based on the current tab        
        if self.tab == "Overview":
            self.page = self.ovpage
            self.up = self.greenUp
            self.down = self.greenDown
            #self.save = self.greenSave
            self.back = self.greenBack
            self.edit = self.greenEdit
        if self.tab == "Homework":
            self.page = self.hwpage
            self.up = self.blueUp
            self.down = self.blueDown
            #self.save = self.blueSave
            self.back = self.blueBack
            self.edit = self.blueEdit
        if self.tab == "Coursework":
            self.page = self.cwpage
            self.up = self.yellowUp
            self.down = self.yellowDown
            #self.save = self.yellowSave
            self.back = self.yellowBack
            self.edit = self.yellowEdit
        if self.tab == "Exam":
            self.page = self.expage
            self.up = self.redUp
            self.down = self.redDown
            #self.save = self.redSave
            self.back = self.redBack
            self.edit = self.redEdit
     
        # Change state of up/down buttons based on the current page
        if self.page == 0:
            self.up_state = "disabled"
            self.down_state = "active"
        if self.page > 0:
            self.up_state = "active"
            self.down_state = "active"
        if self.page == ((self.sets)*2)-2:
            self.up_state = "normal"
            self.down_state = "disabled"
        if self.sets == 1:
            self.up_state = "disabled"
            self.down_state = "disabled"
        if self.tasknumber == 0:
            self.up_state = "disabled"
            self.down_state = "disabled"

        # Clear contents of every row (entry box)
        self.name_1.delete(0, END)
        self.subject_1.delete(0, END)
        self.date_1.delete(0, END)
        self.name_2.delete(0, END)
        self.subject_2.delete(0, END)
        self.date_2.delete(0, END)
        self.name_3.delete(0, END)
        self.subject_3.delete(0, END)
        self.date_3.delete(0, END)
        self.name_4.delete(0, END)
        self.subject_4.delete(0, END)
        self.date_4.delete(0, END)
    
        # Add up/down buttons
        button_up = Button(self, image=self.up, command=self.page_up, anchor = W)
        button_up.configure(border=0, relief = FLAT, state=self.up_state, highlightthickness=0)
        button_up_window = self.canvas.create_window(30, 315, anchor=NW, window=button_up)

        button_down= Button(self, image=self.down, command=self.page_down, anchor = W)
        button_down.configure(border=0, relief = FLAT, state=self.down_state, highlightthickness=0)
        button_down_window = self.canvas.create_window(80, 315, anchor=NW, window=button_down)

#        button_save = Button(self, image=self.save, command=self.save_changes, anchor = W)
#        button_save.configure(border=0, relief = FLAT, highlightthickness=0)
#        button_save_window = self.canvas.create_window(452, 315, anchor=NW, window=button_save)        

        # Generate text for the current page and insert into the lower center
        self.pageText="Page "+str((self.page//2)+1)+" of "+str(self.sets)
        self.canvas.create_text(280, 340, text=self.pageText, fill="grey", tags="page")

        # Set each entry box to use black text
        self.name_1.configure(fg="#000000")
        self.subject_1.configure(fg="#000000")
        self.date_1.configure(fg="#000000")
        self.name_2.configure(fg="#000000")
        self.subject_2.configure(fg="#000000")
        self.date_2.configure(fg="#000000")
        self.name_3.configure(fg="#000000")
        self.subject_3.configure(fg="#000000")
        self.date_3.configure(fg="#000000")
        self.name_4.configure(fg="#000000")
        self.subject_4.configure(fg="#000000")
        self.date_4.configure(fg="#000000")

        # Get the current date
        todayDate = (time.strftime("%d/%m/%Y"))
        currentDate = time.strptime(todayDate, "%d/%m/%Y")  

        # If there are no tasks to display:
        #   Show the text 'No tasks to display'
        #   Remove the page counter from the page
        if self.tasknumber == 0:
            self.canvas.delete("page")
            self.canvas.create_text(290, 210, text="No tasks to display", fill="black", tags="noData")
            return                        

        # If a page isn't full:
        #   Select every task from the array by passing the page number and progress array
        #   and add it to a set array
        elif self.tasknumber<=self.progress[self.page+1] and self.tasknumber>self.progress[self.page]:
            self.canvas.delete("noData") 
            self.set=[]
            for i in self.tasks[self.progress[self.page]:self.tasknumber]:
                self.set.append(i)
            # Calculate number of full rows
            self.fullRows = self.tasknumber - self.progress[self.page]

            # Insert rows
            self.t = 80
            self.b = 130
            # Create coloured row boxes
            for i in range(self.fullRows):
                self.canvas.create_rectangle(30, self.b+2, 548, self.t+1, fill="#f9f9f9", outline="#f9f9f9", tags="rowBox")
                self.canvas.create_rectangle(30, self.b, 546, self.t, fill="white", outline=self.rowColour, width=2, tags="rowBox")
                self.t += 60
                self.b += 60

            if self.fullRows == 1:
            # Split previous array into 1 array (for the first row)                
                row1 = []
                for i in self.set[0]:
                    row1.append(i)

                # Append the ID of every task on the page to an array
                self.sets_id=[]
                self.sets_id.append(row1[4])

                # Append the task type of every task on the page to an array
                self.sets_type=[]
                self.sets_type.append(row1[3])

                # Insert data for the tasks into the relevant entry boxes
                self.name_1.insert(INSERT, row1[0])      
                self.subject_1.insert(INSERT, row1[1])
                self.date_1.insert(INSERT, row1[2])
                
                # Get current date
                taskDate_1 = time.strptime(row1[2], "%d/%m/%Y")
                taskOverdue_1 = currentDate > taskDate_1

                # Change text colour to red for any task overdue
                if taskOverdue_1 == True:
                    self.name_1.configure(fg="#f44336")
                    self.subject_1.configure(fg="#f44336")
                    self.date_1.configure(fg="#f44336")
                
                button_remove_1 = Button(self, image=self.edit, command=lambda: self.load_notes(0), anchor = W)
                button_remove_1.configure(border=0, relief = FLAT, highlightthickness=0)
                button_remove_1_window = self.canvas.create_window(520, 94, anchor=NW, window=button_remove_1, tags="rowBox")   
                return

            if self.fullRows == 2:
            # Split previous array into 2 arrays (1 per full row)
                row1 = []
                for i in self.set[0]:
                    row1.append(i)
                row2 = []
                for i in self.set[1]:
                    row2.append(i)

                # Append the ID of every task on the page to an array
                self.sets_id=[]
                self.sets_id.append(row1[4])
                self.sets_id.append(row2[4])

                # Append the task type of every task on the page to an array
                self.sets_type=[]
                self.sets_type.append(row1[3])
                self.sets_type.append(row2[3])

                # Insert data for the tasks into the relevant entry boxes
                self.name_1.insert(INSERT, row1[0])      
                self.subject_1.insert(INSERT, row1[1])
                self.date_1.insert(INSERT, row1[2])            
                self.name_2.insert(INSERT, row2[0])      
                self.subject_2.insert(INSERT, row2[1])
                self.date_2.insert(INSERT, row2[2])
                
                # Get current date
                taskDate_1 = time.strptime(row1[2], "%d/%m/%Y")
                taskOverdue_1 = currentDate > taskDate_1
                taskDate_2 = time.strptime(row2[2], "%d/%m/%Y")
                taskOverdue_2 = currentDate > taskDate_2
                
                # Change text colour to red for any task overdue
                if taskOverdue_1 == True:
                    self.name_1.configure(fg="#f44336")
                    self.subject_1.configure(fg="#f44336")
                    self.date_1.configure(fg="#f44336")
                if taskOverdue_2 == True:
                    self.name_2.configure(fg="#f44336")
                    self.subject_2.configure(fg="#f44336")
                    self.date_2.configure(fg="#f44336")

                button_remove_1 = Button(self, image=self.edit, command=lambda: self.load_notes(0), anchor = W)
                button_remove_1.configure(border=0, relief = FLAT, highlightthickness=0)
                button_remove_1_window = self.canvas.create_window(520, 94, anchor=NW, window=button_remove_1, tags="rowBox")

                button_remove_2 = Button(self, image=self.edit, command=lambda: self.load_notes(1), anchor = W)
                button_remove_2.configure(border=0, relief = FLAT, highlightthickness=0)
                button_remove_2_window = self.canvas.create_window(520, 154, anchor=NW, window=button_remove_2, tags="rowBox")                   
                return
            
            if self.fullRows == 3:
            # Split previous array into 3 arrays (1 per full row)
                row1 = []
                for i in self.set[0]:
                    row1.append(i)
                row2 = []
                for i in self.set[1]:
                    row2.append(i)
                row3 = []
                for i in self.set[2]:
                    row3.append(i)

                # Append the ID of every task on the page to an array
                self.sets_id=[]
                self.sets_id.append(row1[4])
                self.sets_id.append(row2[4])
                self.sets_id.append(row3[4])

                # Append the task type of every task on the page to an array
                self.sets_type=[]
                self.sets_type.append(row1[3])
                self.sets_type.append(row2[3])
                self.sets_type.append(row3[3])

                # Insert data for the tasks into the relevant entry boxes
                self.name_1.insert(INSERT, row1[0])      
                self.subject_1.insert(INSERT, row1[1])
                self.date_1.insert(INSERT, row1[2])            
                self.name_2.insert(INSERT, row2[0])      
                self.subject_2.insert(INSERT, row2[1])
                self.date_2.insert(INSERT, row2[2])
                self.name_3.insert(INSERT, row3[0])      
                self.subject_3.insert(INSERT, row3[1])
                self.date_3.insert(INSERT, row3[2])
                
                # Get current date
                taskDate_1 = time.strptime(row1[2], "%d/%m/%Y")
                taskOverdue_1 = currentDate > taskDate_1
                taskDate_2 = time.strptime(row2[2], "%d/%m/%Y")
                taskOverdue_2 = currentDate > taskDate_2
                taskDate_3 = time.strptime(row3[2], "%d/%m/%Y")
                taskOverdue_3 = currentDate > taskDate_3
                
                # Change text colour to red for any task overdue
                if taskOverdue_1 == True:
                    self.name_1.configure(fg="#f44336")
                    self.subject_1.configure(fg="#f44336")
                    self.date_1.configure(fg="#f44336")
                if taskOverdue_2 == True:
                    self.name_2.configure(fg="#f44336")
                    self.subject_2.configure(fg="#f44336")
                    self.date_2.configure(fg="#f44336")
                if taskOverdue_3 == True:
                    self.name_3.configure(fg="#f44336")
                    self.subject_3.configure(fg="#f44336")
                    self.date_3.configure(fg="#f44336")

                button_remove_1 = Button(self, image=self.edit, command=lambda: self.load_notes(0), anchor = W)
                button_remove_1.configure(border=0, relief = FLAT, highlightthickness=0)
                button_remove_1_window = self.canvas.create_window(520, 94, anchor=NW, window=button_remove_1, tags="rowBox")

                button_remove_2 = Button(self, image=self.edit, command=lambda: self.load_notes(1), anchor = W)
                button_remove_2.configure(border=0, relief = FLAT, highlightthickness=0)
                button_remove_2_window = self.canvas.create_window(520, 154, anchor=NW, window=button_remove_2, tags="rowBox")

                button_remove_3 = Button(self, image=self.edit, command=lambda: self.load_notes(2), anchor = W)
                button_remove_3.configure(border=0, relief = FLAT, highlightthickness=0)
                button_remove_3_window = self.canvas.create_window(520, 214, anchor=NW, window=button_remove_3, tags="rowBox")
                return

            # For any empty rows, append a single space to the array of data to insert
            for i in range(self.tasknumber,self.progress[self.page+1]+1):
                self.set.append(' ')
                
        # If all pages are full, use this array
        else:
            self.canvas.delete("noData")
            self.fullRows = 4          
            self.set=[]
            for i in self.tasks[self.progress[self.page]:self.progress[self.page+1]+1]:
                self.set.append(i)

            # Insert rows
            self.t = 80
            self.b = 130
            # Create coloured row boxes            
            for i in range(4):
                self.canvas.create_rectangle(30, self.b+2, 548, self.t+1, fill="#f9f9f9", outline="#f9f9f9", tags="rowBox")
                self.canvas.create_rectangle(30, self.b, 546, self.t, fill="white", outline=self.rowColour, width=2, tags="rowBox")
                self.t += 60
                self.b += 60

            # Split previous array into 4 arrays (1 per row)
            row1 = []
            for i in self.set[0]:
                row1.append(i)
            row2 = []
            for i in self.set[1]:
                row2.append(i)
            row3 = []
            for i in self.set[2]:
                row3.append(i)
            row4 = []
            for i in self.set[3]:
                row4.append(i)

            # Append the ID of every task on the page to an array
            self.sets_id=[]
            self.sets_id.append(row1[4])
            self.sets_id.append(row2[4])
            self.sets_id.append(row3[4])
            self.sets_id.append(row4[4])

            # Append the task type of every task on the page to an array
            self.sets_type=[]
            self.sets_type.append(row1[3])
            self.sets_type.append(row2[3])
            self.sets_type.append(row3[3])
            self.sets_type.append(row4[3])           

            # Insert data for the tasks into the relevant entry boxes
            self.name_1.insert(INSERT, row1[0])      
            self.subject_1.insert(INSERT, row1[1])
            self.date_1.insert(INSERT, row1[2])            
            self.name_2.insert(INSERT, row2[0])      
            self.subject_2.insert(INSERT, row2[1])
            self.date_2.insert(INSERT, row2[2])
            self.name_3.insert(INSERT, row3[0])      
            self.subject_3.insert(INSERT, row3[1])
            self.date_3.insert(INSERT, row3[2])
            self.name_4.insert(INSERT, row4[0])      
            self.subject_4.insert(INSERT, row4[1])
            self.date_4.insert(INSERT, row4[2])
                
            # Get current date
            taskDate_1 = time.strptime(row1[2], "%d/%m/%Y")
            taskOverdue_1 = currentDate > taskDate_1
            taskDate_2 = time.strptime(row2[2], "%d/%m/%Y")
            taskOverdue_2 = currentDate > taskDate_2
            taskDate_3 = time.strptime(row3[2], "%d/%m/%Y")
            taskOverdue_3 = currentDate > taskDate_3
            taskDate_4 = time.strptime(row4[2], "%d/%m/%Y")
            taskOverdue_4 = currentDate > taskDate_4

            # Change text colour to red for any task overdue            
            if taskOverdue_1 == True:
                self.name_1.configure(fg="#f44336")
                self.subject_1.configure(fg="#f44336")
                self.date_1.configure(fg="#f44336")
            if taskOverdue_2 == True:
                self.name_2.configure(fg="#f44336")
                self.subject_2.configure(fg="#f44336")
                self.date_2.configure(fg="#f44336")
            if taskOverdue_3 == True:
                self.name_3.configure(fg="#f44336")
                self.subject_3.configure(fg="#f44336")
                self.date_3.configure(fg="#f44336")
            if taskOverdue_4 == True:
                self.name_4.configure(fg="#f44336")
                self.subject_4.configure(fg="#f44336")
                self.date_4.configure(fg="#f44336")                

            button_remove_1 = Button(self, image=self.edit, command=lambda: self.load_notes(0), anchor = W)
            button_remove_1.configure(border=0, relief = FLAT, highlightthickness=0)
            button_remove_1_window = self.canvas.create_window(520, 94, anchor=NW, window=button_remove_1, tags="rowBox")

            button_remove_2 = Button(self, image=self.edit, command=lambda: self.load_notes(1), anchor = W)
            button_remove_2.configure(border=0, relief = FLAT, highlightthickness=0)
            button_remove_2_window = self.canvas.create_window(520, 154, anchor=NW, window=button_remove_2, tags="rowBox")

            button_remove_3 = Button(self, image=self.edit, command=lambda: self.load_notes(2), anchor = W)
            button_remove_3.configure(border=0, relief = FLAT, highlightthickness=0)
            button_remove_3_window = self.canvas.create_window(520, 214, anchor=NW, window=button_remove_3, tags="rowBox")            

            button_remove_4 = Button(self, image=self.edit, command=lambda: self.load_notes(3), anchor = W)
            button_remove_4.configure(border=0, relief = FLAT, highlightthickness=0)
            button_remove_4_window = self.canvas.create_window(520, 274, anchor=NW, window=button_remove_4, tags="rowBox")

    def load_notes(self, task_id):
        # Set up the function's variables based on the current tab        
        if self.tab == "Overview":
            self.done = self.greenDone
            self.delete = self.greenDelete
            self.back = self.greenBack
        if self.tab == "Homework":
            self.done = self.blueDone
            self.delete = self.blueDelete
            self.back = self.blueBack
        if self.tab == "Coursework":
            self.done = self.yellowDone
            self.delete = self.yellowDelete
            self.back = self.yellowBack
        if self.tab == "Exam":
            self.done = self.redDone
            self.delete = self.redDelete
            self.back = self.redBack

        self.canvas.delete(ALL)
        self.draw_title_bar()
        self.canvas.create_rectangle(0, 40, 600, 0, fill=self.colour, outline=self.colour)
        self.draw_tabs() 

        # Set to true to use the correct validation methods when saving the task
        self.editPage = True

        # Create a single coloured task box
        self.canvas.create_rectangle(30, 132, 548, 81, fill="#f9f9f9", outline="#f9f9f9", tags="rowBox")
        self.canvas.create_rectangle(30, 130, 546, 80, fill="white", outline=self.rowColour, width=2, tags="rowBox")

        # Create entry boxes for the task's name, subject and due date to display data for the selected task
        
        # TASK NAME           SUBJECT   DATE
        # ##################  ########  ######
        # NOTES
        # ####################################
        # ####################################
        # ####################################
        # ####################################
        # ####################################
        
        self.task_name = Entry(self,width=45)
        self.task_name.configure(border=0, relief=FLAT, bg="white")
        task_name_window = self.canvas.create_window(40, 97, anchor=NW, window=self.task_name)
        self.task_subject = Entry(self,width=20)
        self.task_subject.configure(border=0, relief=FLAT, bg="white")
        task_subject_window = self.canvas.create_window(320, 97, anchor=NW, window=self.task_subject)
        self.task_date = Entry(self,width=15)
        self.task_date.configure(border=0, relief=FLAT, bg="white")
        task_date_window = self.canvas.create_window(450, 97, anchor=NW, window=self.task_date)

        self.tb = Text(self, width=64, height=11)
        self.tb.configure(border=1, bg="white")
        self.tb_window = self.canvas.create_window(30, 132, anchor=NW, window=self.tb)
        
        button_delete = Button(self, image=self.delete, command=lambda: self.delete_notes_task(self.task_id), anchor = W)
        button_delete.configure(border=0, relief = FLAT, highlightthickness=0)
        button_delete_window = self.canvas.create_window(30, 315, anchor=NW, window=button_delete)
        
        button_back = Button(self, image=self.back, command=self.return_tasks, anchor = W)
        button_back.configure(border=0, relief = FLAT, highlightthickness=0)
        button_back_window = self.canvas.create_window(80, 315, anchor=NW, window=button_back)

        button_done = Button(self, image=self.done, command=lambda: self.check_add_name(self.task_id), anchor = W)
        button_done.configure(border=0, relief = FLAT, highlightthickness=0)
        button_done_window = self.canvas.create_window(502, 315, anchor=NW, window=button_done)
        # old: 452 => new: 80
        
        # Insert the selected task's data into the entry boxes and text area.
        self.task_type = self.set[0][3]
        self.task_name.insert(INSERT, self.set[task_id][0])      
        self.task_subject.insert(INSERT, self.set[task_id][1])
        self.task_date.insert(INSERT, self.set[task_id][2])
        self.tb.insert(INSERT, self.set[task_id][5])
        self.task_id = (self.set[task_id][4])
        # Get current date
        todayDate = (time.strftime("%d/%m/%Y"))
        # Change text colour to red for any task overdue                    
        if todayDate > self.task_date.get():
            self.task_name.configure(fg="#f44336")
            self.task_subject.configure(fg="#f44336")
            self.task_date.configure(fg="#f44336")

    def page_up(self):
        # Scroll to previous page
        if self.tab == "Overview":
            self.ovpage -= 2
        elif self.tab == "Homework":
            self.hwpage -= 2
        elif self.tab == "Coursework":
            self.cwpage -= 2
        elif self.tab == "Exam":
            self.expage -= 2
        self.canvas.delete("rowBox")
        self.load_rows()
            
    def page_down(self):
        # Scroll to next page
        if self.tab == "Overview":
            self.ovpage += 2
        elif self.tab == "Homework":
            self.hwpage += 2
        elif self.tab == "Coursework":
            self.cwpage += 2
        elif self.tab == "Exam":
            self.expage += 2
        self.canvas.delete("rowBox")            
        self.load_rows()

    def add_item(self):
        # Set up the function's variables based on the current tab                
        if self.tab == "Overview":
            self.colour = "#4caf50"
            self.done = self.greenDone
            self.delete = self.greenDelete        
        if self.tab == "Homework":
            self.colour = "#4472C4"
            self.done = self.blueDone
            self.delete = self.blueDelete
        if self.tab == "Coursework":
            self.colour = "#ff9800"
            self.done = self.yellowDone
            self.delete = self.yellowDelete
        if self.tab == "Exam":
            self.colour = "#ff5722"
            self.done = self.redDone
            self.delete = self.redDelete
            
        self.canvas.delete(ALL)
        self.draw_title_bar()      
        self.canvas.create_rectangle(0, 40, 600, 0, fill=self.colour, outline=self.colour)
        self.draw_tabs()

        button_done = Button(self, image=self.done, command=lambda: self.check_add_name('null'), anchor = W)
        button_done.configure(border=0, relief = FLAT, highlightthickness=0)
        button_done_window = self.canvas.create_window(502, 315, anchor=NW, window=button_done)

        button_delete = Button(self, image=self.delete, command=self.return_rows, anchor = W)
        button_delete.configure(border=0, relief = FLAT, highlightthickness=0)
        button_delete_window = self.canvas.create_window(30, 315, anchor=NW, window=button_delete)


        # Create entry boxes for the task's name, subject and due date to display data for the selected task

        #  DETAILS        DUE DATE & TYPE
        # ------------   -------------------------  
        #  NAME           DAY    MONTH      YEAR
        #  ##########     ####   ########   #####
        #
        #  SUBJECT        TYPE
        #  ##########     #######

        self.canvas.create_rectangle(30, 300, 195, 90, fill="#eeeeee", outline="#FFFFFF")
        self.canvas.create_rectangle(212, 300, 544, 90, fill="#eeeeee", outline="#FFFFFF")
        #self.canvas.create_rectangle(394, 300, 544, 90, fill="#e0e0e0", outline="#FFFFFF")
        self.canvas.create_rectangle(30, 131, 544, 130, fill="#FFFFFF", outline="#FFFFFF")

        self.canvas.create_text(70, 111, text="Details", font=self.box_heading_font, fill="black")
        if self.tab == "Overview":
            self.canvas.create_text(287, 111, text="Due Date & Type", font=self.box_heading_font, fill="black")
        else:
            self.canvas.create_text(260, 111, text="Due Date", font=self.box_heading_font, fill="black")            
        
        self.canvas.create_text(60, 160, text="Name", font=self.box_content_font, fill="black")
        self.task_name = Entry(self,width=24)
        self.task_name.configure(border=0, relief=FLAT, bg="#FFFFFF")
        task_name_window = self.canvas.create_window(40, 175, anchor=NW, window=self.task_name)

        self.canvas.create_text(65, 230, text="Subject", font=self.box_content_font, fill="black")
        self.task_subject = Entry(self,width=24)
        self.task_subject.configure(border=0, relief=FLAT, bg="#FFFFFF")
        task_subject_window = self.canvas.create_window(40, 245, anchor=NW, window=self.task_subject)

        # Every number from 1 to 31 is assigned to the array called self.days
        # A text label is created 'Day'
        # A combobox is created with the contents of the self.days array
        # The combobox is positioned on the canvas
        self.days = [1,2,3,4,5,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
        self.canvas.create_text(232, 160, text="Day", font=self.box_content_font, fill="black")
        self.task_day = ttk.Combobox(self, values=self.days, state='readonly', width=5)
        task_day_window = self.canvas.create_window(220, 175, anchor=NW, window=self.task_day)

        # Every month from January to December is assigned to the array called self.months
        # A text label is created 'Month'
        # A combobox is created with the contents of the self.months array
        # The combobox is positioned on the canvas
        self.months = ['January','February','March','April','May','June','July','August','September','October','November','December']
        self.canvas.create_text(314, 160, text="Month", font=self.box_content_font, fill="black")
        self.task_month = ttk.Combobox(self, values=self.months, state='readonly', width=13)
        task_month_window = self.canvas.create_window(295, 175, anchor=NW, window=self.task_month)

        # The current year is assigned to self.year
        # An empty array is created 'self.years'
        # The current year and the next four years are added to the self.years array
        self.year = (time.strftime("%Y"))
        self.years=[]
        self.years.append(int(self.year))
        self.years.append(int(self.year) + 1)
        self.years.append(int(self.year) + 2)
        self.years.append(int(self.year) + 3)
        self.years.append(int(self.year) + 4)

        #self.years = list(range(5))
        #map(lambda x: x + int(self.year), self.years)

        # A text label is created 'Year'
        # A combobox is created with the contents of the self.years array
        # The combobox is positioned on the canvas
        self.canvas.create_text(433, 160, text="Year", font=self.box_content_font, fill="black")
        self.task_year = ttk.Combobox(self, values=self.years, state='readonly', width=7)
        task_year_window = self.canvas.create_window(417, 175, anchor=NW, window=self.task_year)

        # If the array tab is selected:
        # A text label is created 'self.type'
        # A combobox is created with the contents of the self.type array
        # The combobox is positioned on the canvas
        
        # The dropdown menu will select the value for the current tab by default
        # If the overview tab is selected, no values are automatically selected.
        self.type = ['Homework','Coursework','Exam']
        self.canvas.create_text(235, 230, text="Type", font=self.box_content_font, fill="black")
        self.task_type = ttk.Combobox(self, values=self.type, state='readonly', width=13)
        if self.tab == "Homework":
            self.task_type.set('Homework')
        elif self.tab == "Coursework":
            self.task_type.set('Coursework')
        elif self.tab == "Exam":
            self.task_type.set('Exam')
        task_type_window = self.canvas.create_window(220, 245, anchor=NW, window=self.task_type)
        self.editPage == False
         
    def check_add_name(self, task_id):
        # VALIDATION: if task name is blank, return message
        if self.task_name.get() == "":
            messagebox.showinfo("Invalid Entry", "Task name cannot be left blank.")
            pass
        else:
            self.check_add_subject()

    def check_add_subject(self):
        # VALIDATION: if subject is blank, return message
        if self.task_subject.get() == "":
            messagebox.showinfo("Invalid Entry", "Subject cannot be left blank.")
            pass
        else:
            self.check_add_date()

    def check_add_date(self):
        if self.editPage:    
            # VALIDATION: if date is blank, return message
            if self.task_date.get() == "":
                messagebox.showinfo("Invalid Entry", "Date cannot be left blank.")
                pass
            # VALIDATION: if date is shorter than 10 characters, return message
            elif len(self.task_date.get()) != 10:
                messagebox.showinfo("Invalid Entry", "Incorrect date format, please use DD/MM/YYYY.")
                pass
            # VALIDATION: if date does not include a '/' in the relevant positions, return message
            elif (self.task_date.get()[2]) != "/" or (self.task_date.get()[5]) != "/":
                messagebox.showinfo("Invalid Entry", "Incorrect date format, please use DD/MM/YYYY.")
                pass
            # VALIDATION: if date contains non number characters, return message
            else:
                dateData = (self.task_date.get().strip().split('/'))
                self.taskDay = dateData[0]
                self.monthNumber = dateData[1]
                self.taskYear = dateData[2]
                if self.taskDay.isdigit() == False or self.monthNumber.isdigit() == False or self.taskYear.isdigit() == False:
                    messagebox.showinfo("Invalid Entry", "Incorrect date format, please use DD/MM/YYYY.")
                    pass

                else:
                    self.check_add_valid_date()
        else:
            # VALIDATION: if a day is not selected, return message
            if self.task_day.get() == "":
                messagebox.showinfo("Invalid Entry", "Day cannot be left blank.")
                pass
            else:
                # VALIDATION: if a month is not selected, return message
                if self.task_month.get() == "":
                    messagebox.showinfo("Invalid Entry", "Month cannot be left blank.")
                    pass
                else:
                    # VALIDATION: if a year is not selected, return message
                    #print(self.task_year.get())
                    if self.task_year.get() == "":
                        messagebox.showinfo("Invalid Entry", "Year cannot be left blank.")
                        pass
                    else:
                        self.check_add_valid_date()

    def check_add_valid_date(self):
        # Check if the given date is valid
        # Create a dictionary of months with thier associated numbers
        months = {"January": 1,
          "February": 2,
          "March": 3,
          "April": 4,
          "May": 5,
          "June": 6,
          "July": 7,
          "August": 8,
          "September": 9,
          "October": 10,
          "November": 11,
          "December": 12}
        
        if self.editPage == False:
            # Get string values for each part of the given date
            self.taskDay = self.task_day.get()
            self.monthName = self.task_month.get()
            self.taskYear = self.task_year.get()
            # Using the dictionary, convert month name to its respective number
            for name, number in months.items():
                if self.monthName == str(name):
                    self.monthNumber = number

        else:
            # Get integer values for each part of the given date            
            dateData = (self.task_date.get().strip().split('/'))
            self.taskDay = dateData[0]
            self.monthNumber=dateData[1]
            self.task_year = dateData[2]

            # Strip the proceding '0' from the slected month if appropriate
            monthIntegers=[]
            for n in self.monthNumber:
                monthIntegers.append(n)
            if  monthIntegers[0]=="0":
                self.monthNumber=monthIntegers[1]
            # Using the dictionary, convert month number to its respective name
            for name, number in months.items():
                if self.monthNumber == str(number):
                    self.monthName = name# 17578

        # The maximum number of days for each month is determined
        # 2 arrays are created
        # The first contains every month that can have up to 30 days
        # The second contains every month that can have up to 31 days
        days_30 = (4,6,9,11)
        days_31 = (1,3,5,7,8,10,12)

        # If the user enters a day value greater than 30 for a 30 day month, a message will be shown
        # If the user enters a day value greater than 31 for a 31 day month, a message will be shown
        if int(self.monthNumber) in days_30 and int(self.taskDay) > 30:
            messagebox.showinfo("Invalid Entry", str(self.monthName)+" can only have up to 30 days.")
            pass
        elif int(self.monthNumber) in days_31 and int(self.taskDay) > 31:
            messagebox.showinfo("Invalid Entry", str(self.monthName)+" can only have up to 31 days.")
            pass
        else:
            self.check_leap_year()

    def check_leap_year(self):
        # Check if the year selected is a leap year
        # A variable 'leap_year' is created an is assigned as false
        # If the selected year can be divided by 4, it is considered a leap year
        # But, if the selected year can be divided by 100, it is no longer a leap year
        # If the selected year can be divided by 400, it is a leap year
        leap_year=False
        if (int(self.taskYear)%4) == 0:
            leap_year=True
            if (int(self.taskYear)%100) == 0:
                leap_year=False
            elif (int(self.taskYear)%400) == 0:
                leap_year=True        

        # If the user has selected February and a leap_year is true, the day cannot be greater than 29
        # If the user has selected February and a leap_year is false, the day cannot be greater than 28
        # If the day is valid, the write_task function is called
        if int(self.monthNumber) == 2 and leap_year and int(self.taskDay) > 29:
            messagebox.showinfo("Invalid Entry", "On a leap year, "+str(self.monthName)+" can only have up to 29 days.")
            pass
        elif int(self.monthNumber) == 2 and not leap_year and int(self.taskDay) > 28:
            messagebox.showinfo("Invalid Entry", "Not on a leap year, "+str(self.monthName)+" can only have up to 28 days.")
            pass    
        else:
            if self.editPage == False:
                self.write_task()
            else:
                self.editPage=False
                self.save_notes_task()
            
    def write_task(self):
        # Save any new task to the database
        # If the day selected is only a single digit, add a '0'
        if len(self.taskDay) == 1:
            self.dayNumber = "0" + str(self.taskDay)
        else:
            self.dayNumber = str(self.taskDay)
        # If the month selected is only a single digit, add a '0'
        if len(str(self.monthNumber)) == 1:
            self.monthNumber = "0" + str(self.monthNumber)
       
        # Concatenate the date data in the form YYYY/MM/DD
        self.date = str(self.taskYear) + "/" + str(self.monthNumber) + "/" + str(self.dayNumber)

        # Check if type has been selected
        if self.tab == "Overview":
            if self.task_type.get() == "":
                messagebox.showinfo("Invalid Entry", "Type cannot be left blank.")
                return
        # Find the last row's ID in the database and increment
        # If no tasks exist, set the ID to '0'
        conn = sqlite3.connect('tasks.db')
        lastRow = conn.execute("SELECT MAX(id) FROM TASKS")
        for row in lastRow:
            self.id = row[0]
        if self.id == None:
            self.id = 0
        if self.tab == "Overview":
            conn.execute("INSERT INTO TASKS(ID, TASK, SUBJECT, DATE, TAB, NOTES) values (?, ?, ?, ?, ?, ?)", (self.id+1, self.task_name.get(), self.task_subject.get(), self.date, str(self.task_type.get()), ""))
        else:
            conn.execute("INSERT INTO TASKS(ID, TASK, SUBJECT, DATE, TAB, NOTES) values (?, ?, ?, ?, ?, ?)", (self.id+1, self.task_name.get(), self.task_subject.get(), self.date, self.tab, ""))
        conn.commit()
        conn.close()

        # The program will show the relevant tasks page once added
        self.return_tasks()                 

    def return_tasks(self):
        # Return to previous page after adding a task
        if self.tab == "Overview":
            self.setup_overview()                            
        if self.tab == "Homework":
            self.setup_homework()
        if self.tab == "Coursework":  
            self.setup_coursework()
        if self.tab == "Exam":  
            self.setup_exams()   

    def return_rows(self):
        # Confirm deleting whilst adding a task
        if messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?"):
            # Return to previous page after deleting a task            
            if self.tab == "Overview":
                self.setup_overview()
            if self.tab == "Homework":
                self.setup_homework()
            if self.tab == "Coursework":
                self.setup_coursework()
            if self.tab == "Exam":
                self.setup_exams()                
        else:
            pass

    def sort_1(self):
        # SORT: Date Ascending
        if self.outside:
            pass
        else:        
            self.conn = sqlite3.connect('tasks.db')
            self.tasks = []
            if self.tab == "Overview":
                self.cursor = self.conn.execute("SELECT * FROM tasks ORDER BY DATE ASC")
            else:
                self.cursor = self.conn.execute("SELECT * FROM tasks WHERE TAB='"+str(self.tab)+"' ORDER BY DATE ASC")
            self.refresh_task_list()

    def sort_2(self):
        # SORT: Date Descending
        if self.outside:
            pass
        else:
            self.conn = sqlite3.connect('tasks.db')
            self.tasks = []
            if self.tab == "Overview":
                self.cursor = self.conn.execute("SELECT * FROM tasks ORDER BY DATE DESC")
            else:
                self.cursor = self.conn.execute("SELECT * FROM tasks WHERE TAB='"+str(self.tab)+"' ORDER BY DATE DESC")
            self.refresh_task_list()

    def sort_3(self):
        # SORT: Task Ascending
        if self.outside:
            pass
        else:        
            self.conn = sqlite3.connect('tasks.db')
            self.tasks = []
            if self.tab == "Overview":
                self.cursor = self.conn.execute("SELECT * FROM tasks ORDER BY TASK ASC")
            else:
                self.cursor = self.conn.execute("SELECT * FROM tasks WHERE TAB='"+str(self.tab)+"' ORDER BY TASK ASC")
            self.refresh_task_list()

    def sort_4(self):
        # SORT: Task Descending
        if self.outside:
            pass
        else:        
            self.conn = sqlite3.connect('tasks.db')
            self.tasks = []
            if self.tab == "Overview":
                self.cursor = self.conn.execute("SELECT * FROM tasks ORDER BY TASK DESC")
            else:
                self.cursor = self.conn.execute("SELECT * FROM tasks WHERE TAB='"+str(self.tab)+"' ORDER BY TASK DESC")
            self.refresh_task_list()

    def sort_5(self):
        # SORT: Subject Ascending
        if self.outside:
            pass
        else:        
            self.conn = sqlite3.connect('tasks.db')
            self.tasks = []
            if self.tab == "Overview":
                self.cursor = self.conn.execute("SELECT * FROM tasks ORDER BY SUBJECT ASC")
            else:
                self.cursor = self.conn.execute("SELECT * FROM tasks WHERE TAB='"+str(self.tab)+"' ORDER BY SUBJECT ASC")
            self.refresh_task_list()

    def sort_6(self):
        # SORT: Subject Descending
        if self.outside:
            pass
        else:        
            self.conn = sqlite3.connect('tasks.db')
            self.tasks = []
            if self.tab == "Overview":
                self.cursor = self.conn.execute("SELECT * FROM tasks ORDER BY SUBJECT DESC")
            else:
                self.cursor = self.conn.execute("SELECT * FROM tasks WHERE TAB='"+str(self.tab)+"' ORDER BY SUBJECT DESC")
            self.refresh_task_list()

    def sort_7(self):
        # SORT: Time Task Added
        if self.outside:
            pass
        else:        
            self.conn = sqlite3.connect('tasks.db')
            self.tasks = []
            if self.tab == "Overview":
                self.cursor = self.conn.execute("SELECT * FROM tasks ORDER BY ID ASC")
            else:
                self.cursor = self.conn.execute("SELECT * FROM tasks WHERE TAB='"+str(self.tab)+"' ORDER BY ID ASC")
            self.refresh_task_list()
        
    def refresh_task_list(self):
        for row in self.cursor:
            single = []                 #Create an array for each task
            single.append(row[1])       #Add name
            single.append(row[2])       #Add subject
            #single.append(row[3])

            # Reverse the date format (YYYY/MM/DD => DD/MM/YYYY)
            dateData = (row[3].strip().split('/'))
            dateDay = dateData[2]
            dateMonth = dateData[1]
            dateYear = dateData[0]
            dateNew = dateDay + "/" + dateMonth + "/" + dateYear

            single.append(dateNew)      #Add date
            single.append(row[4])       #Add type
            single.append(row[0])       #Add ID
            single.append(row[5])       #Add notes
            self.tasks.append(single)   #Create an array of each task's array
        self.conn.close()
        self.load_rows()

    def delete_notes_task(self, task_id):
        # Delete tasks whilst modifying
        self.conn = sqlite3.connect('tasks.db')
        self.conn.execute("DELETE from TASKS where ID='"+ str(self.task_id)+"';")

        # If selected task is the final task on the page, go to previous page unless, current page is 1
        if self.fullRows == 1:
            if self.page > 0:
                if self.tab == "Overview":
                    self.ovpage -= 2
                elif self.tab == "Homework":
                    self.hwpage -= 2
                elif self.tab == "Coursework":
                    self.cwpage -= 2
                elif self.tab == "Exam":
                    self.expage -= 2
            else:
                pass
        self.refresh_task_list_remove()

    def save_notes_task(self):
        print("SAVE")
        # Update task's data in the edit page
        # Get data from the modify page
        t1d=self.task_date.get()
        date1=t1d.split('/')
        t1d=date1[2]+"/"+date1[1]+"/"+date1[0]
        self.name_of_task = self.task_name.get()
        self.subject_of_task = self.task_subject.get()
       
        # Update the database with the data
        self.conn = sqlite3.connect('tasks.db')
        sql = ''' UPDATE TASKS
                  SET TASK = ? ,
                      SUBJECT = ? ,
                      DATE = ?,
                      TAB = ?,
                      NOTES = ?
                  WHERE ID = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, (self.name_of_task, self.subject_of_task, t1d, self.task_type, str(self.tb.get("1.0", END)), str(self.task_id)))
        self.conn.commit()  
        self.refresh_task_list_remove()

    def delete_row(self, row_number):
        # Deletes task when on the tasks page
        # Using the value passed by the delete button, the row number can be used to find the task's ID
        self.task_id = self.set[row_number][4]
        
        # Delete the task with that ID
        self.conn = sqlite3.connect('tasks.db')
        self.conn.execute("DELETE from TASKS where ID='"+ str(self.task_id)+"';")
        
        # If selected task is the final task on the page, go to previous page unless, current page is 1
        if self.fullRows == 1:
            if self.page > 0:
                if self.tab == "Overview":
                    self.ovpage -= 2
                elif self.tab == "Homework":
                    self.hwpage -= 2
                elif self.tab == "Coursework":
                    self.cwpage -= 2
                elif self.tab == "Exam":
                    self.expage -= 2
            else:
                pass
        self.refresh_task_list_remove()
        
    def refresh_task_list_remove(self):
        # Save changes to the database and reload the program to the tasks page
        self.conn.commit()        
        self.conn.close()
        self.setup_data()

    def map_sga(self):
        # Set up the function's variables based on the current tab                        
        if self.tab == "Overview":
            self.back = self.greenBack
        if self.tab == "Homework":
            self.back = self.blueBack
        if self.tab == "Coursework":
            self.back = self.yellowBack
        if self.tab == "Exam":
            self.back = self.redBack
            
        self.canvas.delete(ALL)
        button_back = Button(self, image=self.back, command=self.return_tasks, anchor = W)
        button_back.configure(border=0, relief = FLAT, highlightthickness=0)
        button_back_window = self.canvas.create_window(502, 315, anchor=NW, window=button_back)

        # Fill the canvas with an image of the Carre's map
        self.map = PhotoImage(file="map_sga.gif")
        self.canvas.create_image(54, 0, image = self.map, anchor = NW)

        #Disallow page sorting (True)
        self.outside=True

    def map_cgs(self):
        # Set up the function's variables based on the current tab                                
        if self.tab == "Overview":
            self.back = self.greenBack
        if self.tab == "Homework":
            self.back = self.blueBack
        if self.tab == "Coursework":
            self.back = self.yellowBack
        if self.tab == "Exam":
            self.back = self.redBack
            
        self.canvas.delete(ALL)
        button_back = Button(self, image=self.back, command=self.return_tasks, anchor = W)
        button_back.configure(border=0, relief = FLAT, highlightthickness=0)
        button_back_window = self.canvas.create_window(502, 315, anchor=NW, window=button_back)
        
        # Fill the canvas with an image of the St George's map        
        self.map = PhotoImage(file="map_cgs.gif")
        self.canvas.create_image(0, 0, image = self.map, anchor = NW)

        #Disallow page sorting (True)       
        self.outside=True

    def websites(self):
        # Set up the function's variables based on the current tab                                        
        if self.tab == "Overview":
            self.back = self.greenBack
        if self.tab == "Homework":
            self.back = self.blueBack
        if self.tab == "Coursework":
            self.back = self.yellowBack
        if self.tab == "Exam":
            self.back = self.redBack
            
        self.canvas.delete(ALL)
        self.draw_title_bar()
        self.canvas.create_rectangle(0, 40, 600, 0, fill=self.colour, outline=self.colour)
        self.canvas.create_text(287, 22, text="Useful Websites", font=self.tab_font, fill="white")

        button_back = Button(self, image=self.back, command=self.return_tasks, anchor = W)
        button_back.configure(border=0, relief = FLAT, highlightthickness=0)
        button_back_window = self.canvas.create_window(502, 315, anchor=NW, window=button_back)

        # Create a list of 10 websites with their name and URL
        web1 = self.canvas.create_text(50, 100, text="01", fill="black")        
        web1 = self.canvas.create_text(200, 100, text="Children's Services Young People's Website", fill="blue")
        self.canvas.tag_bind(web1, '<ButtonPress-1>', self.open_web1)
        
        web2 = self.canvas.create_text(50, 130, text="02", fill="black")        
        web2 = self.canvas.create_text(171, 130, text="Lincolnshire's Online Prospectus", fill="blue")
        self.canvas.tag_bind(web2, '<ButtonPress-1>', self.open_web2) 

        web3 = self.canvas.create_text(50, 160, text="03", fill="black")        
        web3 = self.canvas.create_text(149, 160, text="National Careers Service", fill="blue")
        self.canvas.tag_bind(web3, '<ButtonPress-1>', self.open_web3) 

        web4 = self.canvas.create_text(50, 190, text="04", fill="black")        
        web4 = self.canvas.create_text(133, 190, text="Bright Knowledge", fill="blue")
        self.canvas.tag_bind(web4, '<ButtonPress-1>', self.open_web4)

        web5 = self.canvas.create_text(50, 220, text="05", fill="black")        
        web5 = self.canvas.create_text(129, 220, text="Apprenticeships", fill="blue")
        self.canvas.tag_bind(web5, '<ButtonPress-1>', self.open_web5)

        web6 = self.canvas.create_text(50, 250, text="06", fill="black")        
        web6 = self.canvas.create_text(116, 250, text="Careers Box", fill="blue")
        self.canvas.tag_bind(web6, '<ButtonPress-1>', self.open_web6)

        web7 = self.canvas.create_text(50, 280, text="07", fill="black")        
        web7 = self.canvas.create_text(102, 280, text="icould", fill="blue")
        self.canvas.tag_bind(web7, '<ButtonPress-1>', self.open_web7)

        web8 = self.canvas.create_text(50, 310, text="08", fill="black")        
        web8 = self.canvas.create_text(121, 310, text="SUVAT Solver", fill="blue")
        self.canvas.tag_bind(web8, '<ButtonPress-1>', self.open_web8)         

        #Disallow page sorting (True)
        self.outside=True

    # Add a link to each URL that can open the default browser once clicked
    def open_web1(self, event):
        webbrowser.open_new(r"http://www.teeninfolincs.co.uk")
    def open_web2(self, event):
        webbrowser.open_new(r"http://www.14-19.info")
    def open_web3(self, event):
        webbrowser.open_new(r"https://nationalcareersservice.direct.gov.uk")
    def open_web4(self, event):
        webbrowser.open_new(r"http://www.brightknowledge.org")
    def open_web5(self, event):
        webbrowser.open_new(r"http://www.apprenticeships.org.uk")
    def open_web6(self, event):
        webbrowser.open_new(r"http://www.careersbox.co.uk")
    def open_web7(self, event):
        webbrowser.open_new(r"http://www.icould.com")
    def open_web8(self, event):
        webbrowser.open_new(r"http://karsten.pw")

    def contact(self):
        # Set up the function's variables based on the current tab                                                
        if self.tab == "Overview":
            self.back = self.greenBack
        if self.tab == "Homework":
            self.back = self.blueBack
        if self.tab == "Coursework":
            self.back = self.yellowBack
        if self.tab == "Exam":
            self.back = self.redBack
            
        self.canvas.delete(ALL)
        self.draw_title_bar()
        self.canvas.create_rectangle(0, 40, 600, 0, fill=self.colour, outline=self.colour)
        self.canvas.create_text(287, 22, text="Contact Details", font=self.tab_font, fill="white")

        button_back = Button(self, image=self.back, command=self.return_tasks, anchor = W)
        button_back.configure(border=0, relief = FLAT, highlightthickness=0)
        button_back_window = self.canvas.create_window(502, 315, anchor=NW, window=button_back)

        self.logo1 = PhotoImage(file="logo_sga.gif")
        self.canvas.create_image(100, 60, image = self.logo1, anchor = NW)
        self.logo2 = PhotoImage(file="logo_cgs.gif")
        self.canvas.create_image(355, 60, image = self.logo2, anchor = NW)

        name1 = self.canvas.create_text(150, 170, text="St George's Academy", font=self.header_font, fill="black")        
        name2 = self.canvas.create_text(400, 170, text="Carre's Grammar School", font=self.header_font, fill="black")        
        
        st1 = self.canvas.create_text(150, 200, text="Westholme", fill="black")
        tn1 = self.canvas.create_text(150, 215, text="Sleaford", fill="black") 
        pc1 = self.canvas.create_text(150, 230, text="NG34 7PP", fill="black") 
        st2 = self.canvas.create_text(400, 200, text="Northgate", fill="black")
        tn2 = self.canvas.create_text(400, 215, text="Sleaford", fill="black") 
        pc2 = self.canvas.create_text(400, 230, text="NG34 7DD", fill="black") 

        tel1 = self.canvas.create_text(150, 255, text="01529 302487", fill="blue")
        self.canvas.tag_bind(tel1, '<ButtonPress-1>', self.open_tel1)
        tel2 = self.canvas.create_text(400, 255, text="01529 302181", fill="blue")
        self.canvas.tag_bind(tel2, '<ButtonPress-1>', self.open_tel2)

        email1 = self.canvas.create_text(150, 275, text="sjsf@st-georges-academy.org", fill="blue")
        self.canvas.tag_bind(email1, '<ButtonPress-1>', self.open_email1)
        email2 = self.canvas.create_text(400, 275, text="sjsf@carres.lincs.sch.uk", fill="blue")
        self.canvas.tag_bind(email2, '<ButtonPress-1>', self.open_email2)

        web1 = self.canvas.create_text(150, 295, text="www.st-georges-academy.org", fill="blue")
        self.canvas.tag_bind(web1, '<ButtonPress-1>', self.open_web9)
        web2 = self.canvas.create_text(400, 295, text="www.carres.lincs.sch.uk", fill="blue")
        self.canvas.tag_bind(web2, '<ButtonPress-1>', self.open_web10)

        #Disallow page sorting (True)
        self.outside=True

    def open_tel1(self, event):
        webbrowser.open_new(r"tel:+441529302487")
    def open_tel2(self, event):
        webbrowser.open_new(r"tel:+441529302181")
    def open_email1(self, event):
        webbrowser.open_new(r"mailto:SJSF@st-georges-academy.org")
    def open_email2(self, event):
        webbrowser.open_new(r"mailto:SJSF@carres.lincs.sch.uk")
    def open_web9(self, event):
        webbrowser.open_new(r"http://www.st-georges-academy.org")        
    def open_web10(self, event):
        webbrowser.open_new(r"http://www.carres.lincs.sch.uk")


        
        



#### FOR TESTING ####
    def more(self):
        print("more")

    def donothing(self):
        pass
    
    def generate_sample_data(self):
        conn = sqlite3.connect('tasks.db')
        lastRow = conn.execute("SELECT MAX(id) FROM TASKS")
        for row in lastRow:
            _id = row[0]
        if _id == None:
            _id = 0
        for i in range(1, 20):
            task = "Sample Task %i" % i
            subject = random.choice(["Maths", "English", "Geography", "Physics", "Chemicals"])#, "Chestology"])

            note = random.choice(["Notes here", "More notes", "Other things"])

            day = random.choice(["01", "15", "06", "17", "24", "19"])
            month = random.choice(["01", "02", "06", "07", "12", "11"])
            year = random.choice(["2016", "2017", "2018"])
            
            date = year+"/"+month+"/"+day
            _type = random.choice(["Homework", "Coursework", "Exam"])
            conn.execute("INSERT INTO TASKS(ID, TASK, SUBJECT, DATE, TAB, NOTES) values (?, ?, ?, ?, ?, ?)", (_id+i, task, subject, date, _type, note))
        conn.commit()
        conn.close()
        self.setup_data()
        
    def generate_sample_task(self):
        conn = sqlite3.connect('tasks.db')
        lastRow = conn.execute("SELECT MAX(id) FROM TASKS")
        for row in lastRow:
            _id = row[0]
        if _id == None:
            _id = 0
        for i in range(1):
            task = "Sample Task %i" % i
            subject = random.choice(["Maths", "English", "Geography", "Physics", "Chemicals"])#, "Chestology"])

            note = random.choice(["Notes here", "More notes", "Other things"])

            day = random.choice(["01", "15", "06", "17", "24", "19"])
            month = random.choice(["01", "02", "06", "07", "12", "11"])
            year = random.choice(["2016", "2017", "2018"])
            
            date = year+"/"+month+"/"+day
            _type = random.choice(["Homework", "Coursework", "Exam"])
            conn.execute("INSERT INTO TASKS(ID, TASK, SUBJECT, DATE, TAB, NOTES) values (?, ?, ?, ?, ?, ?)", (_id+1, task, subject, date, _type, note))
        conn.commit()
        conn.close()
        self.setup_data()        
        
    def nuke_database(self):
        os.remove("tasks.db")
        conn = sqlite3.connect('tasks.db')
        conn.execute('''CREATE TABLE TASKS
               (ID INT PRIMARY KEY     NOT NULL,
               TASK           TEXT    NOT NULL,
               SUBJECT            TEXT     NOT NULL,
               DATE        DATE    NOT NULL,
               TAB          TEXT    NOT NULL,
               NOTES   TEXT);''')
        conn.close()
        self.ovpage=0
        self.hwpage=0
        self.cwpage=0
        self.expage=0
        self.setup_data()
        
interface = StudentOrganiser()
interface.mainloop()
