from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

# Create an engine
engine = create_engine(r"sqlite:///db.db")


# Create a session instance
Session = sessionmaker(bind=engine)
session = Session()


# Create a base class for mapped classes
class Base(DeclarativeBase):
    pass
