from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re


class User(BaseModel):
    username = pw.CharField(unique=True)
    first_name = pw.CharField(unique=False, default="")
    last_name = pw.CharField(unique=False, default="")
    password = pw.CharField(unique=False)
    email = pw.CharField(unique=True)
    hp_number = pw.CharField(unique=True)

    def validate(self):
        if self.username == "": 
            self.errors.append('Username cannot be empty!')
    
        if self.hp_number == "": 
            self.errors.append('Mobile phone number cannot be empty!')

        duplicate_emails = User.get_or_none(User.email == self.email)
        if duplicate_emails:
            self.errors.append('Email has been used')

        duplicate_user = User.get_or_none(User.username == self.username)
        if duplicate_user: 
            self.errors.append('Username has been used')
        
        if re.search('[A-Za-z0-9._%+-]+@+[A-Za-z]+[.]+[c][o][m]', self.email) is None:
            self.errors.append('Invalid email')
        if len(self.password) < 6:
            self.errors.append('Password has to be at least 6 characters!')
        elif re.search('[0-9]', self.password) is None:
            self.errors.append('Password must have at least 1 number!')
        elif re.search('[A-Z]', self.password) is None:
            self.errors.append('Password must have at least 1 capital letter!')
        elif re.search("[$&+,_:;=?@#\"\\/|'<>.^*()%!-]", self.password) is None:
            self.errors.append('Password must have at least 1 special character!')

        self.password = generate_password_hash(self.password)

    def standard_hp(self):
        if re.search('[+-]', self.hp_number) is None: 
            return self.hp_number
        else:
            hp = self.hp_number
            hp = hp.replace("-", "")
            hp = hp.replace("+", "")
            if hp[0] == "6":
                hp = hp.replace("6", "", 1) 
                return hp   
            else: 
                hp   
