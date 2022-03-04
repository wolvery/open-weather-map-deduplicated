from pyspark.sql import DataFrame
from pyspark.sql.functions import desc, month, dayofmonth, year, row_number, avg, expr, max
from pyspark.sql.window import Window


def perform_treatment(raw_weather_data_df: DataFrame):
    return (
        raw_weather_data_df
            .selectExpr("struct(lat,lon) as location", "explode(hourly) as hourly")
            .selectExpr("location", "to_timestamp(hourly.dt) as date_temp", "hourly.temp as temp")
    )


def max_per_month_and_location(weather_data_df: DataFrame):
    return (weather_data_df
            .groupby("location", month("date_temp").alias("month"), year("date_temp").alias("year"), "temp")
            .agg(max("temp").alias("max")))


def multiple_aggregations(weather_data_df: DataFrame):
    window_spec_min = Window.partitionBy(dayofmonth("date_temp"), month("date_temp"), year("date_temp")).orderBy("temp")
    window_spec_max = Window.partitionBy(dayofmonth("date_temp"), month("date_temp"), year("date_temp")).orderBy(
        desc("temp"))
    control_weather_df = (
        weather_data_df
            .withColumn("row_min", row_number().over(window_spec_min))
            .withColumn("row_max", row_number().over(window_spec_max))
            .withColumn("avg_min", avg("temp").over(window_spec_min))
    )
    clean_control_weather_df = (
        control_weather_df
            .where("row_max == 1 or row_min == 1")
            .withColumn("max_temperature", expr("row_max == 1"))
            .withColumn("min_tempurature", expr("row_min == 1")).drop("row_max", "row_min")
    )

    return clean_control_weather_df
