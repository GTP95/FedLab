FROM python:3.9.5-buster
RUN pip install paho-mqtt argparse
COPY server_subscriber.py server_subscriber.py
CMD python server_subscriber.py -s mqtt -p 1883

