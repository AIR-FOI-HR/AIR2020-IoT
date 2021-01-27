import json


class BLEDeviceDto():

    def __init__(self, address, type, rssi, scannedData):
        self.address = address
        self.addrType = type
        self.rssi = rssi
        self.scannedData = scannedData


    def getJson(self):
        device = {
            'address': self.address,
            'type': self.addrType,
            'rssi': self.rssi,
            'scanned': self.scannedData
        }
        return device

