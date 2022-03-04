import logging

from config import config_execution
from pyspark.sql import DataFrame


def save_parquet(data_df: DataFrame, step_name):
    path = config_execution.get_sink_path(step_name)
    logging.info(f"Saving to path: %{path}")
    data_df.write.mode("overwrite").parquet(path=path)
