from .settings import Config

class DevelopmentConfig(Config):
    '开发模式下的配置'
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True