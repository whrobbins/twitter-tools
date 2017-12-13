import csv


class Member(object):
    """
    Represents a member of a group
    """
    DEFAULT_VALUE = ''
    REQUIRED = 'required'
    OPTIONAL = 'optional'
    VP_SCHEMA = {
        'name': REQUIRED,
        'email_address': REQUIRED,
        'major': OPTIONAL,
        'interests': OPTIONAL,
        'description': OPTIONAL,
        'twitter': OPTIONAL,
    }

    def __init__(self, *attrs, **kwargs):
        for d in attrs:
            for key, value in d.items():
                setattr(self, key, value)
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.contrary_vp_schema = {}

    def __getattr__(self, item):
        return Member.DEFAULT_VALUE

    @staticmethod
    def read_from_spreadsheet(filename):
        """
        Create a list of member objects from a CSV file
        :param filename: csv file to read
        :return: list of member objects
        """
        students = []
        with open(filename, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'Tarczynski' not in row['Name']:
                    students.append(row)

        members = []
        for s in students:
            members.append(Member(name=s['Name'],
                                  university=s['University'],
                                  email_address=s['Public Email'],
                                  major=s['Majors, Minors'],
                                  interests=s['Interests'],
                                  description=s['Description'],
                                  twitter=s['Twitter']))
        return Member.enforce_schema_requirements(Member.VP_SCHEMA, members)

    @staticmethod
    def enforce_schema_requirements(schema, member):
        """
        Make sure that the given Member object abides by some pre-defined schema
        :param schema: dict schema to follow
        :param member: list or individual Member object
        :return: list or individual Member
        """
        def is_valid(m):
            for required_key, value in schema.items():
                member_attr = getattr(m, str(required_key))
                if member_attr == Member.DEFAULT_VALUE and schema[required_key] != Member.OPTIONAL:
                    return False
            return True

        if type(member) == list:
            return [m for m in member if is_valid(m)]
        else:
            return member if is_valid(schema, member) else None
