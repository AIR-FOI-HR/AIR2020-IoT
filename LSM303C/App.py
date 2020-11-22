from LSM303C.model.dto.LSM303Dto import LSM303Dto
from LSM303C.service import MqttClient
from time import sleep as delay
from threading import Thread
import json
from datetime import datetime as dt

class Main(Thread):
    validRange = 5

    def __init__(self, mqtt: MqttClient):
        Thread.__init__(self)


        self.mqtt = mqtt
        self.x = []
        self.y = []
        self.z = []
        self.time = []
        self.counter = []

        self.xArr = []
        self.yArr = []
        self.zArr = []

        self.offsetX = None
        self.offsetY = None
        self.offsetZ = None

        self.scaleX = None
        self.scaleY = None
        self.scaleZ = None

    def run(self):
        self.mqtt.start()
        print("MQTT initialized!")
        i = 1
        validPoints = 0
        calibrate = True
        calibrationDone = False

        while True:
            msg = self.mqtt.getFromQueue()
            if msg != None:
                topic, values = msg.split(";")
                timeNow = dt.now().strftime("%H:%M:%S %Y-%m-%d")
                # print("{} | Message received on topic {}".format(timeNow, topic))
                lsmDto = LSM303Dto().serialize(values, ignoreProperties=False)
                # print("{} {} {}".format(lsmDto.x, lsmDto.y, lsmDto.z))
                xRaw = int(lsmDto.x)
                yRaw = int(lsmDto.y)
                zRaw = int(lsmDto.z)

                if calibrate:
                    if len(self.xArr) == 0:
                        self.xArr.append(xRaw)
                        self.yArr.append(yRaw)
                        self.zArr.append(zRaw)
                        validPoints += 1
                    else:
                        xValid = True
                        yValid = True
                        zValid = True
                        for i in self.xArr:
                            if (abs(i - xRaw) < self.validRange):
                                xValid = False

                        for i in self.yArr:
                            if (abs(i - yRaw) < self.validRange):
                                yValid = False

                        for i in self.zArr:
                            if (abs(i - zRaw) < self.validRange):
                                zValid = False

                        if xValid and yValid and zValid:
                            self.xArr.append(xRaw)
                            self.yArr.append(yRaw)
                            self.zArr.append(zRaw)
                            validPoints += 1

                print("_______________________________________Valid points: {}".format(validPoints))
                if not calibrationDone:
                    if validPoints >= 50:
                        calibrate = False
                        calibrationDone = True
                        print("X: {} {}".format(max(self.xArr), min(self.xArr)))
                        print("y: {} {}".format(max(self.yArr), min(self.yArr)))
                        print("z: {} {}".format(max(self.zArr), min(self.zArr)))
                        self.offsetX = (max(self.xArr) - min(self.xArr)) / 2
                        self.offsetY = (max(self.yArr) - min(self.yArr)) / 2
                        self.offsetZ = (max(self.zArr) - min(self.zArr)) / 2

                        offsetAvg = (self.offsetX + self.offsetY + self.offsetZ) / 3

                        self.scaleX = offsetAvg / self.offsetX
                        self.scaleY = offsetAvg / self.offsetY
                        self.scaleZ = offsetAvg / self.offsetZ

                else:
                    calibratedX = (xRaw - self.offsetX)  # * self.scaleX
                    calibratedY = (yRaw - self.offsetY)  # * self.scaleY
                    calibratedZ = (zRaw - self.offsetZ)  # * self.scaleZ

                    print("{}, {}, {}".format(calibratedX, calibratedY, calibratedZ))

                self.x.append(lsmDto.x)
                self.y.append(lsmDto.y)
                self.z.append(lsmDto.z)
                self.counter.append(i)
                i += 1

            delay(0.1)


if __name__ == '__main__':
    mqtt = MqttClient.Mqtt(MqttClient._topic)
    main = Main(mqtt)
    main.start()