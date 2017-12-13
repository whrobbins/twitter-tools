import unittest
from unittest import TestCase

from intros import member


class TestMember(TestCase):
    def setUp(self):
        pass

    def test_init(self):
        m = member.Member(email='hi@example.com', twitter='whrobbins')
        self.assertEqual(m.email, 'hi@example.com')
        self.assertEqual(m.twitter, 'whrobbins')

    def test_enforce_schema(self):
        m = member.Member(email='hi@example.com', twitter='whrobbins')
        m2 = member.Member(twitter='whrobbins')
        m_list = [m, m2]
        enforced = member.Member.enforce_schema_requirements({'email': 'required',
                                                              'twitter': 'optional'}, m_list)
        self.assertTrue(m in enforced)
        self.assertTrue(m2 not in enforced)

