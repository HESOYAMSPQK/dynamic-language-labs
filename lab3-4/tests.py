import unittest
from flask import Flask
from flask.testing import FlaskClient

from main import app

class FlaskTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_index_page(self):  # Тестирование главной страницы
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)  # Проверяем, что получаем код ответа 200 (успех)
        self.assertIn(b'Trigonometric Calculator', response.data) # Проверяем, что на странице присутствует определенный текст

    def test_calculation(self):
        response = self.app.post('/', data=dict(angle='45', precision='2', unit='degrees')) # Отправляем POST-запрос с определенными данными
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sine: 0.71', response.data)
        self.assertIn(b'Cosine: 0.71', response.data)
        self.assertIn(b'Tangent: 1.0', response.data)

if __name__ == '__main__':
    unittest.main()