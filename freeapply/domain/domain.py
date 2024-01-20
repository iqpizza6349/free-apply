# domain 과 property 를 바탕으로 직접 엔티티를 만들어야함
# 예를 들어 Domain(name="Person", properties=[Property(name="name", type=str), Property(name="age", type=int)])
# 위와 같이 정의 되어 있다면, 이를 하나 하나 분해하여 엔티티로 만들고 저장하도록 해야한다.
"""freeapply domain module.
domain.py
=========
A function-based module that aims to dynamically create domains.

Attributes:
    Base(declarative_base): SQLAlchemy level of base

Classes:
    DomainDynamicCreation: create domain by dynamic

author: iqpizza6349
"""

from typing import List

from sqlalchemy import Column, Integer, Table, MetaData, inspect, Engine, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from freeapply.domain.property import Property, ForeignProperty

Base = declarative_base()


class DomainDynamicCreation:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.metadata = MetaData()

    def create_new_domain(self, domain_name: str, properties: List[Property]):
        """create a new domain by dynamic

        Args:
            :param domain_name: new domain name
            :param properties: list of properties

        Returns:
            :return: nothing.
            create dynamic domain and no returns.

        Raises:
            :raise ValueError: if properties are not valid or empty

        """

        if properties is None or properties == []:
            raise ValueError("Property list is empty")

        table = Table(
            domain_name,
            self.metadata,
            Column('id', Integer, primary_key=True),
            *(Column(prop.name, prop.type) for prop in properties)
        )
        table.create(self.engine)
        self.metadata.create_all(self.engine)

    def create_relationship(self, parent_domain, child_domain, foreign: ForeignProperty):
        parent = self.metadata.tables[parent_domain]
        child = self.metadata.tables[child_domain]

        foreign_constraint = ForeignKeyConstraint([foreign.column], [parent.c.id])
        child.append_constraint(foreign_constraint)

    def has_domain(self, domain_name: str) -> bool:
        inspector = inspect(self.engine)
        return inspector.has_table(domain_name)

    def has_relation(self, parent_domain, child_domain) -> bool:
        parent = self.metadata.tables[parent_domain]
        child = self.metadata.tables[child_domain]

        parent_inspector = inspect(parent)
        child_inspector = inspect(child)

        # Retrieve relationships from foreign keys
        parent_relationships = [fk.target_fullname for fk in parent_inspector.foreign_keys]
        child_relationships = [fk.target_fullname for fk in child_inspector.foreign_keys]

        return parent_relationships != [] or child_relationships != []

