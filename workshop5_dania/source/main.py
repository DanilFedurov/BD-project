import datetime
from sqlalchemy import create_engine, ForeignKey, Sequence, CheckConstraint
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{host}:{port}/{sid}'

engine = create_engine(
    oracle_connection_string.format(

        username="SYSTEM",
        password="oracle",
        sid="XE",
        host="localhost",
        port="1521",
        database="PROJECT",

    )
    , echo=True
)


Base = declarative_base()


class user_database (Base):
    __tablename__ = 'user_database'

    id_user = Column(Integer, Sequence('id_seq1'), primary_key=True)
    user_name = Column(String(100), nullable=False)
    user_surname = Column(String(100), nullable=False)
    user_age = Column(Integer, CheckConstraint('user_age >= 18'), nullable=False)
    user_mail = Column(String(100), nullable=False, unique=True)	
    user_login = Column(String(100), nullable=False, unique=True)
    user_pass = Column(String(100), nullable=False)

    
    def __init__(self, user_name, user_surname, user_age, user_mail, user_login, user_pass):
        """"""
        self.user_name = user_name
        self.user_surname = user_surname
        self.user_age = user_age
        self.user_mail = user_mail
        self.user_login = user_login
        self.user_pass = user_pass


class prediction_database (Base):
    __tablename__ = 'prediction_database'

    id_pred = Column(Integer, Sequence('id_seq2'), primary_key=True)
    prediction_description = Column(String(500), unique=True, nullable=False)

    def __init__(self, prediction_description):
        """"""
        self.prediction_description = prediction_description


class numerology_database (Base):
    __tablename__ = 'numerology_database'

    id_nume = Column(Integer, Sequence('id_seq3'), primary_key=True)
    numerology_date =  Column(Date)
    numerology_description = Column(String(500), unique=True, nullable=False)

    def __init__(self, numerology_date, numerology_description):
        """"""
        self.numerology_date = numerology_date
        self.numerology_description = numerology_description



# create tables
Base.metadata.create_all(engine)