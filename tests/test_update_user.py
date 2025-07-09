import allure
import pytest
from ..utils.api import StellarBurgersApi
from utils.helpers import generate_random_user_data


@allure.feature('Обновление данных пользователя')
class TestUpdateUser:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.api = StellarBurgersApi()
        self.user_data = generate_random_user_data()
        response = self.api.register_user(self.user_data)
        self.token = response.json()['accessToken']
        yield
        self.api.delete_user(self.token)

    @allure.title('Обновление данных с авторизацией')
    @pytest.mark.parametrize('field,value', [
        ('email', 'newemail@example.com'),
        ('password', 'newpassword123'),
        ('name', 'New Name')
    ])
    def test_update_user_authorized(self, field, value):
        update_data = {field: value}
        response = self.api.update_user(update_data, self.token)
        assert response.status_code == 200
        assert response.json()['user'][field] == value

    @allure.title('Обновление данных без авторизации')
    @pytest.mark.parametrize('field,value', [
        ('email', 'newemail@example.com'),
        ('password', 'newpassword123'),
        ('name', 'New Name')
    ])
    def test_update_user_unauthorized(self, field, value):
        update_data = {field: value}
        response = self.api.update_user(update_data)
        assert response.status_code == 401
        assert response.json()['message'] == 'You should be authorised'