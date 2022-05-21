import ibm_db
import ibm_db_dbi
import os
from sqlalchemy import *

# Definition of ENV variables
DB_NAME = os.environ.get("DBNAME")        
DB_HOSTNAME = os.environ.get("DB_HOSTNAME")
DB_PASSWORD = os.environ.get("DB2INST1_PASSWORD")
SECURITY = os.environ.get("SECURITY")
UID = os.environ.get("UID")
CERTIFICATE = os.environ.get("CERTIFICATE")

class Db2Connection(object):
    def __init__(self): 
        self.dbstring =  f"DATABASE={DB_NAME};HOSTNAME={DB_HOSTNAME};PROTOCOL=TCPIP;PORT=50000;UID={UID};PWD={DB_PASSWORD}"
        try:
            self.ibm_db_conn = ibm_db.connect(self.dbstring, '', '')
            self._validate_connection()
            conn = ibm_db_dbi.Connection(self.ibm_db_conn)
            self.cursor = conn.cursor()
        except Exception as e:
            print(e)

    def _create_connection_sqlAlchemy(self):
        try:
            e = create_engine(f"db2+ibm_db://{UID}:{DB_PASSWORD}@{DB_HOSTNAME}:50000/{DB_NAME}")
            self.metadata = MetaData()
            self.metadata.bind = e
            
        except Exception as e:
            print(e)
    def _create_models(self):
        self.metadata.create_all()
    def _validate_connection(self):
        print(f"State of connection is: {ibm_db.active(self.ibm_db_conn)}")

    def execute(self, sentence):
        self.cursor.execute(sentence)

    def get_one(self, sentence):
        self.cursor.execute(sentence)
        return self.cursor.fetchone()

    def get_all(self, sentence):
        try:
            self.cursor.execute(sentence)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def commit(self):
        pass

    def close_connection(self):
        self.cursor.close()
        ibm_db.close(self.ibm_db_conn)
