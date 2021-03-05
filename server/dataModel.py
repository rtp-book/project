from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def get_model(table_name: str) -> Base:
    models = Base.__subclasses__()
    return next((model for model in models if model.__name__ == table_name))


class Categories(Base):
    __tablename__ = __qualname__
    ID = Column(Integer, primary_key=True, nullable=False)
    Category = Column(String, unique=True)


class Publishers(Base):
    __tablename__ = __qualname__
    ID = Column(Integer, primary_key=True, nullable=False)
    Publisher = Column(String, unique=True)


class Conditions(Base):
    __tablename__ = __qualname__
    ID = Column(Integer, primary_key=True, nullable=False)
    Code = Column(String, unique=True)
    Condition = Column(String)


class Formats(Base):
    __tablename__ = __qualname__
    ID = Column(Integer, primary_key=True, nullable=False)
    Format = Column(String, unique=True)


class Users(Base):
    __tablename__ = __qualname__
    ID = Column(Integer, primary_key=True, nullable=False)
    Username = Column(String, unique=True)
    Password = Column(String)


class Books(Base):
    __tablename__ = __qualname__
    ID = Column(Integer, primary_key=True, nullable=False)
    Title = Column(String, nullable=False)
    Author = Column(String)
    Publisher = Column(String, ForeignKey('Publishers.Publisher',
                                          onupdate='CASCADE',
                                          ondelete='RESTRICT'))
    IsFiction = Column(Boolean, default=0)
    Category = Column(String, ForeignKey('Categories.Category',
                                         onupdate='CASCADE',
                                         ondelete='RESTRICT'))
    Edition = Column(String)
    DatePublished = Column(String)
    ISBN = Column(String)
    Pages = Column(Integer)
    DateAcquired = Column(Date)
    Condition = Column(String, ForeignKey('Conditions.Code',
                                          onupdate='CASCADE',
                                          ondelete='RESTRICT'))
    Format = Column(String, ForeignKey('Formats.Format',
                                       onupdate='CASCADE',
                                       ondelete='RESTRICT'))
    Location = Column(String)
    Notes = Column(String)
