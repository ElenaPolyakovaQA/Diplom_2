import allure
import pytest
from ..utils.api import StellarBurgersApi
from utils.helpers import generate_random_user_data


@allure.feature('Создание заказа')
class TestCreateOrder:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.api = StellarBurgersApi()
        self.user_data = generate_random_user_data()
        response = self.api.register_user(self.user_data)
        self.token = response.json()['accessToken']
        ingredients_response = self.api.get_ingredients()
        self.valid_ingredients = [ingredient['_id'] for ingredient in ingredients_response.json()['data']][:2]
        yield
        self.api.delete_user(self.token)

    @allure.title('Создание заказа с авторизацией')
    def test_create_order_authorized(self):
        response = self.api.create_order(self.valid_ingredients, self.token)
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'name' in response.json()
        assert 'order' in response.json()

    @allure.title('Создание заказа без авторизации')
    def test_create_order_unauthorized(self):
        response = self.api.create_order(self.valid_ingredients)
        assert response.status_code == 401
        assert response.json()['message'] == 'You should be authorised'

    @allure.title('Создание заказа с ингредиентами')
    def test_create_order_with_ingredients(self):
        response = self.api.create_order(self.valid_ingredients, self.token)
        assert response.status_code == 200
        assert len(response.json()['order']['ingredients']) > 0

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self):
        response = self.api.create_order([], self.token)
        assert response.status_code == 400
        assert response.json()['message'] == 'Ingredient ids must be provided'

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_invalid_ingredients(self):
        response = self.api.create_order(['invalid_hash'], self.token)
        assert response.status_code == 500