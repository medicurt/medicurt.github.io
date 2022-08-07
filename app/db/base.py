#This implements the base object that all crud inherets and uses. 
from sqlalchemy.orm import as_declarative

@as_declarative()
class Base(object):
    def validate(self):
        pass