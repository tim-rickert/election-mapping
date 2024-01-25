This script maps county-level elections for Presidential and Senate races for specified years.

Author: Tim Rickert (rickertti@gmail.com)

Data is open-sourced from Algara and Amlani (2021) "Replication Data for: Partisanship & Nationalization in American Elections: Evidence from Presidential, Senatorial, & Gubernatorial Elections in the U.S. Counties, 1872-2020" https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DGUMFI

Package requirements are outlined in the `requirements.txt` file and can be written to a Python virtual environment via `pip install -r requirements.txt` from the command line

To run the example script to see how it works, just run `python script/map.py` from the command line

Still very much a WIP, I want to use Dash to code an interactive frontend, extend the analysis to Senate and Gubernatorial races (the data is there and this can easily be added), and make the mapping more robust to third-party candidacies because right now it only works for two-party Democratic/Republican matchups

One could also use the GeoJSON / Plotly segments of the code to map stuff at the precinct level, looks like the data exists here