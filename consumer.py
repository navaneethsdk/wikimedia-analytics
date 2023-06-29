from kafka import KafkaConsumer
import json
import streamlit as st
import pandas as pd 
import plotly.express as px

# Kafka topic to produce to
TOPIC = "wikimedia-events"

# Kafka cluster address
BOOTSTRAP_SERVERS = "localhost:9092"

# Create Kafka consumer
consumer = KafkaConsumer(
  TOPIC,
	bootstrap_servers=BOOTSTRAP_SERVERS,
	value_deserializer=lambda x: json.loads(x.decode("utf-8"))    
)

# Dataframe to store event data
data = pd.DataFrame(columns=["timestamp", "title", "server_name", "bot", "type"])

# Create streamlit app title
st.title("Wikimedia Even Dashboard")

st.header("Wikimedia bot updates")
bot_bar_chart_spot = st.empty()

st.header("Wikimedia update types")
type_bar_chart_spot = st.empty()


index = 0

for message in consumer:
  try:
    event = message.value
    data.loc[index] = event
    
    index += 1

    bot_bar_chart = px.bar(data, x="bot", title="Bot updates vs Manual updates")
    type_bar_chart = px.bar(data, x='type', title='What type of change is happening?')
    with bot_bar_chart_spot:
      st.plotly_chart(bot_bar_chart, use_container_width=True)

    with type_bar_chart_spot:
      st.plotly_chart(type_bar_chart)

  except Exception as error:
    print(f"Error processing message: {error}")