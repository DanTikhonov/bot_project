from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


days = {
    'mon': 'Понедельник',
    'tue': 'Вторник',
    'wed': 'Среда',
    'thu': 'Четверг',
    'fri': 'Пятница'
}


engine = create_engine('sqlite:///my.db')
Base = declarative_base()


class Lessons(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    day_id = Column(String)
    lesson = Column(String)
    home_work = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)



class Dairy:
    def __init__(self):
        self.session = Session()

    def getLesHWasDict(self, id, day):
        rows = self.session.query(Lessons).filter(Lessons.user_id == id, Lessons.day_id == day).all()
        les = {r.lesson : r.home_work for r in rows}
        return les

    def getHomeWork(self, day):
        rows = self.session.query(Lessons).filter(Lessons.day_id == day).all()
        les = {}
        for r in rows:
            if r in les:
                les[r].append([r.lesson, r.home_work])
            else:
                les[r] = [r.lesson, r.home_work]
        return les

    def addRecord(self, id, day, lessons):
        for les in lessons:
            new_row = Lessons(user_id=id, day_id=day, lesson=les, home_work='')
            self.session.add(new_row)
            self.session.commit()

    def updateHW(self, id, day, lesson, hw):
        self.session.query(Lessons). \
            filter(Lessons.user_id == id, Lessons.day_id == day, Lessons.lesson == lesson). \
            update({'home_work': hw})
        self.session.commit()

    def clearAll(self):
        self.session.query(Lessons).delete()
        self.session.commit()