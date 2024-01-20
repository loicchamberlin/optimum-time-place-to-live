## Optimum place to live based on two work place positions

Problematic : Is it possible from two places to get the optimum place to be where it is the fastest to commute ?

Input : 
- **Location A** : address
- **Location B** : address
- **Means of Transport** : int or list of element you can choose from (after)

Output :
1. in a first place : 
    - **Optimum Locations** : List of geocoordinates in order
2. then :
    - **Optimum Area** : Map representation of point of interest

## Process
1. Get the workplace addresses into latitude and longitude coordinates
2. Get the mid geolocalisation in between
3. Optimisation problem : need to find the lowest time for both routes 
    - first based of car routes (done)
    - then adding public transport
4. Results : Roadmap of the different routes

## feature roadmap : 

1. functions : 
    - add a function that calculate the distance between two points for the distance graph creation : DONE
    - graphic functions to help the data analysis use : DONE
    - function to get the top 10 fastest routes : DONE
    - data end user visualisation, add some colors to different route : in progress

2. logic : 
    - avoid using every nodes, just select one for some next to each other == it will optimise the road calculation, select nodes based of a close radius : DONE using Kmeans algorithm
    - find a way to find the fastest route, but one that is equivalent for both time (50/50) : DONE

3. data analysis : 
    - automate the data analysis in order to know what it is happening in the data (time dependency, histogram, min times, ...)
    - data visualisation with library folium : DONE

4. repository : 
    - reorganize the class and 
    - organize the repository
    - create classes for address, roads
    - create a main.py meant for the calculation process
