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

For the second process, you can either : 
- Choisir un périmètre fixe, trouver les premiers endroits les plus rapides [**méthode à trouver**] pour aller à l'addresse n, puis vérifier si ces endroits s'intersectent à condition d'être à une certaine distance l'un de l'autre. Si oui, garder la position moyenne entre les deux endroits. Sinon, recommencer en augmentant la périmètre de recherche.
 --> méthode surement inutile sur Paris/IDF car le temps de route en ville peut être raccourcis même en dehors de la même zone
- Méthode en utilisant l'API routes de google
- s'inspirer du post medium : https://medium.com/towards-data-science/modern-route-optimization-with-python-fea87d34288b

feature roadmap : 

functions : 
- add a functions that calculate the distance between two points for the distance graph creation
- graphic functions to help the data analysis use
- maybe reorganize the class and organize the repo
- function to get the top 10 fastest routes

logic : 
- avoid using every nodes, just select one for some next to each other == it will optimise the road calculation
- find a way to find the fastest route, but one that is equivalent for both time (50/50)

data analysis : 
- automate the data analysis in order to know what it is happening in the data (time dependency, histogram, min times, ...)
- data visualisation with library folium
