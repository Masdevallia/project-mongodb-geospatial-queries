# <p align="center">Find the perfect location for your Company</p>

## <p align="center">Ironhack's Data Analytics Bootcamp Project III: MongoDB Geospatial Queries</p>

The goal of this project is to determine the perfect location for a company based on some given criteria (to choose at least 3 of the following):

* Nobody in the company likes to have companies with more than 10 years in a radius of 2 km.
* Developers like to be near successful tech startups that have raised at least 1 Million dollars.
* Account managers need to travel a lot.
* Executives like Starbucks A LOT. Ensure there's a starbucks not to far.
* The CEO is Vegan.
* All people in the company have between 25 and 40 years, give them some place to go to party.
* 30% of the company have at least 1 child.
* Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.

### Data cleaning (*cleaningprocess.py*):

1. I imported the data from the Crunchbase JSON file (*companies.json*) to MongoDB Compass.
2. I acquired the data from MongoDB building *find* queries in Pymongo to perform a first filter on the raw data.
3. I cleaned the dataset using Pandas.
4. I created a GeoJSON Object.
5. I Converted the total money raised by each company to US dollars through the [Exchangerate API](https://api.exchangerate-api.com/).
6. I imported the cleaned data back to MongoDB Compass as a new collection.

### Data filtering and map visualization (*main.py*):

## 

<p align="center"><img  src="https://github.com/Masdevallia/project-mongodb-geospatial-queries/blob/master/images/output.png" width="700"></p>

<p align="center"><img  src="https://github.com/Masdevallia/project-mongodb-geospatial-queries/blob/master/images/map.png" width="700"></p>

<p align="center"><img  src="https://github.com/Masdevallia/project-mongodb-geospatial-queries/blob/master/images/map2.png" width="700"></p>

## 

### Deliverables:

* *cleaningprocess.py*
* *main.py*
* *images* folder: Contains images desplayed in readme.md
* *input* folder:
    * Initial data sets: *companies.json* and *airports.csv*.
    * Cleaned and enriched final data set in two formats: *cleaned_companies.json* and *companies_df.csv*.
* *output* folder:
    * *map.html* (as an example output)
* *src* folder: Contains functions I have imported and used in the project:
    * *apy.py*: functions related to APIs' usage.
    * *CleanFilter.py*: functions ralated to data cleaning, wrangling and filtering.
    * *input.py*: functions related to displaying the inputs on screen.
    * *mongodb.py*: functions related to establishing connection with MongoDB and executing queries.
    * *output.py*: functions related to displaying the outputs (results) on screen.
