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

rownummet=met_data.count()


print(f"\ttotal number of records in meteorological data files {rownummet}")


# Remove rows which has out of range latitude and longitude values
print("\tSTARTING THE REMOVAL ROWS WHICH HAS OUT OF BOUND VALUES")
met_data = met_data.filter(F.col("LAT").between(-90,90))
met_data = met_data.filter(F.col("LONG").between(-180,180))


rownummet2=met_data.count()


print(f"\tremoved records from meteorological data {rownummet-rownummet2}")


print("\tREMOVAL FINISHED")

# ENRICH DATA
print("\tSTARTING THE ENRICHMENT PROCESS, ADDING COLUMNS WITH ROUNDED LAT&LONG VALUES")

met_data = met_data.withColumn("r_lat", F.round(met_data["LAT"], 0))
met_data = met_data.withColumn("r_lon", F.round(met_data["LONG"], 0))
met_data = met_data.withColumn("1r_lat", F.round(met_data["LAT"], 1))
met_data = met_data.withColumn("1r_lon", F.round(met_data["LONG"], 1))

print("\tENRICHMENT DONE")

print("\tSHOW TABLES")
met_data.show()

# POPULATE TABLES

met_data.write.mode("overwrite").saveAsTable('{}_OCEANRACE_DATA.MET_DATA'.format(username), format="parquet")

print("\tPOPULATE TABLE(S) COMPLETED")

print("JOB COMPLETED.\n\n")