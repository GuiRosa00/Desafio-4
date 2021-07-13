#from app.sensive import Sensive as sen
class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///data-dev.db"
    SQL_ALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    
    #documentado integração com o sensive
    #SQLALCHEMY_DATABASE_URI =sen.SQLALCHEMY_DATABASE_URI
    #SQL_ALCHEMY_TRACK_MODIFICATIONS =sen.SQL_ALCHEMY_TRACK_MODIFICATIONS
    #JSON_SORT_KEYS =sen.JSON_SORT_KEYS
    #MAIL_SERVER =sen.MAIL_SERVER
    #MAIL_PORT =sen.MAIL_PORT
    #MAIL_USERNAME =sen.MAIL_USERNAME
    #MAIL_KEY =sen.MAIL_KEY
    #MAIl_USE_TLS =sen.MAIl_USE_TLS 
    #MAIL_USE_SSL =sen.MAIL_USE_SSL 
