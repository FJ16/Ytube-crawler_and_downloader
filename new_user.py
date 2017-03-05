# import class Database from file database.py
from common.database import Database

Database.initialize()
Database.insert('users',{"account":"jason@test.com","name":"jason","password":"123456"})
