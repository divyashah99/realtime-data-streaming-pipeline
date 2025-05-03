# Navigate to your project directory
cd C:/Users/divya/Repos/ProjectRepo/realtime-data-streaming-pipeline

# Start the Docker containers
docker-compose up -d

# Connect to the Spark master container
docker exec -it realtime-data-streaming-pipeline-spark-master-1 bash

# Submit the Spark job inside the container
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 /opt/bitnami/spark/spark_stream.py


# Connect to the Cassandra container
docker exec -it cassandra bash

# Start the Cassandra Query Language Shell (cqlsh)
cqlsh


# Query the table to see if data is being written
SELECT * FROM spark_streams.created_users LIMIT 10;
