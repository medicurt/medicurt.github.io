from typing import List
from app.crud.base import CRUDBase
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate
from enum import Enum
from sqlalchemy.orm import Session


#Uses the methods from base.py Requires no extra behavior and can safely run off of the base crud
#the model is passed in first, followed by the create and update schemas
class cardinalityEnum(str, Enum):
    ASC = "ASCENDING"
    DESC = "DESCENDING"

class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    def get_by_sort(self, db: Session, *, cardinality: cardinalityEnum, skip: int = 0, limit: int = 0)-> List[Event]:
        if cardinality == cardinalityEnum.ASC:
            return db.query(self.model).offset(skip).limit(limit).order_by(self.model.sort_order.asc()).all()
        return db.query(self.model).offset(skip).limit(limit).order_by(self.model.sort_order.desc()).all()


crud_event = CRUDEvent(Event)