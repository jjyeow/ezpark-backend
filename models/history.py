from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re
from models.user import User
from models.parking import Parking


class History(BaseModel):
    user = pw.ForeignKeyField(User, backref = "history", on_delete="CASCADE", unique=False)
    parking = pw.ForeignKeyField(Parking, backref="history", on_delete="CASCADE", unique=False)

    def info(self):
        from models.user import User
        from models.mall import Mall
        from models.floor import Floor
        from models.parking import Parking
        
        user = self.user
        parking = self.parking
        floor = Floor.get_or_none(Floor.id == self.parking.floor_id)
        mall = Mall.get_or_none(Mall.id == floor.mall_id)
        timestamp = self.created_at
        result = {
            "user": user,
            "parking": parking,
            "floor": floor,
            "mall": mall,
            "timestamp": timestamp,
        }

        return result


    # def parking_location(self):
    #     from models.floor import Floor
    #     from models.mall import Mall
    #     floor = Floor.get_or_none(Floor.id == self.parking.floor_id)
    #     mall = Mall.get_or_none(Mall.id == floor.mall_id)
    #     location = {
    #         "mall": mall,
    #         "floor": floor
    #     }
    #     return location

    # def time(self):
    #     return self.created_at

    # def parking(self):
    #     return self.parking.parking_num

