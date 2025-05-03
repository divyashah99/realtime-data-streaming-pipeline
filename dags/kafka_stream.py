import uuid
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2023, 9, 3, 10, 00)
}

def get_data():
    import requests
    import logging

    try:
        res = requests.get("https://randomuser.me/api/")
        res = res.json()
        if 'results' in res and len(res['results']) > 0:
            return res['results'][0]
        else:
            logging.error("API response doesn't contain expected data structure")
            return None
    except Exception as e:
        logging.error(f"Error fetching data from API: {e}")
        return None

def format_data(res):
    data = {}
    location = res['location']
    # Convert UUID to string before serialization
    data['id'] = str(uuid.uuid4())
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data

def stream_data():
    import json
    from kafka import KafkaProducer
    import time
    import logging

    try:
        producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
        logging.info("Successfully connected to Kafka")
    except Exception as e:
        logging.error(f"Failed to connect to Kafka: {e}")
        return

    curr_time = time.time()

    while True:
        if time.time() > curr_time + 60: #1 minute
            break
        try:
            res = get_data()
            if res is None:
                logging.warning("Skipping iteration due to empty API response")
                time.sleep(1)
                continue
                
            res = format_data(res)
            producer.send('users_created', json.dumps(res).encode('utf-8'))
            logging.info(f"Successfully sent data for {res['first_name']} {res['last_name']}")
            time.sleep(0.5)  # Add a small delay to avoid overwhelming the API
        except Exception as e:
            logging.error(f'An error occurred: {e}')
            time.sleep(1)
            continue

with DAG('user_automation',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    streaming_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data
    )
