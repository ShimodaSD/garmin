from pyspark.sql import SparkSession
import pyspark
import glob
from pyspark.sql.functions import from_json, col
from delta import *

def read_data(spark: SparkSession):
    files = glob.glob('../HealthData/FitFiles/Activities/activity_details_*.json')
    if not files:
        raise FileNotFoundError("No matching JSON files found!")
    df = spark.read.option('multiline', 'true').json(files)
    df_summary = df.select("summaryDTO.*")
    return df_summary

def save_data_to_delta(df):
    df.coalesce(1).write\
        .format("parquet")\
        .mode("overwrite")\
        .save("bronze_data/activities_delta")

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("Garmin Data Processing") \
        .getOrCreate()
        #.config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        #.config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        
    df = read_data(spark)
    save_data_to_delta(df)
    spark.stop()

