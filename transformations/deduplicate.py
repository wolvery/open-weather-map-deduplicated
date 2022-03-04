from pyspark.sql import DataFrame
from pyspark.sql.functions import col, row_number, to_timestamp
from pyspark.sql.window import Window


def get_date_column(creation_col):
    return to_timestamp(col(creation_col))


def setup_deduplicate(keys, partition_date):
    def get_deduplicated_df(data_df: DataFrame):
        windowSpec = Window.partitionBy(keys).orderBy(
            get_date_column(partition_date).desc()
        )
        deduplicated_df = (
            data_df.withColumn("row_number", row_number().over(windowSpec))
                .where("row_number == 1")
                .drop("row_number")
        )
        return deduplicated_df

    return get_deduplicated_df
