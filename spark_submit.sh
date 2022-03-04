#!/bin/bash

/opt/spark/bin/spark-submit --conf "spark.hadoop.fs.s3a.endpoint"='http://minio1:9000' \
  --conf spark.hadoop.fs.s3a.access.key='minio' \
  --conf spark.hadoop.fs.s3a.secret.key='minio123' \
  --conf spark.hadoop.fs.s3a.fast.upload=True \
  --conf "spark.hadoop.fs.s3a.path.style.access"=True \
  --conf "spark.hadoop.fs.s3a.impl"="org.apache.hadoop.fs.s3a.S3AFileSystem" main.py



