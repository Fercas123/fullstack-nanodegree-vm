from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from database_setup import Base, Shelter, Puppy
import datatime

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def query_one():
    """return all the puppies in asc alphabetical order"""
    pups = session.query(Puppy.name).order_by(Puppy.name.asc()).all()
    for item in pups:
        print item[0]

def query_two():
    """all the youngers than 6 months by younguest first"""
    today = datetime.date.today()
    if passesLeapDay(today):
        sixMonthsAgo = today - datetime.timedelta(days = 183)
    else:
        sixMonthsAgo = today - datetime.timedelta(days = 182)
    result = session.query(Puppy.name, Puppy.dateOfBirth)\
        .filter(Puppy.dateOfBirth >= sixMonthsAgo)\
        .order_by(Puppy.dateOfBirth.desc())

def query_three():
    """all by ascending weight"""
    byweight = session.query(Puppy.name, Puppy.weight).order_by(Puppy.weight.asc()).all()

    for item in byweight:
        print item[0], item[1]

def query_four():
    """all puppies by shelter"""
    byshelter = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()

    for item in byshelter:
        print item[0].name, item[1]


# Helper Methods
def passesLeapDay(today):
    """
    Returns true if most recent February 29th occured after or exactly 183 days ago (366 / 2)
    """
    thisYear = today.timetuple()[0]
    if isLeapYear(thisYear):
        sixMonthsAgo = today - datetime.timedelta(days = 183)
        leapDay = datetime.date(thisYear, 2, 29)
        return leapDay >= sixMonthsAgo
    else:
        return False

def isLeapYear(thisYear):
    """
    Returns true iff the current year is a leap year.
    Implemented according to logic at https://en.wikipedia.org/wiki/Leap_year#Algorithm
    """
    if thisYear % 4 != 0:
        return False
    elif thisYear % 100 != 0:
        return True
    elif thisYear % 400 != 0:
        return False
    else:
        return True