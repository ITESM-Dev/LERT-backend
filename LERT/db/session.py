from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.administrator.models import Administrator

try:
    session = Session(connection.e)
    admin1 = Administrator(name="admin1")
    session.add(admin1)
    session.commit() 

except Exception as e:
    print(e)

    connection.Base.metadata.create_all(connection.e)

