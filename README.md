# Ocean Race data visualization 2017-2018
## Overview

The Ocean Race is often described as the longest and toughest professional sporting event in the world, sailing’s toughest team challenge and one of the sport’s Big Three events, alongside the Olympic Games and America’s Cup.

The Volvo Ocean Race started on 22 October 2017 from Alicante and finished eight months later in The Hague. The latest race is renamed to Ocean Race and started on 15 January 2023. 

> Volvo Ocean Race Science Programme was funded by Volvo Cars, who have donated €100 from first 3,000 sales of the new Volvo V90 Cross Country Volvo Ocean Race edition to support the initiative. 

The 2017 race was 45,000nm, this was the longest course in the history of the race (previous longest racecourse was 39,270 in 2011-12.).
It crossed four oceans and take in 12 major cities: Alicante, Lisbon, Cape Town, Melbourne, Hong Kong, Guangzhou, Auckland, Itajaí, Newport RI, Cardiff, Gothenburg and The Hague.

## Motivation
2022-2023 Ocean Race: The round-the-world sailing race will measure microplastic pollution, gather information about the impact of climate change on the ocean and collect data to improve global weather forecasting! This is the most ambitious and comprehensive science programme created by a sporting event. 

Every boat participating in the gruelling six-month around-the-world race will carry specialist equipment onboard to measure a range of variables throughout the 60,000km route, which will be analysed by scientists from eight leading research organisations to further understanding about the state of the ocean. Sailing through some of the most remote parts of the planet, seldom reached by scientific vessels, teams will have a unique opportunity to collect vital data where information is lacking on two of the biggest threats to the health of the seas: the impact of climate change and plastic pollution. 

Launched during the 2017-18 edition of the Race in collaboration with 11th Hour Racing, Premier Partner of The Ocean Race and Founding Partner of the Racing with Purpose sustainability programme, the innovative science programme will capture even more types of data in the forthcoming Race, including for the first time levels of oxygen and trace elements in the water. Data will also be delivered to science partners faster in this edition, transmitted via satellite and reaching the organisations, which includes World Meteorological Organization, National Oceanography Centre, Max Planck Society, Centre National de la Recherche Scientifique and National Oceanic and Atmospheric Administration, in real time.

> The data visualization is impressive, however it will provide much more insight together with the newest dataset gathered during the latest race. 

![Route](https://github.com/simontarzi/oceanrace/blob/main/pics/Screenshot%202023-02-24%20at%2016.40.11.png)


## Data collected during the race (3 data sets)

The microplastic particle information was collected from seawater samples taken during the Volvo Ocean Race, which, for the first time, combined a global sporting event with cutting-edge scientific research.
The science initiative, part of the race’s Sustainability Programme, was presented at the MICRO2018 conference, which heard about leading research related to microplastic pollution.

![Microplastic1](https://github.com/simontarzi/oceanrace/blob/main/pics/Screenshot%202023-02-24%20at%2016.41.05.png)

The oceanographic data were collected onboard "Turn the Tide on Plastic" and team "AkzoNobel". 
The meteorological data were collected by Dongfeng Race Team, Team Brunel, Vestas 11th Hour Racing, Sun Hung Kai Scallywag, Turn the Tide on Plastic, Mapfre and Team AkzoNobel.

![Microplastic2](https://github.com/simontarzi/oceanrace/blob/main/pics/Screenshot%202023-02-24%20at%2016.41.33.png)

![Microplastic3](https://github.com/simontarzi/oceanrace/blob/main/pics/Screenshot%202023-02-24%20at%2016.42.16.png)

## Ingestion and enrichment with Spark 

CDE was used to run the oceanrace_ingestion_onejob.py which loads the data from an S3 storage bucket, and enriches the tables with additional latitude and longitude values rounded to 1 decimal and to integer in additional columns to provide usable format for visualization. Later on DataViz is used for data visualization. 

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

You can also use the Airflow editor to prepare the 3 data sets in parallel, for that first place the oceanrace_ingestion_p0 as individual job, and connect the three jobs ending with "p1A" "p1B" 'p1C" in parallel like on the image: 
![airflow](https://github.com/simontarzi/oceanrace/blob/main/pics/Screenshot%202023-03-27%20at%2014.01.37.png)

No changes required in the spark jobs, only the parameters.conf has to be adjusted, and in that case only the username if you are using the sandbox env. 

## CDW - DataViz steps

the dataviz json has been preset with a username "tsimon", therefore it has to be replaced with the exact username set in the parameters.conf
also please use your own mapbox token if you are using this demo frequently on the dataviz UI. 

Steps to connect to a CDW virtual warehouse

Go to Data and Create a new connection: 
![dviz1](https://github.com/simontarzi/oceanrace/blob/main/pics/Screenshot%202023-03-27%20at%2013.46.11.png)

Select the warehouse that you would like to use Hive or Impala, connection name is oceanrace, leave everything as predefined and hit test to verify:
![dviz2](https://github.com/simontarzi/oceanrace/blob/main/pics/Screenshot%202023-03-27%20at%2013.46.59.png)

To import a visual, under Data hit the three dots, and Import Visual Artifacts: 
![dviz3](https://github.com/simontarzi/oceanrace/blob/main/pics/Screenshot%202023-03-27%20at%2013.47.16.png)

Select the file that you previously downloaded and modified the username to you own, hit import: 
![dviz4](https://github.com/simontarzi/oceanrace/blob/main/pics/Screenshot%202023-03-27%20at%2013.47.44.png)

You will se this windows, hit accept and import:
![dviz5](https://github.com/simontarzi/oceanrace/blob/main/pics/Screenshot%202023-03-27%20at%2013.47.56.png)

Please make sure that the CDW virtual warehouse is running! 
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
