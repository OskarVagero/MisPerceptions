)# How (mis-)perceptions influence the acceptance of wind power deployment – can Energy Justice contribute to reaching a socio-technical tipping point?
This repository is based on work performed within the HORIZON 2020 project WIMBY (Wind In My Backyard: Using holistic modelling tools to advance social awareness and engagement on large wind power installations in the EU)

## Sentiment analysis of Twitter data
Particularly, this repository contains the scripts and some supporting data for the sentiment analysis of social media content. 

### Flowchart of the overarching process

### Cities & locations included in different countries (places_country.csv). 
We currently operate with an allowlist of places within a country, following the methodology of [Bruns et al. (2017)](https://doi.org/10.1177/2056305117748162). Due to data availability, the country allowlists has to be constructed and verified differently, based on what data is available. 

For **Austria**, the places are sourced from [Wikipedia](https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Austria), and covers 98.87% of Austria's population. For **France**, the places are sourced from [Banatic](https://www.banatic.interieur.gouv.fr/V5/fichiers-en-telechargement/fichiers-telech.php) and available in English through the sublinks of [this Wikipedia page](https://en.wikipedia.org/wiki/Lists_of_communes_of_France). Currently, there is no verification of how much of the population is covered, however, it is known to be greater than 40%. With 6941 different locations, it is expected to be comprehensive. 

 
An alternative approach could be to just throw the text string into a geolocation program, although this might cause problems if there are multiple locations in the world with the same name. 
