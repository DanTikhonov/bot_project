from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker


days = {
    'mon' : 'Понедельник',
    'tue' : 'Вторник',
    'wed': 'Среда',
    'thu': 'Четверг',
    'fri': 'Пятница'
}


engine = create_engine('sqlite:///my.db')
Base = declarative_base()


class Lessons(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    day_id = Column(String)
    lesson = Column(String)
    home_work = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Dairy:
    def __init__(self):
        pass

    def