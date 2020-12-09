from app.LSMmain import Main
from main import app
from service.InitializeService import InitializeService


def initialize():
    print("initializing")
    InitializeService.initialize()
    main = Main()
    main.start()



if __name__ == '__main__':
    initialize()
    app.run(host='0.0.0.0', port=8080)