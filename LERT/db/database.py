import sys
sys.path.insert(0,'./lert_driver_db2/db2')
from db2_Connection import Db2Connection
from sqlalchemy import *

connection = Db2Connection()
connection._create_connection_sqlAlchemy()

try:
    hello = Table('STAF118', connection.metadata, 
                Column('ID', Integer, primary_key = True),
                Column('NAME', String(9), nullable = False),
                Column('DEPT', Integer, nullable = False),
                Column('JOB', String(5), nullable = False)
        )
    
except Exception as e:
    print(e)


try:
    stmt = (
        insert(hello).
        values(id=1 ,name='username', dept= 12, job = 'Full')
    )
    connection.Session.commit()

except Exception as e:
    print(e)

print(connection.get_all("SELECT * FROM STAF118"))
connection._create_models()

