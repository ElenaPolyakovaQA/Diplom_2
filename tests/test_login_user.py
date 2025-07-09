import allure
import pytest
from ..utils.api import StellarBurgersApi
from utils.helpers import generate_random_user_data


@allure.feature('Авторизация пользователя')
class TestLoginUser:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.api = StellarBurgersApi()
        self.user_data = generate_random_user_data()
        response = self.api.register_user(self.user_data)
        self.token = response.json()['accessToken']
        yield
        self.api.delete_user(self.token)

    @allure.title('Успешная авторизация существующего пользователя')
    def test_login_existing_user(self):
        response = self.api.login_user({
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        assert response.status_code == 200
        assert 'accessToken' in response.json()

    @allure.title('Авторизация с неверными данными')
    @pytest.mark.parametrize('email,password,message', [
        ('wrong@email.com', 'validpass', 'email or password are incorrect'),
        ('valid@email.com', 'wrongpass', 'email or password are incorrect'),
        ('', 'validpass', 'email or password are incorrect'),
        ('valid@email.com', '', 'email or password are incorrect')
    ])
    def test_login_invalid_credentials(self, email, password, message):
        test_email = email if email != 'valid@email.com' else self.user_data['email']
        test_password = password if password != 'validpass' else self.user_data['password']
        
        response = self.api.login_user({
            'email': test_email,
            'password': test_password
        })
        assert response.status_code == 401
        assert response.json()['message'] == message