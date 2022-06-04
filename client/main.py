from distutils.util import get_platform 
import pandas as pd
import streamlit as st
import altair as alt
import time
from configparser import ConfigParser
from plotUtils import *
from kafka_consumer import * 

st.set_page_config(page_title="ANOMALYX", page_icon="img/favicon.png",layout='wide')

config = ConfigParser()
config_path = 'configuration.ini'
config.read(config_path)
broker_ip = config.get('CONFIG', 'kafka_broker')
rawDataTopic = config.get('CONFIG', 'kafka_topic_raw')
sparkDataTopic = config.get('CONFIG', 'kafka_topic_analyzed')

# KAFKA DATA CONSUMER
kafkaDataConsumer = KafkaConsumer(
  bootstrap_servers=broker_ip,
  #group_id='StreamlitDataConsumer',
  auto_offset_reset='latest',
  enable_auto_commit=True,
  value_deserializer=lambda msg: json.loads(msg.decode('utf-8'))
)

kafkaDataConsumer.subscribe([rawDataTopic, sparkDataTopic])
########################

# USEFUL VARIABLES
n_speed = 0
n_rpm = 0
mean_speed = 0.0
max_speed = 0
mean_rpm = 0.0
curr_lap = 0

# It is the dictionary where we store
# the anomaly scores as values and lap idx as keys
lap_anomalyscores_dict = {}

# Refresh time for plots update
refresh_time = 10 #seconds
reference_time = time.time()
##################

# Define the schema of the incoming dict
df_dict = {'RowIdx': [], 'RPM': [], 'Speed': [], 'nGear': [], 'Throttle': [], 'Time': [], 'X': [], 'Y': [], 'LapIdx': []}
curr_idx = 0

# Uncomment if deploying app - this is needed to remove the hamburger menu on top-right corner
#hide_menu_style = """<style> #MainMenu {visibility: hidden;}</style>"""
#st.markdown(hide_menu_style, unsafe_allow_html=True)

# css code to hide the full screen icon appearing on top-right corner of site elements
hide_img_full_screen = '''<style> button[title="View fullscreen"]{ visibility: hidden;}</style>'''
st.markdown(hide_img_full_screen, unsafe_allow_html=True)

# Define the website containers
header = st.container()
graphics = st.container()

# HEADER CONTENT
with header:
  st.image("img/logo_large.png", width=800)
  st.caption("An anomaly detection and visualization tool for F1 on-board telemetry data \
             - \nCapone Vincenzo, Lombardi Andrea, Panariello Ciro, Silvio Vincenzo")
#------------------------------------------#

# SIDEBAR CONTENT
with st.sidebar:

  # This column trick is done to fix the image in the center of the sidebar
  col1,col2 = st.columns((1,2))
  with col2:
    col2.markdown('<p style="font-family:Bahnschrift; font-weight: bold;  \
              color:#dd0000; font-size: 28px;">PARAMETER SELECTION</p>', unsafe_allow_html=True)
  with col1:
    col1.image("img/logo_small_icon_only_inverted.png", width=80)
  # -----

  st.text(" Select the anomaly threshold and the racer to analyze\n its on-board telemetry data")

  # Variables in which race parameters are stored.
  # A race is defined by year, gran prix name and driver name.
  anomaly_threshold = st.slider("Select the anomaly tolerance", min_value=100, max_value=500, 
                                step=20, value=300)
  driver = st.selectbox("Select the  Driver", options=["LEC", "VET"]) 
#------------------------------------------#

# GRAPHICS CONTENT
with graphics:

  speed_col, rpm_col, stats_col= st.columns((2,2,1))

  # Columns with the Speed and RPM charts
  with speed_col:
    st.subheader("Speed graphic")
    speed_chart = st.line_chart()

  with rpm_col:
    st.subheader("RPM graphic")
    rpm_chart = st.area_chart()

  # Statistics column
  with stats_col:
    st.subheader("Statistics")

    current_lap_metric = st.empty()

    mean_speed_metric = st.empty()

    max_speed_metric = st.empty()

    mean_rpm_metric = st.empty()
    
    most_frequent_gear_metric = st.empty()

    less_frequent_gear_metric = st.empty()

  plots_col, anomaly_stats_col = st.columns((3,1))

  with plots_col:
    st.subheader("Anomaly Score for each lap")
    anomaly_chart = st.empty()

    # Show the lap heatmap on the circuit (referring to the speed and the gears)
    #st.subheader("Speed heatmap on circuit")
    speedHeatmap_graph = st.empty()
    #st.subheader("Gears heatmap on circuit")
    gearsHeatmap_graph = st.empty()
    
  with anomaly_stats_col:
    st.markdown("#")
    st.subheader("Detected Anomalies")

    anomalies_table = st.empty()
