from main import app, db
from app.LSMmain import Main
from service import MqttClient
from service.InitializeService import InitializeService


def initialize():
    print("initializing")
    InitializeService.initialize()
    mqtt = MqttClient.Mqtt(MqttClient._topic)
    main = Main(mqtt)
    main.start()



if __name__ == '__main__':
    initialize()
    app.run(debug=True, host='0.0.0.0', port=8080)