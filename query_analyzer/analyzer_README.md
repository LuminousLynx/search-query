# Query Analyzer

Query Analyzer is an optional extension of the search-query package. It allows the user to analyze the yield of the search query they built with search-query. Momentarily, it depends on the CoLRev environment to perform searches in Crossref for demo purposes. Other search sources or environments may be implemented in the future. 

The program can be used programmatically after building a query with search-query. 


## Installation

Query Analyzer is installed automatically during the installation of search-query. To successfully use the demo of Query Analyzer, CoLRev needs to be installed.

To install search-query, run:

```
pip install search-query
```

To install CoLRev, run:

```
pip install colrev
```


## Programmatic use

To run Query Analyzer, create a python file and import Query Analyzer and all necessary query types. Secondly, code in your query with search-query and call the analyzer with your query as a parameter. Finally, execute the file through your IDE. The following example file shows the basic steps in python code:

```Python
# Import Query types and Query Analyzer
from search_query import OrQuery, AndQuery
from query_analyzer impoer QueryAnalyzer

# Build your query programmatically with search-query
digital_synonyms = OrQuery(["digital", "virtual", "online"], search_field="Abstract")
work_synonyms = OrQuery(["work", "labor", "service"], search_field="Abstract")
query = AndQuery([digital_synonyms, work_synonyms], search_field="Author Keywords")

# Now, call Query Analyzer:
analyzer = QueryAnalyzer()
analyzer.analyze_yield(query=query, platform="crossref")
```

Parameters for Query Analyzer:

- query: the query object built within the file
- platform: the search source where you want to perform the query (for now, only crossref is accessible)


## UI

The results of the analysis of your query will be displayed in a simple Graphic User Interface (GUI). The upper partition of the GUI window displays your full query at the top left and the corresponding yield on the top right. The lines below indicate the respective yields of every subquery of your query. This visualization allows to identify problematic terms - those, whose yield is either extremely high or too low. 
The lower partition of the GUI displays the program's analysis of the yields, shows the identified problematic area and gives a recommendation on how to refine that specific area of the query. 

To refine the query according to the analysis, simply close the GUI window and edit the query in the python file.


## How to cite

Query Analyzer was developed as part of the following Bachelor's thesis:

- Theis, R. (2024). Analyzing the yield of literature search queries: An open-source design science approach. Otto-Friedrich-University of Bamberg.


## Not what you are looking for?

If Query Analyzer is not the right tool for your analysis, it might be worth it to look at these related programs:

[litsearchr](https://github.com/elizagrames/litsearchr.git) -> an R package for query refinement (Grames et al., 2019)
[searchrefiner](https://github.com/ielab/searchrefiner.git) -> a tool for query visualization and analysis (Scells & Zuccon, 2018)


## License

This project is distributed under the [MIT License](LICENSE).
