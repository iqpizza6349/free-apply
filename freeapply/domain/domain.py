# domain 과 property 를 바탕으로 직접 엔티티를 만들어야함
# 예를 들어 Domain(name="Person", properties=[Property(name="name", type=str), Property(name="age", type=int)])
# 위와 같이 정의 되어 있다면, 이를 하나 하나 분해하여 엔티티로 만들고 저장하도록 해야한다.
"""
domain.py
=========
A function-based module that aims to dynamically create domains.

Attributes:
    Base(declarative_base): SQLAlchemy level of base

Classes:
    Property: defines each column that use for domain
    DomainDynamicCreation: create domain by dynamic

Todo:
    * Write comment for this module file
    * Write comment for each function

author: iqpizza6349
"""

from typing import List

from sqlalchemy import Column, Integer, Table, MetaData, inspect, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class Property(object):
    def __init__(self, _type, name: str):
        self.typo = _type
        self.name = name


class DomainDynamicCreation:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.metadata = MetaData()

    def create_new_domain(self, domain_name: str, properties: List[Property]):
        if properties is None or properties == []:
            raise ValueError("Property list is empty")

        session = Session(self.engine)

        Table(
            domain_name,
            self.metadata,
            Column('id', Integer, primary_key=True),
            *(Column(prop.name, prop.typo) for prop in properties)
        )
        self.metadata.create_all(self.engine)
        session.commit()
        session.close()

    def has_domain(self, domain_name: str) -> bool:
        inspector = inspect(self.engine)
        return inspector.has_table(domain_name)

