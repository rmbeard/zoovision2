# db_creator.py

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('postgresql://postgres:Circe2635!@localhost/zoovision', echo=True)
Base = declarative_base()


class HumanData(Base):
    __tablename__ = "human_data"

    id = Column(Integer, primary_key=True)
    states = Column(String(20), nullable=False)
    season_description = Column(String(20), nullable=False)
    flu_pdm = Column(String(20), nullable=False)

    def __repr__(self):
        return "{}".format(self.states)


# create tables
Base.metadata.create_all(engine)
