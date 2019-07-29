import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Smy Flask Web]'
    FLASKY_MAIL_SENDER = '*********@***.***'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_POSTS_PER_PAGE = 50

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
        # 'mysql+pymysql://root:123@localhost:3306/hzmc'
    SQLALCHEMY_BINDS = {
        'hzmc_data' : 'mysql+pymysql://root:hzmcmysql@mysql.db/hzmc_data',
        'hzmc' : 'mysql+pymysql://root:hzmcmysql@mysql.db/hzmc',
        'target_warning': 'mysql+pymysql://root:hzmcmysql@mysql.db/target_warning'
    }


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    # 'mysql+pymysql://root:123@localhost:3306/hzmc'
    SQLALCHEMY_BINDS = {
        'hzmc_data': 'mysql+pymysql://root:hzmcmysql@mysql.db:3306/hzmc_data',
        'hzmc': 'mysql+pymysql://root:hzmcmysql@mysql.db:3306/hzmc'
    }


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    # 'mysql+pymysql://root:123@localhost:3306/hzmc'
    SQLALCHEMY_BINDS = {
        'hzmc_data': 'mysql+pymysql://root:hzmcmysql@mysql.db:3306/hzmc_data',
        'hzmc': 'mysql+pymysql://root:hzmcmysql@mysql.db:3306/hzmc'
    }

class QuzhouConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql+pymysql://root:123@localhost:3306/hzmc'
    # 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_BINDS = {
        'hzmc_data' : 'mysql+pymysql://root:hzmcmysql@mysql.db:3306/hzmc_data',
        'hzmc': 'mysql+pymysql://root:hzmcmysql@mysql.db:3306/hzmc'
    }

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'quzhou' : QuzhouConfig,

    'default': DevelopmentConfig
}
