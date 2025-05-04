# Real-Time Data Streaming Pipeline

A scalable data pipeline that streams user data from a public API through Kafka, processes it with Spark, and stores it in Cassandra, all orchestrated with Airflow.

## Project Overview

This project demonstrates a complete end-to-end data engineering pipeline that processes streaming data in real-time. It fetches random user profiles from a public API, streams them through a messaging system, processes the data, and stores it in a NoSQL database.

The pipeline is designed with scalability in mind, using industry-standard tools for each component:

- **Data Source**: Random user data is fetched from the [RandomUser API](https://randomuser.me/api/)
- **Orchestration**: Apache Airflow schedules and monitors the data fetching process
- **Messaging**: Apache Kafka handles the streaming data with fault tolerance
- **Processing**: Apache Spark performs real-time stream processing
- **Storage**: Apache Cassandra provides a distributed NoSQL database for the processed data
- **Deployment**: Docker containers ensure consistent environments and easy deployment

This architecture follows modern data engineering principles, allowing for horizontal scaling, fault tolerance, and real-time data processing. It can be adapted for various use cases such as user analytics, real-time dashboards, or as a foundation for more complex data pipelines.

## Video Demonstration

[![Real-Time Data Streaming Pipeline Demo]](https://github.com/divyashah99/realtime-data-streaming-pipeline/blob/master/video-demo/FinalDemo.mp4)

## Architecture

![Architecture Diagram](architecture_diagram.png)

## Components

- **Apache Airflow**: Orchestrates the data pipeline and schedules API data fetching
- **Apache Kafka**: Handles real-time data streaming
- **Apache Spark**: Processes streaming data
- **Apache Cassandra**: NoSQL database for storing processed data
- **Docker & Docker Compose**: Containerization for easy deployment

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Setup and Running

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd realtime-data-streaming-pipeline
   ```

2. Start the Docker containers:
   ```bash
   docker-compose up -d
   ```

3. Access the services:
   - Airflow: http://localhost:8080 (username: admin, password: admin)
   - Kafka Control Center: http://localhost:9021
   - Spark Master UI: http://localhost:9090

## Data Flow

1. Airflow DAG fetches random user data from an external API
2. Data is published to Kafka topic 'users_created'
3. Spark Streaming consumes the Kafka topic
4. Processed data is stored in Cassandra

## Running the Spark Job

Connect to the Spark master container and submit the job:

```bash
docker exec -it realtime-data-streaming-pipeline-spark-master-1 bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 /opt/bitnami/spark/spark_stream.py
```

## Querying Data in Cassandra

Connect to the Cassandra container and run queries:

```bash
docker exec -it cassandra bash
cqlsh

# View stored data
SELECT * FROM spark_streams.created_users LIMIT 10;
```

## Project Structure

- `dags/`: Airflow DAG definitions
- `script/`: Setup scripts
- `spark_stream.py`: Spark streaming application
- `docker-compose.yml`: Docker services configuration
