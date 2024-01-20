from sqlalchemy import create_engine, Integer, String
from sqlalchemy.orm import sessionmaker

from freeapply.domain.domain import DomainDynamicCreation, Property

import unittest

from freeapply.domain.property import ForeignProperty


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        self.Session = sessionmaker(self.engine)
        self.dynamic_creation = DomainDynamicCreation(self.engine)

    def test_create_domain(self):
        domain_name = "song"
        title = Property(name="title", _type=String)
        artist = Property(name="artist", _type=String)
        likes = Property(name="likes", _type=Integer)

        self.dynamic_creation.create_new_domain(domain_name, [title, artist, likes])

        has_domain = self.dynamic_creation.has_domain(domain_name)
        self.assertTrue(has_domain)

    def test_create_domain_with_relation(self):
        parent = "artist"
        parent_name = Property(name="name", _type=String)

        child = "song"
        child_title = Property(name="title", _type=String)
        child_artist = Property(_type=Integer, name="artist_id")

        self.dynamic_creation.create_new_domain(parent, [parent_name])
        self.dynamic_creation.create_new_domain(child, [child_title, child_artist])

        has_parent = self.dynamic_creation.has_domain(parent)
        has_child = self.dynamic_creation.has_domain(child)
        self.assertTrue(has_parent)
        self.assertTrue(has_child)

        foreign = ForeignProperty(column="artist_id", ref_column="id")
        self.dynamic_creation.create_relationship(parent, child, foreign)

        has_relationship = self.dynamic_creation.has_relation(parent, child)
        self.assertTrue(has_relationship)


if __name__ == '__main__':
    unittest.main()
