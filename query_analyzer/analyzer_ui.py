#!/usr/bin/env python
'''UI Class for query analyzer'''

import tkinter as tk 
from tkinter import ttk

import typing

class analyzer_UI(tk.Tk):
    '''Class for UI object with main methods for UI display and information passing'''

    def __init__(self) -> None:
        '''initializing tkinter as framework'''

        super().__init__()

    def run_UI(self, data: typing.Dict) -> None:            # data has "list"=List of dicts with query and yield
        '''Main function for UI display'''                  # and "suggestions"= List of strings for display
        
        self.build_window(data=data)
        
        self.mainloop()

    def build_window(self, data: typing.Dict) -> None:
        '''Main Window builder, geometry and title'''
        
        # Main Window attributes
        self.title("Query Analyzer")
        self.geometry("800x600+64+64")
        self.iconbitmap("./query_analyzer/analyzer.ico")

        # Main Window layout and frames with content
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)

        listframe = self.insert_querylist(list=data["list"])
        listframe.grid(column=0, row=0)
        textframe = self.insert_suggestions(list=data["suggestions"])
        textframe.grid(column=0, row=1)


    def insert_querylist(self, list: typing.List[typing.Dict]) -> tk.Frame:
        '''Create first frame and insert query strings and yield into its grid'''

        #create basic frame layout
        frame = ttk.Frame(self)
        frame["width"] = 800
        frame["height"] = 350
        frame["borderwidth"] = 5
        frame["relief"] = "groove"

        # Create grid layout
        frame.columnconfigure(0, weight=4)
        frame.columnconfigure(1, weight=1)

        # Fill in column headlines SOLVE ISSUE HERE!!!!!!!!!
        query_headline = ttk.Label(frame, width=640, text="Query and Subqueries", font=("Helvetica", 14, "bold"))
        yield_headline = ttk.Label(frame, width=160,text="Yield", font=("Helvetica", 14, "bold"))
        query_headline.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
        yield_headline.grid(column=1, row=0, padx=5, pady=5)

        # Insert entries from list into grid

        return frame


    def insert_suggestions(self, list: typing.List[str]) -> tk.Frame:
        '''Create second frame and insert suggestion text'''

        # create basic frame layout
        frame = ttk.Frame(self)
        frame["width"] = 800
        frame["height"] = 150
        frame["borderwidth"] = 5
        frame["relief"] = "groove"

        # create headline
        headline = ttk.Label(frame, width=800, text="Suggestions", font=("Helvetica", 14, "bold"))
        headline.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)

        # insert suggestions to grid
        row_count = 1

        for entry in list:
            ttk.Label(frame, text=entry, font=("Helvetica", 12)).grid(column=0, row=row_count, padx=5, pady=5, sticky=tk.W)
            row_count += 1

        return frame


        


        


if __name__ == "__main__":

    data = {}
    data["list"] = []
    data["suggestions"] = []

    for a in range(5):
        data["suggestions"].append("test" * (a+1))
    
    ui = analyzer_UI()
    ui.run_UI(data=data)