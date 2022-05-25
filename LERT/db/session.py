from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.administrator.models import Administrator

try:

    session = Session(connection.e)
    #admin1 = Administrator(name="admin1")
    #session.add(admin1)
    #session.commit() 

    connection.Base.metadata.create_all(connection.e)
    print(connection.Base.metadata.sorted_tables)

except Exception as e:
    print(e)

