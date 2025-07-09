import allure
import pytest
from ..utils.api import StellarBurgersApi
from utils.helpers import generate_random_user_data


@allure.feature('Получение заказов пользователя')
class TestGetUserOrders:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.api = StellarBurgersApi()
        self.user_data = generate_random_user_data()
        response = self.api.register_user(self.user_data)
        self.token = response.json()['accessToken']
        self.valid_ingredients = ['60d3b41abdacab0026a733c6', '60d3b41abdacab0026a733c7']
        self.api.create_order(self.valid_ingredients, self.token)
        yield
        self.api.delete_user(self.token)

    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_orders_authorized(self):
        response = self.api.get_user_orders(self.token)
        assert response.status_code == 200
        assert 'orders' in response.json()
        assert len(response.json()['orders']) > 0

    @allure.title('Получение заказов неавторизованного пользователя')
    def test_get_orders_unauthorized(self):
        response = self.api.get_user_orders('invalid_token')
        assert response.status_code == 401
        assert response.json()['message'] == 'You should be authorised'