from app.crud.base import CRUDBase
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate


#Uses the methods from base.py

class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    pass

crud_event = CRUDEvent(Event)