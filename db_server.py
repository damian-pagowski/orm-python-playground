import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_session():
    engine = create_engine('sqlite:///restaurantmenu.db')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session