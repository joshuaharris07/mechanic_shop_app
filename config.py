import os

class DevelopmentConfig:

    user = "CodingTemple"
    password = "C0dingT3mple!"
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{user}:{password}@localhost/mechanic_shop_db'
    DEBUG = True
    CACHE_TYPE = "SimpleCache"


class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    CACHE_TYPE = 'SimpleCache'