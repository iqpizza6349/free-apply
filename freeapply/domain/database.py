# domain 과 property 를 바탕으로 직접 엔티티를 만들어야함
# 예를 들어 Domain(name="Person", properties=[Property(name="name", type=str), Property(name="age", type=int)])
# 위와 같이 정의 되어 있다면, 이를 하나 하나 분해하여 엔티티로 만들고 저장하도록 해야한다.
from typing import List

from sqlalchemy import create_engine, Column, Integer, Table, MetaData, String, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from freeapply import config

SQLALCHEMY_DATABASE_URL = config.get_database_url()
print(f"The database url is {SQLALCHEMY_DATABASE_URL}")

Base = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()
Base.metadata.create_all(engine)


class Property(object):
    def __init__(self, _type, name: str):
        self.typo = _type
        self.name = name


def create_new_domain(domain_name: str, properties: List[Property]):
    if properties is None or properties == []:
        raise ValueError("Property list is empty")

    session = Session(engine)

    Table(
        domain_name,
        metadata,
        Column('id', Integer, primary_key=True),
        *(Column(prop.name, prop.typo) for prop in properties)
    )
    metadata.create_all(engine)
    session.commit()
    session.close()


def has_table(table_name: str) -> bool:
    inspector = inspect(engine)
    return inspector.has_table(table_name)
