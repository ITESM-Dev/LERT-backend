import ibm_db
import os
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# Definition of ENV variables
DB_NAME = os.environ.get("DB_NAME")
DB_HOSTNAME = os.environ.get("DB_HOSTNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
UID = os.environ.get("UID")
DB_PORT = os.environ.get("DB_PORT")

class Db2Connection(object):        

    def _create_connection_sqlAlchemy(self):
        try:
            if os.environ.get('ENVIRONMENT') == "dev":
                db_string = f"db2+ibm_db://{UID}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}"
            elif os.environ.get('ENVIRONMENT') == "prod":
                db_string = f"db2+ibm_db://{UID}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME};SECURITY=SSL"
            self.e = create_engine(db_string)
            self.e.connect()
            self.metadata = MetaData()
            self.Base = declarative_base(metadata=self.metadata)
            self.metadata.bind = self.e
            Session = sessionmaker(self.e)
            self.session = Session()
            
        except Exception as e:
            print(e)

    def _create_models(self):
        try:
            self.metadata.create_all()
        except Exception as e:
            print(e)

    def _validate_connection(self):
        print(f"State of connection is: {ibm_db.active(self.ibm_db_conn)}")
