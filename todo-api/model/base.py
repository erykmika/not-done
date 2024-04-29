from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create an engine
engine = create_engine(r"sqlite:///db.db")


# Create a session instance
Session = sessionmaker(bind=engine)
session = Session()

# Create a base class for mapped classes
Base = declarative_base()
