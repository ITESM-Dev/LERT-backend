import ibm_db
import ibm_db_dbi
import os

class Db2Connection(object):

    def __init__(self):
        self._create_conn()

    def _create_conn(self):
        #dev
        conn_str = "DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qrx40494;PWD=9G6ADgrWP4X5EwXu"
        #test
        #conn_str = "database=BLUDB;hostname=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;port=32459;security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;uid=dcm74122;pwd=wATi7CIGfHjcVyrh"
        #conn_str = os.environ.get('DB_CONNECTION')
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

connection = Db2Connection()
sentence = "SELECT * FROM PRUEBA"
print(connection.get_all(sentence))
connection.close_connection()
