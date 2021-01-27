import json
import requests
from azure.eventhub import EventHubConsumerClient
from threading import Thread


class ClientJob(Thread):
    URL = "https://air-analyzer.herokuapp.com/sensor-data"

    def __init__(self, client, name):
        Thread.__init__(self)
        self.client = client
        self.name = name

    def on_event_batch(self, partition_context, events):
        for event in events:
            print("Device name: {}".format(self.name))
            print("Received event from partition: {}.".format(partition_context.partition_id))
            print("Telemetry received: ", event.body_as_str())
            print("Properties (set by device): ", event.properties)
            print("System properties (set by IoT Hub): ", event.system_properties)
            res = event.body_as_json()
            x = requests.get('https://air-analyzer.herokuapp.com/sensors?Mark=' + res['uuid'])
            senzor = json.loads(x.text)
            senzorID = senzor[0]['id']
            rezultati = {"Results": event.body_as_json(), "sensor": senzorID}
            r = requests.post(self.URL, json=rezultati)
        partition_context.update_checkpoint()

    def on_error(self, partition_context, error):
        if partition_context:
            print("An exception: {} occurred during receiving from Partition: {}.".format(
                partition_context.partition_id,
                error
            ))
        else:
            print("An exception: {} occurred during the load balance process.".format(error))

    def run(self):
        print("Starting client [{}]".format(self.name))
        with self.client:
            self.client.receive_batch(
                on_event_batch=self.on_event_batch,
                on_error=self.on_error
            )


class AzureGetData:
    EVENTHUB_COMPATIBLE_ENDPOINT_LSM = "sb://ihsuprodamres077dednamespace.servicebus.windows.net/"
    EVENTHUB_COMPATIBLE_PATH_LSM = "iothub-ehub-airanalyze-5994777-7219749c9e"
    IOTHUB_SAS_KEY_LSM = "0BQS4zA9243yu4I4xgrAR5kM7mA3TXLOX5GnHTVHN34="
    CONNECTION_STR_LSM = f'Endpoint={EVENTHUB_COMPATIBLE_ENDPOINT_LSM}/;SharedAccessKeyName=service;SharedAccessKey={IOTHUB_SAS_KEY_LSM};EntityPath={EVENTHUB_COMPATIBLE_PATH_LSM}'
    
    CONNECTION_STRINGS = [CONNECTION_STR_LSM, "LSM"]

    def __init__(self):
        self.createClients()

    def createClients(self):
        try:
            client = EventHubConsumerClient.from_connection_string(
                conn_str=self.CONNECTION_STR_LSM,
                consumer_group="$default",
            )
            clientJob = ClientJob(client, "LSM")
            clientJob.start()

        except KeyboardInterrupt:
            print("Primanje je završilo.")

if __name__ == '__main__':
    azure = AzureGetData()
