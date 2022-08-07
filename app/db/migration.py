#The migration file tells alembic which files to base its migration script on. If a model is not imported here,
#Alembic will miss it during migration and you won't be sure why your db calls aren't working. 


from app.db.base import Base

from app.models.event import Event
from app.models.user import User
from app.models.permissions import Permissions