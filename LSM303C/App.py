from LSM303C.model.dto.LSM303Dto import LSM303Dto
from LSM303C.service import MqttClient
from time import sleep as delay
from threading import Thread
import json
from datetime import datetime as dt

class Main(Thread):
    def __init__(self, mqtt: MqttClient):
        Thread.__init__(self)
        self.mqtt = mqtt

    def run(self):
        self.mqtt.start()
        print("MQTT initialized!")
        while True:
            msg = self.mqtt.getFromQueue()
            if msg != None:
                topic, values = msg.split(";")
                timeNow = dt.now().strftime("%H:%M:%S %Y-%m-%d")
                print("{} | Message received on topic {}".format(timeNow, topic))
                lsmDto = LSM303Dto().serialize(values, ignoreProperties=False)
                print("{} {} {}".format(lsmDto.x, lsmDto.y, lsmDto.z))
            delay(0.5)


if __name__ == '__main__':
    mqtt = MqttClient.Mqtt(MqttClient._topic)
    main = Main(mqtt)
    main.start()