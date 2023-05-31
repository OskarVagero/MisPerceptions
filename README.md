# How (mis-)perceptions influence the acceptance of wind power deployment – can Energy Justice contribute to reaching a socio-technical tipping point?
This repository is based on work performed within the [HORIZON 2020 project WIMBY (Wind In My Backyard: Using holistic modelling tools to advance social awareness and engagement on large wind power installations in the EU)](https://cordis.europa.eu/project/id/101083460).

## Sentiment analysis of Twitter data
Particularly, this repository contains the scripts and some supporting data for the sentiment analysis of social media content. 

### Flowchart of the overarching process

### Cities & locations included in different countries (places_country.csv). 
We currently operate with an allowlist of places within a country, following the methodology of [Bruns et al. (2017)](https://doi.org/10.1177/2056305117748162). Due to data availability, the country allowlists have to be constructed and verified differently, based on what data is available. 

* For **Austria**, the places are sourced from [Wikipedia](https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Austria), and covers 98.87% of Austria's population. 
* For **Denmark**, the places include 243 urban areas (_byområder_), together covering 72.11% of the Danish population. It excludes rural areas (_landdistrikter_), which are locations with less than 200 people. The list is from  [Wikipedia](https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Denmark). More detailed information may be available at [Danmarks Statistik](https://www.statistikbanken.dk/statbank5a/SelectVarVal/Define.asp?Maintable=BEF4&PLanguage=0)
* For **France**, the places are sourced from [Banatic](https://www.banatic.interieur.gouv.fr/V5/fichiers-en-telechargement/fichiers-telech.php) and available in English through the sublinks of [this Wikipedia page](https://en.wikipedia.org/wiki/Lists_of_communes_of_France). Currently, there is no verification of how much of the population is covered, however, it is known to be greater than 40%. With 6941 different locations, it is expected to be comprehensive. 
* For **Germany**, the list contain 2055 cities and towns, sourced from [Wikipedia](https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Germany). Currently, it does not include population data, but a potential data source is [Statistikportal.de](https://www.statistikportal.de/de/gemeindeverzeichnis).
* For **Italy**, the places include all municipalities of the 107 provinces, resulting in 7817 places for Italy. These locations cover 100% of the population, according to data from [The Italian National Institute of Statistics](https://demo.istat.it/app/?i=D7B&a=2023&l=en)
* For **Norway**, the places include _townships_ of at least 200 people within 50 meter of one another and covers at least 82.67% of the population, based on numbers from [Statistics Norway](https://www.ssb.no/befolkning/folketall/statistikk/tettsteders-befolkning-og-areal). 

### Data overview
|             | Austria | Denmark | France | Germany | Italy | Ireland | Norway | 
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| Raw tweets      | 1,097,818 | 79,571 | 1,943,353 | 1,097,818 | 313,188 | | 118,439 |
| Excluded due to lack of geodata  | 368,722 | 22,515 | 648,304 | 368,722 | 114,351 |  | 31,769 |
| Tweets with geolocation | 729,091 | 57,056 | 1,295,049 | 729,091 | 198,837 |  | 86,670 |
| Tweets excluded due to illegible geodata | 450,050 | 39,588 | 305,552 | 300,541 | 51,131 |  | 22,827 |
| Final sample of tweets | 278,907 | 17,443 | 989,237 | 428,416 | 147,680 | | 63,830 |
| Tweets per million inhabitants | 
| Population covered | 99% | 72% | | |100% | | 83% |

#### Austria
![at_temporal](figures/AT_temporal.svg)

#### Denmark
![dk_temporal](figures/DK_temporal.svg)
![dk_geospatial](figures/dk_geospatial.svg)

#### Germany
![de_temporal](figures/DE_temporal.svg)
![de_geospatial](figures/de_geospatial.svg)

#### France
![fr_temporal](figures/FR_temporal.svg)
![fr_geospatial](figures/fr_geospatial.svg)

#### Italy
![it_temporal](figures/IT_temporal.svg)
![it_geospatial](figures/it_geospatial.svg)

#### Norway
![no_temporal](figures/NO_temporal.svg)
![no_geospatial](figures/no_geospatial.svg)
