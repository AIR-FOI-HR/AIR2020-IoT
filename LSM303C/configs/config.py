import pathlib

class Config(object):
    pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///calibration.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
