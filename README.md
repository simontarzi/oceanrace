# Ocean Race data visualization 2017-2018
## Overview

The Ocean Race is often described as the longest and toughest professional sporting event in the world, sailing’s toughest team challenge and one of the sport’s Big Three events, alongside the Olympic Games and America’s Cup.

The Race starts on 22 October 2017 from Alicante and finished eight months later in The Hague.

At 45,000nm, this will be the longest course in the history of the race (previous longest racecourse was 39,270 in 2011-12.).

It crosses four oceans and take in 12 major cities: Alicante, Lisbon, Cape Town, Melbourne, Hong Kong, Guangzhou, Auckland, Itajaí, Newport RI, Cardiff, Gothenburg and The Hague.

> Volvo Ocean Race Science Programme was funded by Volvo Cars, who have donated €100 from first 3,000 sales of the new Volvo V90 Cross Country Volvo Ocean Race edition to support the initiative. 

![Route](https://github.com/simontarzi/oceanrace/blob/main/pics/Screenshot%202023-02-10%20at%2022.59.40.png)


## Data collected during the race (3 data sets)

The microplastic particle information was collected from seawater samples taken during the Volvo Ocean Race, which, for the first time, combined a global sporting event with cutting-edge scientific research.
The science initiative, part of the race’s Sustainability Programme, was presented at the MICRO2018 conference, which heard about leading research related to microplastic pollution.

![Microplastic1](https://github.com/simontarzi/oceanrace/blob/main/pics/Screenshot%202023-02-10%20at%2023.00.01.png)

The oceanographic data were collected onboard "Turn the Tide on Plastic" and team "AkzoNobel". 
The meteorological data were collected by Dongfeng Race Team, Team Brunel, Vestas 11th Hour Racing, Sun Hung Kai Scallywag, Turn the Tide on Plastic, Mapfre and Team AkzoNobel.

![Microplastic2](https://github.com/simontarzi/oceanrace/blob/main/pics/Screenshot%202023-02-10%20at%2023.00.21.png)

## Ingestion and enrichment with Spark

The oceanrace_ingestion.py loads the data from an S3 storage bucket, and enriches the tables with additional latitude and longitude values rounded to 1 decimal and to integer in additional columns to provide usable format for visualization. 

| decimal places | degrees  | distance  | 
|---|---|---|
| 0  | 1  |  111  km |
|  1 | 0.1  | 11.1 km  |
|  2 |  0.11 |  1.11 km |
|  3 |  0.111 |  111  m |
|  4 |  0.1111 | 11.1 m  |
|  5 |  0.11111 | 1.11 m  |

The distance of the race is 60.000km, integer and 1 decimal place coordinates would give us appropriate high-level view, but in some places the rounded coordinates have been placed to land near the shore. 

Also the latitude and longitude values been out-of-range for the visualization, therefore the script filters these values as well. 

In the official microparticle csv, the latitude and longitude coordinates have been swapped, this was manually corrected.  

Meteorological data has not been uploaded to github because of it's size, it can be downloaded directly via the link at the bottom. The oceanrace_ingestion.py has to be pointing to the directory which contains the meteorological csvs, and will ingest all the csv in the folder. 

## Important

the dataviz json has been preset with a username "tsimon", therefore it has to be replaced with the exact username set in oceanrace_ingestion.py
add mapbox token
connection should be manually configured before uploading the dataviz json file to the correct CDW Hive. 

## Output of spark job

	total number of records in meteorological data files 6688096
	total number of records in microplastic data 358199
	total number of records in OceanographicSurfaceUnderwayData 16035
  
  	removed records from meteorological data 10280
	removed records from microplastic data after filtering 4889
	removed records from OceanographicSurfaceUnderwayData after filtering 0

## Links
Expert conference link: https://archive.theoceanrace.com/en/news/12202_Race-data-revealed-at-expert-conference.html 

Science report: https://drive.google.com/file/d/1y0sJEghnWx_Txn7Zy4l33WZsl_3Zddwq/view 

Download open-access data: https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.nodc:0170967 
