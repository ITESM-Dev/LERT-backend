import ibm_db_sa
import os
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

# Definition of ENV variables
DB_NAME = os.environ.get("DBNAME")        
DB_HOSTNAME = os.environ.get("DB_HOSTNAME")
DB_PASSWORD = os.environ.get("DB2INST1_PASSWORD")
SECURITY = os.environ.get("SECURITY")
UID = os.environ.get("UID")
CERTIFICATE = os.environ.get("CERTIFICATE")
DB_PORT = os.environ.get("DB_PORT")


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Db2Connection(object):
    def __init__(self): 
        try:
            if os.environ.get('ENVIRONMENT') == "dev":
                db_string = f"db2+ibm_db://{UID}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}"
            elif os.environ.get('ENVIRONMENT') == "prod":
                db_string = f"db2+ibm_db://{UID}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME};SECURITY=SSL;"

            engine_db = create_engine(db_string, pool_size=10, max_overflow=0)
            self.e = engine_db
            self.metadata = MetaData()
            self.Base = declarative_base(metadata=self.metadata)
            self.metadata.bind = self.e
            self._create_connection_sqlAlchemy()

            
        except Exception as e:
            print(e)
    def _create_connection_sqlAlchemy(self):
            Session = sessionmaker(self.e)
            self.session = Session()

    def _create_models(self):
        try:
            self.metadata.create_all()
        except Exception as e:
            print(e)

    def execute(self, sentence):
        self.cursor.execute(sentence)

    def get_all(self, sentence):
        try:
            self.cursor.execute(sentence)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
