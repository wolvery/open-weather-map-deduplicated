import logging

from controller.weather_data import gather_weather_data
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
from repository.s3_parquet_df import save_parquet
from transformations.deduplicate import setup_deduplicate

STARTING_DATE = "starting_date"
KEYS = ["lat", "lon", "timezone", "starting_date"]


def process():
    logging.info("Getting weather data from open weather map")
    weather_data = gather_weather_data()

    spark = SparkSession.builder.appName("FirstStep").getOrCreate()
    weather_data_df = spark.createDataFrame(weather_data)
    weather_data_star_df = weather_data_df.withColumn(STARTING_DATE, expr("hourly[0].dt"))
    logging.info(f"Removes deduplicated with ${str(KEYS)}")
    weather_data_clean_df = weather_data_star_df.transform(setup_deduplicate(KEYS, STARTING_DATE)).drop(STARTING_DATE)
    logging.info(" Weather data clean:")
    weather_data_clean_df.show()
    save_parquet(weather_data_clean_df, "first_step")


if __name__ == "__main__":
    process()
