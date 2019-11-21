# <p align="center">Find the perfect location for your Company</p>

## <p align="center">Ironhack's Data Analytics Bootcamp Project III: MongoDB Geospatial Queries</p>

![Crunchbase](/images/readme.png)

The goal of this project is to determine the perfect location for a company based on some given criteria:

* Nobody in the company likes to have companies with more than *10* years in a radius of 2 km.
* Developers like to be near successful tech startups that have raised at least *1 Million* dollars.
* Account managers need to travel a lot.
* Executives like Starbucks A LOT. Ensure there's a starbucks not to far.
* The CEO is Vegan.
* All people in the company have between 25 and 40 years, give them some place to go to party.
* 30% of the company have at least 1 child.

I started from a dataset from [Crunchbase](https://www.crunchbase.com/) which contains information on more than 18000 companies (e.g. name, address, coordinates, founded year or total money raised). I cleaned the dataset and enriched it by adding some relevant information extracted from APIs and another datasets. Finally, I filitered the data based on the arguments passed by the user and displayed the final selected location for the company along with all the relevant nearby venues (airports, Starbucks, schools, night clubs and vegan restaurants) in an HTML map using Folium.

### Data cleaning (*cleaningprocess.py*):

1. I imported the data from the Crunchbase JSON file (*companies.json*) to MongoDB Compass.
2. I acquired the data from MongoDB building *find* queries in Pymongo to perform a first filter on the raw data.
3. I cleaned the dataset using Pandas.
4. I created a GeoJSON Object to be able to later perform GeoJSON queries.
5. I Converted the total money raised by each company to US dollars through the [Exchangerate API](https://api.exchangerate-api.com/).
6. I imported the cleaned data (*cleaned_companies.json*) back to MongoDB Compass as a new collection.

### Data filtering and map visualization (*main.py*):

1. The program filters the data based on three the arguments passed by the user:
    * What amount of money should nearby successful tech startups have raised?
    * How old can nearby companies be, at most?
    * What do you prefer to have closer? A Starbucks, a vegan restaurant, a night club or a school?

2. It uses [Foursquare API](https://api.foursquare.com) to supplement the data (requires authentication via token) and a dataset obtained from [Kaggle](https://www.kaggle.com/open-flights/airports-train-stations-and-ferry-terminals), which contains information about all airports in the world and that you can find in the *input* folder (*airports.csv*).

3. Finally, the program calculates the best location for the company and displays it along with all the relevant nearby venues (airports, Starbucks, schools, night clubs and vegan restaurants) in an HTML interactive map using Folium (which opens in a new browser tab).

### Example output:

<p align="center"><img  src="https://github.com/Masdevallia/project-mongodb-geospatial-queries/blob/master/images/output.png" width="700"></p>

<p align="center"><img  src="https://github.com/Masdevallia/project-mongodb-geospatial-queries/blob/master/images/map.png" width="700"></p>

<p align="center"><img  src="https://github.com/Masdevallia/project-mongodb-geospatial-queries/blob/master/images/map2.png" width="700"></p>
 
### Deliverables:

* *cleaningprocess.py*
* *main.py*
* *images* folder: Contains images desplayed in readme.md
* *input* folder:
    * Initial datasets: *companies.json* and *airports.csv*.
    * Cleaned and enriched final dataset in two formats: *cleaned_companies.json* and *companies_df.csv*.
* *output* folder:
    * *map.html* (as an example output)
* *src* folder: Contains functions I have imported and used in the project:
    * *apy.py*: functions related to APIs' usage.
    * *CleanFilter.py*: functions ralated to data cleaning, wrangling and filtering.
    * *input.py*: functions related to displaying the inputs on screen.
    * *mongodb.py*: functions related to establishing connection with MongoDB and executing queries.
    * *output.py*: functions related to displaying the outputs (results) on screen.
