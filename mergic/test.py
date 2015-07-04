import mergic
import unittest


class TestCheck(unittest.TestCase):

    def test_raises_on_duplicate_in_value_list(self):
        with self.assertRaises(ValueError):
            mergic.check({1: [1, 1]})

    def test_raises_on_duplicates_across_keys(self):
        with self.assertRaises(ValueError):
            mergic.check({1: [1], 2: [1]})

    def test_returns_number_of_values(self):
        partition = {1: [1], 2: [2, 3], 3: [4]}
        self.assertEqual(mergic.check(partition), 4)


class TestLinkItems(unittest.TestCase):

    def test_doesnt_change_if_already_together(self):
        group = (1, 2)
        group_of = {1: group, 2: group}
        mergic.link_items(group_of, [(1, 2)])
        self.assertIs(group_of[1], group_of[2])

    def test_joins_to_same_thing(self):
        group_of = {1: (1,), 2: (2,)}
        mergic.link_items(group_of, [(1, 2)])
        self.assertIs(group_of[1], group_of[2])

    def test_joins_to_correct_tuple(self):
        group_of = {1: (1,), 2: (2,)}
        mergic.link_items(group_of, [(1, 2)])
        self.assertEqual(set(group_of[1]), set((1, 2)))


class TestDiff(unittest.TestCase):

    def test_no_diff_when_same(self):
        self.assertEqual(mergic.diff({1: [1]}, {1: [1]}), {})

    def test_order_doesnt_matter(self):
        self.assertEqual(mergic.diff({1: [1, 2]}, {1: [2, 1]}), {})

    def test_raises_when_first_doesnt_assign(self):
        with self.assertRaises(ValueError):
            mergic.diff({1: [1]}, {1: [1, 2]})

    def test_raises_when_second_doesnt_assign(self):
        with self.assertRaises(ValueError):
            mergic.diff({1: [1, 2]}, {1: [1]})

    def test_renaming_key_picked_up(self):
        self.assertEqual(mergic.diff({1: [1]}, {2: [1]}), {2: [1]})

    def test_splitting_value_picked_up(self):
        self.assertEqual(mergic.diff({1: [1, 2], 3: [3]},
                                     {1: [1], 2: [2], 3: [3]}),
                         {1: [1], 2: [2]})


if __name__ == '__main__':
    unittest.main()
