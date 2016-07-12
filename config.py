import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRRT_KEY') or 'vibiu_s_screat'

    @staticmethod
    def init_app(app):
        pass


class ProductConfig(Config):
    pass


class DevelopConfig(Config):
    DEBUG = True


config = {
    'product': ProductConfig,
    'develop': DevelopConfig,
    'default': DevelopConfig
}