#------------------------------------------#

# DATA STREAM AND VISUALIZATION
while True :

  data = kafkaDataConsumer.poll(timeout_ms=240)
  #print(data)

  if data is None:
    continue
    
  current_time = time.time()

  for key, value in data.items():
    #print(key.topic)
    if key.topic == rawDataTopic:
      #print("RAW DATA ")

      for record in value:
        temp_dict = record.value

        # Add the elements of the dict to our dict
        df_dict["RowIdx"].append(curr_idx+1)
        df_dict["RPM"].append(temp_dict["RPM"])
        df_dict["Speed"].append(temp_dict["Speed"])
        df_dict["nGear"].append(temp_dict["nGear"])
        df_dict["Throttle"].append(temp_dict["Throttle"])
        df_dict["Time"].append(temp_dict["Time"])
        df_dict["X"].append(temp_dict["X"])
        df_dict["Y"].append(temp_dict["Y"])
        df_dict["LapIdx"].append(temp_dict["LapIdx"])

        if temp_dict["LapIdx"]>curr_lap:
          curr_lap += 1

        curr_idx += 1
        # UPDATE METRICS
        with current_lap_metric:
          st.metric("Current lap", str(curr_lap), delta=None)

        with mean_speed_metric:
          mean_speed = (temp_dict["Speed"] + mean_speed * n_speed) / (n_speed + 1)
          n_speed += 1
          st.metric("Mean speed", str(round(mean_speed, 2)) + " km/h", delta=None)

        with max_speed_metric:
          if max_speed < temp_dict["Speed"]:
            max_speed = temp_dict["Speed"]
          
          st.metric("Max speed reached", str(round(max_speed, 2)) + " km/h", \
                    delta=str(round(max_speed-mean_speed, 2))  + " km/h")

        with mean_rpm_metric:
          mean_rpm = (temp_dict["RPM"] + mean_rpm * n_rpm) / (n_rpm + 1)
          n_rpm += 1

          st.metric("Mean RPM", str(round(mean_rpm)) + " r/min", delta=None)
        
        ##########################################

        # UPDATE PLOTS
        speed_chart.add_rows([[temp_dict["Speed"]]])
        rpm_chart.add_rows([[temp_dict["RPM"]]])

        # The data is received every 0.240 milliseconds, but the graphics computing time is higher
        # So they are computed every interval_time seconds
        #if current_time - reference_time > refresh_time:

          #with speedHeatmap_graph:
            #fig = plotLapSpeedHeatmap(df_dict)
            #st.pyplot(fig)

          #with gearsHeatmap_graph:
            #fig2 = plotLapGearsHeatmap(df_dict)
            #st.pyplot(fig2)  
        # -----------------------------------------------#

    elif key.topic == sparkDataTopic:
      
      # Store each record in a dict {'LapIdx':''AnomalyScoreValue'}
      # {'0':150.34, '1':76.12, '2':88.5 ....}
      for record in value:
        lap_anomalyscores_dict[record.value["LapIdx"]] = record.value["AnomalyScore"]
      
      if current_time - reference_time > 5:
        
        with anomaly_chart:
          fig3 = plotAnomnalyScores(lap_anomalyscores_dict, anomaly_threshold)
          st.pyplot(fig3)

        # Show a table where the row is the number of a Lap with the corresponding anomaly score
        # If the score is higher than the threshold, it becames red.
        with anomalies_table:
          as_df = pd.DataFrame(data = lap_anomalyscores_dict.values(), 
                              index = lap_anomalyscores_dict.keys(), 
                              columns=["Anomaly Score"])

          as_df = as_df.style.applymap(lambda v: 'color:red;' if (v > anomaly_threshold) else None)
          st.dataframe(as_df) 

      # -----------------------------------------------#
  
  if current_time - reference_time > refresh_time:
    reference_time = current_time