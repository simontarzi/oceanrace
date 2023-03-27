#****************************************************************************
# (C) Cloudera, Inc. 2020-2022
#  All rights reserved.
#
#  Applicable Open Source License: GNU Affero General Public License v3.0
#
#  NOTE: Cloudera open source products are modular software products
#  made up of hundreds of individual components, each of which was
#  individually copyrighted.  Each Cloudera open source product is a
#  collective work under U.S. Copyright Law. Your license to use the
#  collective work is as provided in your written agreement with
#  Cloudera.  Used apart from the collective work, this file is
#  licensed for your use pursuant to the open source license
#  identified above.
#
#  This code is provided to you pursuant a written agreement with
#  (i) Cloudera, Inc. or (ii) a third-party authorized to distribute
#  this code. If you do not have a written agreement with Cloudera nor
#  with an authorized and properly licensed third party, you do not
#  have any rights to access nor to use this code.
#
#  Absent a written agreement with Cloudera, Inc. (“Cloudera”) to the
#  contrary, A) CLOUDERA PROVIDES THIS CODE TO YOU WITHOUT WARRANTIES OF ANY
#  KIND; (B) CLOUDERA DISCLAIMS ANY AND ALL EXPRESS AND IMPLIED
#  WARRANTIES WITH RESPECT TO THIS CODE, INCLUDING BUT NOT LIMITED TO
#  IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY AND
#  FITNESS FOR A PARTICULAR PURPOSE; (C) CLOUDERA IS NOT LIABLE TO YOU,
#  AND WILL NOT DEFEND, INDEMNIFY, NOR HOLD YOU HARMLESS FOR ANY CLAIMS
#  ARISING FROM OR RELATED TO THE CODE; AND (D)WITH RESPECT TO YOUR EXERCISE
#  OF ANY RIGHTS GRANTED TO YOU FOR THE CODE, CLOUDERA IS NOT LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
#  CONSEQUENTIAL DAMAGES INCLUDING, BUT NOT LIMITED TO, DAMAGES
#  RELATED TO LOST REVENUE, LOST PROFITS, LOSS OF INCOME, LOSS OF
#  BUSINESS ADVANTAGE OR UNAVAILABILITY, OR LOSS OR CORRUPTION OF
#  DATA.
#
# #  Author(s): Tarzíciusz Pál Simon
#***************************************************************************/

import configparser
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import pyspark.sql.functions as F
#from pyspark.sql.functions import col

config = configparser.ConfigParser()
config.read('/app/mount/parameters.conf')
data_lake_name=config.get("general","data_lake_name")
s3BucketName=config.get("general","s3BucketName")
username=config.get("general","username")

print("Running script with Username: ", username)

# CREATE SPARK SESSION
spark = SparkSession.builder.appName('INGEST').config("spark.yarn.access.hadoopFileSystems", data_lake_name).getOrCreate()

# LOAD DATA FROM .CSV FILES ON AWS S3 CLOUD STORAGE
met_data = spark.read.csv(s3BucketName + "/MeteorologicalData",        header=True, inferSchema=True) 
mp_data  = spark.read.csv(s3BucketName + "/MicroPlasticData/MicroPlasticData.csv",        header=True, inferSchema=True) 
osu_data  = spark.read.csv(s3BucketName + "/OceanographicSurfaceUnderwayData/OceanographicSurfaceUnderway_data.csv",        header=True, inferSchema=True) 

rownummet=met_data.count()
rownummp=mp_data.count()
rownumosu=osu_data.count()

print(f"\ttotal number of records in meteorological data files {rownummet}")
print(f"\ttotal number of records in microplastic data {rownummp}")
print(f"\ttotal number of records in OceanographicSurfaceUnderwayData {rownumosu}")

# SQL DROP DATABASE

print("JOB STARTED...")
spark.sql("DROP DATABASE IF EXISTS {}_OCEANRACE_DATA CASCADE".format(username))
print("\tDROP DATABASE(S) COMPLETED")

# CREATE DATABASE
spark.sql("CREATE DATABASE {}_OCEANRACE_DATA".format(username))
print("\tCREATE DATABASE(S) COMPLETED")

# Remove rows which has out of range latitude and longitude values
print("\tSTARTING THE REMOVAL ROWS WHICH HAS OUT OF BOUND VALUES")
met_data = met_data.filter(F.col("LAT").between(-90,90))
met_data = met_data.filter(F.col("LONG").between(-180,180))

mp_data = mp_data.filter(F.col("Longitude").between(-180,180))
mp_data = mp_data.filter(F.col("Latitude").between(-90,90))

osu_data = osu_data.filter(F.col("Latitude").between(-90,90))
osu_data = osu_data.filter(F.col("Longitude").between(-180,180))

rownummet2=met_data.count()
rownummp2=mp_data.count()
rownumosu2=osu_data.count()

print(f"\tremoved records from meteorological data {rownummet-rownummet2}")
print(f"\tremoved records from microplastic data after filtering {rownummp-rownummp2}")
print(f"\tremoved records from OceanographicSurfaceUnderwayData after filtering {rownumosu-rownumosu2}")

print("\tREMOVAL FINISHED")

# ENRICH DATA
print("\tSTARTING THE ENRICHMENT PROCESS, ADDING COLUMNS WITH ROUNDED LAT&LONG VALUES")

met_data = met_data.withColumn("r_lat", F.round(met_data["LAT"], 0))
met_data = met_data.withColumn("r_lon", F.round(met_data["LONG"], 0))
met_data = met_data.withColumn("1r_lat", F.round(met_data["LAT"], 1))
met_data = met_data.withColumn("1r_lon", F.round(met_data["LONG"], 1))

mp_data = mp_data.withColumn("r_lat", F.round(mp_data["Latitude"], 0))
mp_data = mp_data.withColumn("r_lon", F.round(mp_data["Longitude"], 0))
mp_data = mp_data.withColumn("1r_lat", F.round(mp_data["Latitude"], 1))
mp_data = mp_data.withColumn("1r_lon", F.round(mp_data["Longitude"], 1))

osu_data = osu_data.withColumn("r_lat", F.round(osu_data["Latitude"], 0))
osu_data = osu_data.withColumn("r_lon", F.round(osu_data["Longitude"], 0))
osu_data = osu_data.withColumn("1r_lat", F.round(osu_data["Latitude"], 1))
osu_data = osu_data.withColumn("1r_lon", F.round(osu_data["Longitude"], 1))

print("\tENRICHMENT DONE")

print("\tSHOW TABLES")
met_data.show()
mp_data.show()
osu_data.show()

# POPULATE TABLES

met_data.write.mode("overwrite").saveAsTable('{}_OCEANRACE_DATA.MET_DATA'.format(username), format="parquet")
mp_data.write.mode("overwrite").saveAsTable('{}_OCEANRACE_DATA.MP_DATA'.format(username), format="parquet")
osu_data.write.mode("overwrite").saveAsTable('{}_OCEANRACE_DATA.OSU_DATA'.format(username), format="parquet")

print("\tPOPULATE TABLE(S) COMPLETED")

print("JOB COMPLETED.\n\n")