from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.resourceExpense.models import ResourceExpense
from LERT.administrator.models import Administrator
from LERT.icaAdmin.models import ICAAdmin
from LERT.opmanager.models import OpManager

try:

    session = Session(connection.e)
    #admin1 = Administrator(name="admin1")
    #session.add(admin1)
    #session.commit() 

    connection.Base.metadata.create_all(connection.e)
    print(connection.Base.metadata.tables)

except Exception as e:
    print(e)

