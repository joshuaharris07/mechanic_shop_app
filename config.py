
class DevelopmentConfig:

    user = "CodingTemple"
    password = "C0dingT3mple!"
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{user}:{password}@localhost/mechanic_shop_db'
    DEBUG = True
    CACHE_TYPE = "SimpleCache"


class TestingConfig:
    pass

class ProductionConfig:
    pass