## Optimum place to live based on two work place positions

Problematic : Is it possible from two places to get the optimum place to be where it is the fastest to commute ?

Input : 
- **Location A** : address
- **Location B** : address
- **Means of Transport** : int or list of element you can choose from (after)

Output :
1. in a first place : 
    - **Optimum Location** : address
2. then :
    - **Optimum Area** : coordinates (center of the area)

## Process
1. Need to convert work place positions into latitude and longitude coordinates
    - For Later : add a mean to verify if the address used exists
2. Optimisation problem : need to find the lowest time for both routes 
    - first based of car routes
    - then adding public transport