FROM guisigo/spark-minio:latest
ADD . open-weather-map
RUN pip install -r open-weather-map/requirements.txt
