import sys
sys.path.insert(0,'./lert_driver_db2/db2')
from db2_Connection import Db2Connection
from sqlalchemy import *

connection = Db2Connection()
def init_app():
    connection._create_connection_sqlAlchemy()
    connection._create_models()
