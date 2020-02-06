from models.base_model import BaseModel
import peewee as pw
import re
from models.floor import Floor


class Parking(BaseModel):
    floor = pw.ForeignKeyField(Floor, backref='parking', on_delete ="CASCADE", unique=False)
    parking_num = pw.CharField(unique=False)
    status = pw.BooleanField(default=False)

