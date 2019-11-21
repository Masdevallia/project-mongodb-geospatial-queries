
import os
import re
import folium
import fontawesome as fa
from pathlib import Path
import webbrowser


def foliumMap(company,starbucks,vegan,veg_name,party,par_name,name_dist_lat_long_airport,school,sch_name,
near_startups):
    tooltip = 'Click me!'
    map_city = folium.Map(location = company, zoom_start=11)
    folium.Circle(radius=2000,location=company,popup='Old companies free zone',color='#3186cc',
        fill=True,fill_color='#3186cc').add_to(map_city)
    folium.Marker(starbucks,radius=2,icon=folium.Icon(
        icon='coffee', prefix='fa',color='orange'),popup='<b>[Starbucks]</b>',
        tooltip=tooltip).add_to(map_city)
    folium.Marker(vegan,radius=2,icon=folium.Icon(
        icon='cutlery',color='green'),popup=f"<b>[Vegan restaurant]</b> '{veg_name}'",
        tooltip=tooltip).add_to(map_city)
    folium.Marker(party,radius=2,icon=folium.Icon(
        icon='glass',color='purple'),popup=f"<b>[Night club]</b> '{par_name}'",
        tooltip=tooltip).add_to(map_city)
    for i in range(0,len(name_dist_lat_long_airport),4):
        folium.Marker([name_dist_lat_long_airport[i+2],name_dist_lat_long_airport[i+3]],radius=2,icon=folium.Icon(
            icon='plane', prefix='fa',color='blue'),
            popup=f"<b>[Airport]</b> '{name_dist_lat_long_airport[i+0]}'. Distance from the office: {int(name_dist_lat_long_airport[i+1])} km",
            tooltip=tooltip).add_to(map_city)
    folium.Marker(school,radius=2,icon=folium.Icon(
        icon='graduation-cap', prefix='fa',color='gray'),popup=f"<b>[School]</b> '{sch_name}'",
        tooltip=tooltip).add_to(map_city)
    folium.Marker(company,radius=2,icon=folium.Icon(
        icon='briefcase', color='red'),popup='<b>Perfect location for your business</b>',
        tooltip=tooltip).add_to(map_city)
    for startup in near_startups:
        category = re.sub("_"," ",startup[3].capitalize())
        folium.Marker([startup[6], startup[5]],radius=2,icon=folium.Icon(
            icon='building-o', prefix='fa',color='black'),
            popup=f"<b>[Startup]</b> {startup[1]}. Founded year: {int(startup[2])}. Category: {category}. Total money raised (USD): {int(startup[4])}.",
            tooltip=tooltip).add_to(map_city) 
    map_city.save('./output/map.html')
    url = "file://{}{}{}".format(str(Path(os.getcwd())),"/output", "/map.html")
    webbrowser.open(url, 2)




from colorama import init
init()
from colorama import Fore, Back, Style


def printoutput(a,b,c,d,e,f,g,h,i,j,k,l):
    print(Fore.MAGENTA + '''


    ----------------------------------------------------------------------------------------------------
                            WE HAVE FOUND THE PERFECT LOCATION FOR YOUR COMPANY!           
    ----------------------------------------------------------------------------------------------------''')
    print(Fore.WHITE + f'''
        The perfect location for your business is in {a}, {b}.

        You don't have companies with more than {c} years in a radius of 2 km (blue circle).

        The office is near successful tech startups that have raised at least {d} dollars.

        Your employees will find a Starbucks just {e} m from the office.

        The vegan restaurant '{f}' can be found just {g} m from the office.

        Party mood? You will find the night club called '{h}'
        just {i} m from the office.

        If you need to travel often, there is no problem. You have {j} airport/s within 20 km
        from the office.

        And if that were not enough, your children could go to school ({k})
        just {l} m from the office.
    ''')

print(Style.RESET_ALL)

