

import random
import time
from datetime import datetime
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=AirAnalyzerSensors.azure-devices.net;DeviceId=BME680M;SharedAccessKey=b0qBtEZzpgF7tiV7jaWqVRO3slgLeZxW4v7OfFSMp+o="

UUID = "ee592f35-e5aa-43b6-b335-da60b94ae915"
temp = 22.0
humid = 80
press = 1010

MSG_TXT = '{{"uuid": "{uuid}", "temp": {temp},"humid": {humid}, "press": {press}}}'

def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            uuid = str(UUID)
            x = temp + (random.random() * 15)
            y = humid + (random.random() * 20)
            z = press + (random.random() * 10)
            sendtime = datetime.now()
            msg_txt_formatted = MSG_TXT.format(uuid=uuid, temp=x, humid=y, press=z)
            message = Message(msg_txt_formatted)
            print( "Sending message: {}".format(message) )
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(10)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()