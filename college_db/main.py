from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, select
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Fakultet(Base):
    __tablename__ = "fakultety"
    id = Column(Integer, primary_key=True)
    nazvanie = Column(String(100), nullable=False)
    gruppy = relationship("Gruppa", back_populates="fakultet")


class Gruppa(Base):
    __tablename__ = "gruppy"
    id = Column(Integer, primary_key=True)
    nazvanie = Column(String(50), nullable=False)
    fakultet_id = Column(Integer, ForeignKey("fakultety.id"))
    fakultet = relationship("Fakultet", back_populates="gruppy")
    studenty = relationship("Student", back_populates="gruppa")


class Prepodavatel(Base):
    __tablename__ = "prepodavateli"
    id = Column(Integer, primary_key=True)
    fio = Column(String(120), nullable=False)
    predmety = relationship("Predmet", back_populates="prepodavatel")


class Predmet(Base):
    __tablename__ = "predmety"
    id = Column(Integer, primary_key=True)
    nazvanie = Column(String(100), nullable=False)
    prepodavatel_id = Column(Integer, ForeignKey("prepodavateli.id"))
    prepodavatel = relationship("Prepodavatel", back_populates="predmety")
    ocenki = relationship("Ocenka", back_populates="predmet")


class Student(Base):
    __tablename__ = "studenty"
    id = Column(Integer, primary_key=True)
    fio = Column(String(120), nullable=False)
    gruppa_id = Column(Integer, ForeignKey("gruppy.id"))
    gruppa = relationship("Gruppa", back_populates="studenty")
    ocenki = relationship("Ocenka", back_populates="student")


class Ocenka(Base):
    __tablename__ = "ocenki"
    id = Column(Integer, primary_key=True)
    ball = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey("studenty.id"))
    predmet_id = Column(Integer, ForeignKey("predmety.id"))
    student = relationship("Student", back_populates="ocenki")
    predmet = relationship("Predmet", back_populates="ocenki")


def zapolnit(session):
    it = Fakultet(nazvanie="Информационные технологии")
    buh = Fakultet(nazvanie="Экономика")
    session.add_all([it, buh])
    session.commit()

    g1 = Gruppa(nazvanie="ИТ-21", fakultet_id=it.id)
    g2 = Gruppa(nazvanie="ЭК-22", fakultet_id=buh.id)
    session.add_all([g1, g2])
    session.commit()

    p1 = Prepodavatel(fio="Смирнов Алексей Петрович")
    p2 = Prepodavatel(fio="Кузнецова Ольга Ивановна")
    session.add_all([p1, p2])
    session.commit()

    pr1 = Predmet(nazvanie="Базы данных", prepodavatel_id=p1.id)
    pr2 = Predmet(nazvanie="Бухучет", prepodavatel_id=p2.id)
    pr3 = Predmet(nazvanie="Программирование", prepodavatel_id=p1.id)
    session.add_all([pr1, pr2, pr3])
    session.commit()

    s1 = Student(fio="Мамедова Мадина Айдынгызы", gruppa_id=g1.id)
    s2 = Student(fio="Иванов Иван Сергеевич", gruppa_id=g1.id)
    s3 = Student(fio="Петрова Анна Дмитриевна", gruppa_id=g2.id)
    session.add_all([s1, s2, s3])
    session.commit()

    session.add_all(
        [
            Ocenka(ball=5, student_id=s1.id, predmet_id=pr1.id),
            Ocenka(ball=4, student_id=s1.id, predmet_id=pr3.id),
            Ocenka(ball=3, student_id=s2.id, predmet_id=pr3.id),
            Ocenka(ball=5, student_id=s3.id, predmet_id=pr2.id),
        ]
    )
    session.commit()


def pokazat(session):
    print("Студенты и группы:")
    rows = session.execute(
        select(Student.fio, Gruppa.nazvanie, Fakultet.nazvanie)
        .join(Gruppa, Student.gruppa_id == Gruppa.id)
        .join(Fakultet, Gruppa.fakultet_id == Fakultet.id)
    )
    for fio, gruppa, fak in rows:
        print(fio, "-", gruppa, "-", fak)

    print()
    print("Оценки:")
    rows2 = session.execute(
        select(Student.fio, Predmet.nazvanie, Ocenka.ball)
        .join(Ocenka, Ocenka.student_id == Student.id)
        .join(Predmet, Ocenka.predmet_id == Predmet.id)
    )
    for fio, pred, ball in rows2:
        print(fio, pred, ball)


def main():
    engine = create_engine("sqlite:///college.db", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    count = session.execute(select(Fakultet)).scalars().first()
    if not count:
        zapolnit(session)

    pokazat(session)
    session.close()


if __name__ == "__main__":
    main()
