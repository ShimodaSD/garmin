from pyspark.sql import SparkSession
import pyspark
import glob

def read_data(spark: SparkSession):
    files = glob.glob('./HealthData/FitFiles/Activities/activity_details_*.json')
    if not files:
        raise FileNotFoundError("No matching JSON files found!")
    df = spark.read.option('multiline', 'true').json(files)
    return df

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("Garmin Data Processing") \
        .getOrCreate()
    df = read_data(spark)
    df = df.select("summaryDTO")
    
    #df.show(truncate=False)

