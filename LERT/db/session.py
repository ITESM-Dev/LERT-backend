from sqlalchemy.orm import Session
from LERT.db.database import connection
from LERT.endpoints.administrator.models import Administrator
from LERT.endpoints.bandType.models import BandType
from LERT.endpoints.expense.models import Expense
from LERT.endpoints.expenseType.models import ExpenseType
from LERT.endpoints.hourType.models import HourType
from LERT.endpoints.ica.models import ICA
from LERT.endpoints.icaAdmin.models import ICAAdmin
from LERT.endpoints.manager.models import Manager
from LERT.endpoints.opmanager.models import OpManager
from LERT.endpoints.resource.models import Resource
from LERT.endpoints.resourceExpense.models import ResourceExpense
from LERT.endpoints.user.models import User
from LERT.endpoints.currentPeriod.models import CurrentPeriod
try:

    session = Session(connection.e)


    connection.Base.metadata.create_all(connection.e)
    print(connection.Base.metadata.tables)

except Exception as e:
    print(e)

