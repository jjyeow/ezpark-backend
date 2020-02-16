import os
import peewee as pw
import datetime
from database import db
from dateutil.tz import tzlocal


class BaseModel(pw.Model):
    created_at = pw.DateTimeField(default=datetime.datetime.now(tzlocal()))
    updated_at = pw.DateTimeField(default=datetime.datetime.now(tzlocal()))

    def save(self, *args, **kwargs):
        self.errors = []
        self.validate()

        if len(self.errors) == 0:
            self.updated_at = datetime.datetime.now(tzlocal())
            return super(BaseModel, self).save(*args, **kwargs)
        else:
            return 0

    def validate(self):
        return True

    class Meta:
        database = db
        legacy_table_names = False
