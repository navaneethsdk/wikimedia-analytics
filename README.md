# Wikimedia analytics

Analyze basic Wikimedia metrics using Kafka pub-sub and Streamlit. The repo is basic and was developed with learning in mind.

## Set up

1. Ensure you have a Kafka cluster running. Change the port number in `producer.py` and `consumer.py` according to the server configurations.
2. Run  the following to install the required packages:
```
pip install requirements.txt
```
3. Start the producer using the following command
```
python3 producer.py
```
4. Start the consumer by running the following command:
```
streamlit run consumer.py
```