from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func, String, Float
import application.conf as cfg

engine = create_engine(cfg.DB_URL, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Patient(Base):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    email = Column(Text)
    username = Column(String(255))
    mobile = Column(Text)
    claims = relationship('Claim', backref='patient')


class Claim(Base):
    __tablename__ = 'claim'
    id = Column(Integer, primary_key=True)
    reason = Column(Text)
    submission_date = Column(DateTime)
    total_value = Column(Float)
    file_name = Column(Text)
    patient_id = Column(Integer, ForeignKey('patient.id'))
