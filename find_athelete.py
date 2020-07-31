import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class Athelete(Base):
    __tablename__ = 'athelete'

    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    weight = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.String(36), primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    #сложо было осознать, что здесь происходит
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def request_data():

    print("Поиск атлетов.")
    user_id = input("Введите id (индентификатор) пользователя: ")
    return int(user_id)


def convert_date(date_conv):

    parts = date_conv.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date

def near_id(user, session):

    atheletes_list = session.query(Athelete).all()
    athelete_id_bd = {}
    for athelete in atheletes_list:
        bd = convert_date(athelete.birthdate)
        athelete_id_bd[athelete.id] = bd

    user_bd = convert_date(user.birthdate)
    min_dist = None
    athelete_id = None
    athelete_bd = None

    for id_a, bd in athelete_id_bd.items():
        dist = abs(user_bd - bd)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athelete_id = id_a
            athelete_bd = bd

    return athelete_id, athelete_bd


def near_height(user, session):

    atheletes_list = session.query(Athelete).filter(Athelete.height != None).all()
    athelete_id_height = {athelete.id: athelete.height for athelete in atheletes_list}

    user_height = user.height
    min_dist = None
    athelete_id = None
    athelete_height = None

    for id_a, height in athelete_id_height.items():
        if height is None:
            continue

        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athelete_id = id_a
            athelete_height = height

    return athelete_id, athelete_height

def main():

    session = connect_db()
    user_id = request_data()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        print("Пользователь не найден.")
    else:
        bd_athelete, bd = near_id(user, session)
        height_athelete, height = near_height(user, session)
        print(
            "Атлет с ближайшей датой рождения: {}, дата рождения этого атлета: {}".format(bd_athelete, bd)
        )
        print(
            "Атлет с ближайшим по значению ростом: {}, его рост: {}".format(height_athelete, height)
        )

if __name__ == "__main__":
    main()