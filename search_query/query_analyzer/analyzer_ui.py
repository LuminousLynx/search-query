#!/usr/bin/env python
'''UI Class for query analyzer'''

import tkinter as tk 
from tkinter import ttk

from search_query.query import Query





# pylint: disable=line-too-long

class AnalyzerUI(tk.Tk):
    '''Class for UI object with main methods for UI display and information passing'''


    def __init__(self) -> None:
        '''Initializing tkinter as framework'''

        super().__init__()


    def run_UI(self, data: dict) -> None:            # data has "list"=List of dicts with query and yield
        '''Main function for UI display'''                  # and "suggestions"= List of strings for display
        
        self.build_window(data=data)
        self.mainloop()


    def build_window(self, data: dict) -> None:
        '''Main Window builder, geometry and title'''
        
        # Main Window attributes
        self.title("Query Analyzer")
        
        width= self.winfo_screenwidth() 
        height= self.winfo_screenheight()
        self.geometry("%dx%d" % (width/1.3, height/1.3))

        self.iconbitmap("./search_query/query_analyzer/analyzer.ico")

        # Create top frame for the canvas and scrollbar
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="both", expand=True)

        # Create canvas
        canvas = tk.Canvas(top_frame)
        canvas.pack(side="left", fill="both", expand=True)

        # Create scrollbar
        scrollbar = ttk.Scrollbar(top_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create upper frame inside the canvas for queries and yield
        upper_frame = self.insert_querylist(canvas=canvas, query_list=data["list"], suggestion_list=data["suggestions"])
        canvas.create_window((0, 0), window=upper_frame, anchor="nw")

        # Configure canvas scroll region
        upper_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create lower frame for suggestions
        lower_frame = self.insert_suggestions(suggestion_list=data["suggestions"])
        lower_frame.pack(fill="both", expand=True)


    def insert_querylist(self, canvas: tk.Canvas, query_list: list[dict], suggestion_list: list[str]) -> tk.Frame:
        '''Create first frame and insert query strings and yields into its grid'''

        #create basic frame 
        upper_frame = ttk.Frame(canvas)

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

                if entry["query"].operator:
                    query_string = entry["query"].to_string(syntax="pubmed")
                    if query_string in suggestion_list[-1] or query_string in suggestion_list[-2]:
                        query_label = ttk.Label(upper_frame, text=query_string, font=("Helvetica", 12), background="orange")
                        query_label.grid(column=0, row=row_count, padx=5, pady=5, sticky=tk.W)

                        yield_label = ttk.Label(upper_frame, text=str(entry["yield"]), font=("Helvetica", 12), background="orange")
                        yield_label.grid(column=1, row=row_count, padx=5, pady=5, sticky=tk.W)
                    else:
                        query_label = ttk.Label(upper_frame, text=query_string, font=("Helvetica", 12))
                        query_label.grid(column=0, row=row_count, padx=5, pady=5, sticky=tk.W)

                        yield_label = ttk.Label(upper_frame, text=str(entry["yield"]), font=("Helvetica", 12))
                        yield_label.grid(column=1, row=row_count, padx=5, pady=5, sticky=tk.W)
                else:
                    query_string = entry["query"].to_string()
                    if query_string in suggestion_list[-1] and query_string in suggestion_list[-2]:
                        query_label = ttk.Label(upper_frame, text=query_string, font=("Helvetica", 12), background="orange")
                        query_label.grid(column=0, row=row_count, padx=5, pady=5, sticky=tk.W)

                        yield_label = ttk.Label(upper_frame, text=str(entry["yield"]), font=("Helvetica", 12), background="orange")
                        yield_label.grid(column=1, row=row_count, padx=5, pady=5, sticky=tk.W)
                    else:
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


    def insert_suggestions(self, suggestion_list: list[str]) -> tk.Frame:
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