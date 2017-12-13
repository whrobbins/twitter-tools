import random

from intros.intro_config import *


class Matching(object):
    """
    Object that matches users withing some group in a specified way
    """
    @staticmethod
    def vp_region_matching(students, print_=True):
        """
        Match Contrary Venture Partners with someone else in their region but at a different school
        """
        # mapping to VPs
        buckets = {
            'West': [],
            'Midwest': [],
            'South': [],
            'East': [],
        }

        for student in students:
            buckets[schools[student.university]].append(student)

        regions = [team for _, team in buckets.items()]

        def check_for_same_pod_match(team):
            for i in range(0, len(team) - 1, 2):
                if team[i].university == team[i + 1].university:
                    return True
            return False

        for team in regions:
            while check_for_same_pod_match(team):
                random.shuffle(team)

        # kick someone out of odd-length region and pair up
        pairs = []
        for region in regions:
            for i in range(0, len(region) - 1, 2):
                pairs.append((region[i], region[i + 1]))

        if print_:
            print('Pairs:')
            for pair in pairs:
                a, b = pair[0], pair[1]
                print(a.name, b.name, sep=' + ')

        return pairs
