import allure
import pytest
from ..utils.api import StellarBurgersApi
from utils.helpers import generate_random_user_data


@allure.feature('Создание пользователя')
class TestCreateUser:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.api = StellarBurgersApi()
        self.user_data = generate_random_user_data()
        yield
        if hasattr(self, 'token'):
            self.api.delete_user(self.token)

    @allure.title('Создание уникального пользователя')
    def test_create_unique_user(self):
        response = self.api.register_user(self.user_data)
        assert response.status_code == 200
        assert 'accessToken' in response.json()
        self.token = response.json()['accessToken']

    @allure.title('Создание уже зарегистрированного пользователя')
    def test_create_existing_user(self):
        response = self.api.register_user(self.user_data)
        self.token = response.json()['accessToken']
        
        response = self.api.register_user(self.user_data)
        assert response.status_code == 403
        assert response.json()['message'] == 'User already exists'

    @allure.title('Создание пользователя без обязательного поля')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_create_user_missing_field(self, field):
        incomplete_data = self.user_data.copy()
        del incomplete_data[field]
        response = self.api.register_user(incomplete_data)
        assert response.status_code == 403
        assert response.json()['message'] == 'Email, password and name are required fields'