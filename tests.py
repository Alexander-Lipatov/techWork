import unittest
from db import Database
from main import App

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        # Добавьте тестовые данные в базу данных
        self.db.add_template({"name": "Order Form", "user_name": "text", "order_date": "date"})
        self.db.add_template({"name": "Contact Form", "user_email": "email", "user_phone": "phone"})
        self.db.add_template({"name": "Profile Form", "username": "text", "created": "date",
         "useremail": "email", "userphone": "phone"})

    def test_unique_templates(self):
        # Получаем все шаблоны из базы данных
        templates = self.db.get_all_templates()

        # Проверяем, что количество шаблонов в базе данных соответствует ожидаемому
        self.assertEqual(len(templates), 3)

        # Проверяем уникальность имен шаблонов
        names = [template["name"] for template in templates]
        self.assertEqual(len(names), len(set(names)))  # Проверяем, что все имена уникальны


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.app.app.config['TESTING'] = True
        self.client = self.app.app.test_client()

    def test_get_form_with_valid_data(self):
        # Mock a valid form data
        valid_form_data = {'user_name': 'John Doe', 'order_date': '2023-11-20'}

        # Send a POST request to '/get_form'
        response = self.client.post('/get_form', data=valid_form_data)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Validate the response content
        expected_response = {'template_name': 'Order Form'}
        self.assertEqual(response.json, expected_response)

    def test_get_form_with_invalid_data(self):
        # Mock an invalid form data
        invalid_form_data = {'user_email': 'invalidemail', 'user_phone': '123'}

        # Send a POST request to '/get_form'
        response = self.client.post('/get_form', data=invalid_form_data)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Validate the response content
        expected_response = {'error': ["Field 'user_email' is not valid", "Field 'user_phone' is not valid"]}
        self.assertEqual(response.json, expected_response)


class TestValidation(unittest.TestCase):

    def setUp(self):
        self.app = App()

    def test_date_validation(self):
        self.assertTrue(self.app.validate_date("10.11.2023"))  # Правильный формат даты
        self.assertFalse(self.app.validate_date("2023-11-10"))  # Неправильный формат даты
        self.assertFalse(self.app.validate_date("31.02.2023"))  # Несуществующая дата

    def test_phone_validation(self):
        self.assertTrue(self.app.validate_phone("+71234567890"))  # Правильный формат телефона
        self.assertFalse(self.app.validate_phone("71234567890"))  # Неправильный формат телефона
        self.assertFalse(self.app.validate_phone("+712345678901"))  # Неправильный формат телефона

    def test_email_validation(self):
        self.assertTrue(self.app.validate_email("test@example.com"))  # Правильный формат email
        self.assertFalse(self.app.validate_email("testexample.com"))  # Неправильный формат email
        self.assertFalse(self.app.validate_email("test@examplecom"))  # Неправильный формат email

if __name__ == '__main__':
    unittest.main()