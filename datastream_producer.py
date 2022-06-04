from kafka import KafkaProducer
from json import dumps
from time import sleep
import fastf1 as ff1
import pandas as pd
ff1.Cache.enable_cache('fastf1_cache')
###
from datetime import datetime

from configparser import ConfigParser
config = ConfigParser()

def getKafkaInfo(config_path):
    kafka_broker = config.get('CONFIG', 'kafka_broker')
    kafka_topic = config.get('CONFIG', 'kafka_topic')
    return kafka_broker, kafka_topic

def producerEvent(producer, topic, data):
    producer.send(topic, value=data)
    producer.flush()

def getRaceTelemetry(year: int, grandprix: str, driver: str):
    
    #Loading session data about the selected race
    session = ff1.get_session(year, grandprix, 'Race')
    session.load(laps=True, telemetry=True, messages=False, livedata=None)

    # Getting telemetry on-board data of the selected driver
    driver_laps = session.laps.pick_driver(driver)
    
    # Attach the Lap Column
    telemetry = pd.DataFrame()
    current_lap = 0

    for _, lap in driver_laps.iterlaps():
        
        current_telemetry = lap.get_car_data()
        # Filling missing data with interpolation methods
        current_telemetry.fill_missing()

        # Additional rows we need for computation
        current_telemetry["X"] = lap.telemetry["X"]
        current_telemetry["Y"] = lap.telemetry["Y"]
        current_telemetry["LapIdx"] = current_lap

        telemetry = pd.concat([telemetry, current_telemetry])
        
        current_lap += 1

    # Dropping useless columns
    telemetry.drop("SessionTime", inplace=True, axis=1)
    telemetry.drop("Date", inplace=True, axis=1)
    telemetry.drop("Brake", inplace=True, axis=1)
    telemetry.drop("DRS", inplace=True, axis=1)
    telemetry.drop("Source", inplace=True, axis=1)
    
    telemetry["Time"] = telemetry['Time'].dt.seconds.astype('float64')/60

    return telemetry

def getData(telemetry, start_idx, n_rows):
    # This function returns a list of dict of size n_rows
    # Hence, if we have a dataframe like this:
    #   A, B
    # 1 a, b
    # 2 c, d
    # .. ...
    # The method to_dict applied on the first two rows returns this:
    # [{"A":"a", "B":"b"}, {"A":"c", "B":"d"}]
    return telemetry[start_idx:start_idx+n_rows].to_dict('records')

if __name__ == "__main__":
    config_path = 'configuration.ini'
    config.read(config_path)

    broker_ip, topic_name = getKafkaInfo(config_path)

    n_rows = 1

    telemetry = getRaceTelemetry(2020, "Monza", "LEC")

    print("Connecting to... ", broker_ip, "\n")
    print("At this topic: ", topic_name, "\n")

    # Creating the Kafka producer that allow us to connect to the Kafka broker server
    producer = KafkaProducer(bootstrap_servers=[broker_ip], 
                            value_serializer=lambda x: dumps(x).encode('utf-8'))

    for i in range(1, telemetry.shape[0], n_rows):
        data = getData(telemetry, i, n_rows)

        # Spark streaming doesn't work with list of dicts, but only with dicts.
        # So we send each dict separately
        for d in data:
            producerEvent(producer, topic=topic_name, data=d)
            print(d)

        sleep(0.240)
