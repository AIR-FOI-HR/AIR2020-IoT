import requests
import ast 
import json
from azure.eventhub import TransportType
from azure.eventhub import EventHubConsumerClient
import sys
from azure.iot.hub import IoTHubRegistryManager

class RequestService():
    
    URL = "https://air-analyzer.herokuapp.com/sensor-data"
    
    def __init__(self, connectionString): 
        self.connectionString = connectionString
        
    def on_event_batch(self, partition_context, events):
        for event in events:
            print("Poruka pročitana s Azure-a, praticija: {}.".format(partition_context.partition_id))
            print("Primljeni podaci: ", event.body_as_str())
            print("Postavke (postavljene kroz uređaj): ", event.properties)
            print("Postavke (postavljene kroz IoT Hub): ", event.system_properties)
            res = event.body_as_json()
            x = requests.get('https://air-analyzer.herokuapp.com/sensors?Mark='+res['uuid'])
            senzor = json.loads(x.text)
            senzorID = senzor[0]['id']
            rezultati = {"Results" : event.body_as_json(),"sensor" : senzorID}
            r = requests.post(self.URL, json = rezultati)
        partition_context.update_checkpoint()
    
    def on_error(self, partition_context, error):
        if partition_context:
            print("An exception: {} occurred during receiving from Partition: {}.".format(
                partition_context.partition_id,
                error
            ))
        else:
            print("An exception: {} occurred during the load balance process.".format(error))


    def send(self):
        client = EventHubConsumerClient.from_connection_string(
            conn_str=self.connectionString,
            consumer_group="$default",
        )
        try:
            with client:
                client.receive_batch(
                    on_event_batch=self.on_event_batch,
                    on_error=self.on_error
                )
        except KeyboardInterrupt:
            print("Primanje je završilo.")

# EVENTHUB_COMPATIBLE_ENDPOINT = "sb://ihsuprodamres077dednamespace.servicebus.windows.net/"

# EVENTHUB_COMPATIBLE_PATH = "iothub-ehub-airanalyze-5994777-7219749c9e"

# IOTHUB_SAS_KEY = "0BQS4zA9243yu4I4xgrAR5kM7mA3TXLOX5GnHTVHN34="

# URL = "https://air-analyzer.herokuapp.com/sensor-data"

# CONNECTION_STR = f'Endpoint={EVENTHUB_COMPATIBLE_ENDPOINT}/;SharedAccessKeyName=service;SharedAccessKey={IOTHUB_SAS_KEY};EntityPath={EVENTHUB_COMPATIBLE_PATH}'

