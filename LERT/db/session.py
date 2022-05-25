from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.administrator.models import Administrator
from LERT.bandType.models import BandType
from LERT.expense.models import Expense
from LERT.expenseType.models import ExpenseType
from LERT.hourType.models import HourType
from LERT.ica.models import ICA
from LERT.icaAdmin.models import ICAAdmin
from LERT.manager.models import Manager
from LERT.opmanager.models import OpManager
from LERT.resource.models import Resource
from LERT.resourceExpense.models import ResourceExpense
from LERT.user.models import User

try:

    session = Session(connection.e)


    connection.Base.metadata.create_all(connection.e)
    print(connection.Base.metadata.tables)

except Exception as e:
    print(e)

