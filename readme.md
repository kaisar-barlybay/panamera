# Quick start
In main.py file modify job literal, where it should be **find_place**, **parse**, **visualize** and run the script. 

1. It's more safe to parse in batches and then concatenate the dataframes into one, rather than catch some error in middle and loose all data. Therefore you need additionally provide page range if you are running **parse** job.

1. **find_place** job was executed separetely, because it needed to access 2GIS API, which could slow the process of parsing.

1. **visualize** job cleans the data and draws some graphics.

The scraped data is contained in source directory - by batches and in krisha_1-502.csv - concatenated as one dataframe. Also in repository there are krisha_1-502_with_geo.csv dataframe, which contains the same data but with longitude and latitude.