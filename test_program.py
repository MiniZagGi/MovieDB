import unittest
from unittest.mock import MagicMock
from program import get_avalible_media_types, insert_director

class TestProgram(unittest.TestCase):
    def setUp(self):
        self.cursor_mock = MagicMock()
        self.cursor_mock.execute.return_value = None

    def test_get_avalible_media_types_returns_expected_media_types(self):
        self.cursor_mock.fetchone.return_value = [('DVD',), ('Blu-ray',), ('Digital',)]
        result = get_avalible_media_types(self.cursor_mock)
        self.assertEqual(result, [('DVD',), ('Blu-ray',), ('Digital',)])

    def test_insert_director_returns_existing_director_id(self):
        self.cursor_mock.fetchone.return_value = (1,)
        result = insert_director(self.cursor_mock, "John Doe")
        self.assertEqual(result, 1)

    def test_insert_director_inserts_new_director_and_returns_director_id(self):
        self.cursor_mock.fetchone.return_value = None
        self.cursor_mock.lastrowid = 2
        result = insert_director(self.cursor_mock, "Jane Smith")
        self.assertEqual(result, 2)

if __name__ == '__main__':
    unittest.main()