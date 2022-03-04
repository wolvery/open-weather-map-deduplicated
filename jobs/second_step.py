from config import config_execution
from pyspark.sql import SparkSession, DataFrame
from repository.s3_parquet_df import save_parquet
from transformations.aggregations import perform_treatment, max_per_month_and_location, multiple_aggregations


def process():
    first_step_source_path: str = config_execution.get_sink_path("first_step")
    spark = SparkSession.builder.appName("SecondStep").getOrCreate()
    first_step_source_df: DataFrame = spark.read.parquet(first_step_source_path)
    curated_df = first_step_source_df.transform(perform_treatment)

    max_per_month_dataset: DataFrame = curated_df.transform(max_per_month_and_location)
    max_per_month_dataset.show()
    save_parquet(max_per_month_dataset, "second_step")

    aggregated_dataset: DataFrame = curated_df.transform(multiple_aggregations)
    aggregated_dataset.show()
    save_parquet(aggregated_dataset, "third_step")


if __name__ == "__main__":
    process()
