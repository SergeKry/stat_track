from django.test import TestCase
from ..utils import Puzzle
from ..views import StatisticsAPIMixin


class PuzzleTestCase(TestCase):
    def create_puzzle(self):
        return Puzzle()

    def test_puzzle_creation(self):
        puzzle = self.create_puzzle()
        self.assertTrue(1 <= puzzle.a <= 10)
        self.assertTrue(1 <= puzzle.b <= 10)


class StatisticsAPIMixinTestCase(TestCase):
    def test_get_attributes_without_passing_them(self):
        obj = StatisticsAPIMixin()
        endpoint, parameters, json = obj.get_attributes(None, None, None)
        self.assertIs(endpoint, None)
        self.assertIs(parameters, None)
        self.assertIs(json, None)

        self.assertIs(obj.endpoint, None)
        self.assertIs(obj.parameters, None)
        self.assertIs(obj.json, None)

        new_obj = StatisticsAPIMixin()
        new_obj.endpoint = 'endpoint'
        new_obj.parameters = {'parameters': 'parameters'}
        new_obj.json = {'json': 'data'}
        endpoint, parameters, json = obj.get_attributes(None, None, None)
        self.assertEqual(new_obj.endpoint, 'endpoint')
        self.assertEqual(new_obj.parameters, {'parameters': 'parameters'})
        self.assertEqual(new_obj.json, {'json': 'data'})

    def test_get_attributes_with_passing_them(self):
        obj = StatisticsAPIMixin()
        endpoint, parameters, json = obj.get_attributes('endpoint', 'parameters', 'json')

        self.assertEqual(endpoint, 'endpoint')
        self.assertEqual(parameters, 'parameters')
        self.assertEqual(json, 'json')

    def test_get_response(self):
        obj = StatisticsAPIMixin()
        obj.endpoint = 'get_players/'
        obj.parameters = {'username': 'PzWf'}
        response = obj.get_response()
        self.assertIsNotNone(response)

        pk_obj = StatisticsAPIMixin()
        pk_obj.endpoint = 'player_stats/'
        pk_obj.pk = 595861151
        response2 = pk_obj.get_response()
        self.assertIsNotNone(response2)


