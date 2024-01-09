from sqlalchemy import create_engine, Integer, String
from sqlalchemy.orm import sessionmaker

from freeapply.domain.domain import DomainDynamicCreation, Property

import unittest


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


if __name__ == '__main__':
    unittest.main()
