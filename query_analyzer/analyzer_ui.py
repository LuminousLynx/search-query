#!/usr/bin/env python
'''UI Class for query analyzer'''

import tkinter as tk 
from tkinter import ttk

from search_query.query import Query
from search_query.and_query import AndQuery
from search_query.or_query import OrQuery


import typing

class AnalyzerUI(tk.Tk):
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
        
        width= self.winfo_screenwidth() 
        height= self.winfo_screenheight()
        self.geometry("%dx%d" % (width/1.3, height/1.3))

        self.iconbitmap("./query_analyzer/analyzer.ico")

        # Main Window layout and frames with content
        upper_frame = self.insert_querylist(query_list=data["list"])
        upper_frame.pack(fill="both", expand=True)

        lower_frame = self.insert_suggestions(suggestion_list=data["suggestions"])
        lower_frame.pack(fill="both", expand=True)


    def insert_querylist(self, query_list: typing.List[typing.Dict]) -> tk.Frame:
        '''Create first frame and insert query strings and yield into its grid'''

        #create basic frame layout
        upper_frame = ttk.Frame(self)
        upper_frame["borderwidth"] = 5
        upper_frame["relief"] = "groove"

        # Create grid layout
        upper_frame.grid_columnconfigure(0, weight=3)
        upper_frame.grid_columnconfigure(1, weight=1)

        # Fill in column headlines
        query_headline = ttk.Label(upper_frame, text="Query and Subqueries", font=("Helvetica", 14, "bold"))
        query_headline.grid(column=0, row=0, padx=5, pady=5, sticky=tk.NW)

        yield_headline = ttk.Label(upper_frame, text="Yield", font=("Helvetica", 14, "bold"))
        yield_headline.grid(column=1, row=0, padx=5, pady=5, sticky=tk.NW)

        # Insert entries from list into grid: Query strings in the first column, yields in the second
        row_count = 1

        for entry in query_list:
            if isinstance(entry["query"], Query):
                query_string = entry["query"].to_string()
                query_label = ttk.Label(upper_frame, text=query_string, font=("Helvetica", 12))
                query_label.grid(column=0, row=row_count, padx=5, pady=5, sticky=tk.W)

                yield_label = ttk.Label(upper_frame, text=str(entry["yield"]), font=("Helvetica", 12))
                yield_label.grid(column=1, row=row_count, padx=5, pady=5, sticky=tk.W)
            
            else:
                query_label = ttk.Label(upper_frame, text="Query not found", font=("Helvetica", 12))
                query_label.grid(column=0, row=row_count, padx=5, pady=5, sticky=tk.W)

                yield_label = ttk.Label(upper_frame, text="n/a", font=("Helvetica", 12))
                yield_label.grid(column=1, row=row_count, padx=5, pady=5, sticky=tk.W)

            row_count += 1

        return upper_frame


    def insert_suggestions(self, suggestion_list: typing.List[str]) -> tk.Frame:
        '''Create second frame and insert suggestion text'''

        # create basic frame layout
        lower_frame = ttk.Frame(self)
        lower_frame["borderwidth"] = 5
        lower_frame["relief"] = "groove"

        # create headline
        headline = ttk.Label(lower_frame, text="Suggestions", font=("Helvetica", 14, "bold"))
        headline.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)

        # insert suggestions to grid
        row_count = 1

        for entry in suggestion_list:
            suggestion = ttk.Label(lower_frame, text=entry, font=("Helvetica", 12))
            suggestion.grid(column=0, row=row_count, padx=5, pady=5, sticky=tk.W)
            row_count += 1

        return lower_frame


        


        
# Only for tests - PLEASE REMOVE WHEN READY!!

if __name__ == "__main__":

    data = {}
    data["list"] = []
    data["suggestions"] = []

    query1 = OrQuery(children=["test0", "test4", "test5"])
    query2 = OrQuery(children=["test1", "test2"])
    query3 = AndQuery(children=[query1, query2])

    query_list = [{"query": query3, "yield": 204}, {"query": query2, "yield": 2232}, {"query": query1, "yield": 341}]
    data["list"].extend(query_list)

    for a in range(5):
        data["suggestions"].append("test" * (a+1))
    
    ui = AnalyzerUI()
    ui.run_UI(data=data)