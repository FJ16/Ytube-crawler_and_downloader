# package.file
from common.database import Database

class User(object):
    # __init__ is more like constructor for instantiation
    def __init__(self,name,account,password):
        self.name = name
        self.account = account
        self.password = password

    @staticmethod
    def is_login_valid(account, password):
        # extract user data, collection and query are the variables created in Database class
        user_data = Database.find_one(collection='users',query={"account":account})
        if user_data is None:
            return False
        # the ['password'] is the value which is extracted from database by using json mark 'password'
        if user_data['password'] != password:
            return False
        return True

    @staticmethod
    def register_user(name, account, password):
        result = Database.find_one(collection='users',query={"account":account})
        if result is not None:
            return False
        # instantiate a new User here
        User(name, account, password).save_to_db()
        return  True


    # input is giving a instantiation User
    # and call the inside function json(self) to covert the format
    def save_to_db(self):
        Database.insert(collection='users',data=self.json())

    # using a function to convert variables in user class to a jason file for giving data
    def json(self):
        # directly return json format file
        return {
            "name":self.name,
            "account":self.account,
            "password":self.password
        }

    def find_user_data(account):
        user_data = Database.find_one(collection='users',query={"account":account})
        return user_data