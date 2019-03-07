import conf
from dbtools import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Float, DateTime
)

SQLBase = declarative_base()


class Instrument(SQLBase):
    __tablename__ = 'instruments'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), index=True, nullable=False)


class Parameter(SQLBase):
    __tablename__ = 'parameters'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))


class Datum(SQLBase):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    parameter_id = Column(Integer, ForeignKey('parameters.id'))
    value = Column(Float)
    date = Column(DateTime)


class DataStatus(SQLBase):
    __tablename__ = 'datastatus'

    id = Column(Integer, primary_key=True)
    datum_id = Column(Integer, ForeignKey('data.id'))


class CsvDB(Session):
    def __init__(self, url=conf.CSV_DB, engine_args=[],
                 engine_kwargs={}, **kwargs):

        Session.__init__(
            self, url=url, metadata=SQLBase.metadata,
            engine_args=engine_args, engine_kwargs=engine_kwargs, **kwargs
        )
