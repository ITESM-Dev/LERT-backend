import ibm_db
import ibm_db_dbi
import os

#Environment variables
DB_NAME = os.environ.get("DB_NAME")
DB_HOSTNAME = os.environ.get("DB_HOSTNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
SECURITY = os.environ.get("SECURITY")
UID = os.environ.get("UID")
CERTIFICATE = os.environ.get("CERTIFICATE")

class Db2Connection(object):

    def __init__(self):
        self._create_conn()

    def _create_conn(self):
    
        conn_str = "database=${DB_NAME};hostname=${DB_HOSTNAME};port=32733;security=${SECURITY};SSLServerCertificate=${CERTIFICATE};uid=${UID};pwd=${DB_PASSWORD}"
      
        self.ibm_db_conn = ibm_db.connect(conn_str, '', '')
        conn = ibm_db_dbi.Connection(self.ibm_db_conn)
        self.cursor = conn.cursor()

    def execute(self, sentence):
        self.cursor.execute(sentence)

    def get_one(self, sentence):
        self.cursor.execute(sentence)
        return self.cursor.fetchone()

    def get_all(self, sentence):
        self.cursor.execute(sentence)
        return self.cursor.fetchall()

    def commit(self):
        pass

    def close_connection(self):
        self.cursor.close()
        ibm_db.close(self.ibm_db_conn)
