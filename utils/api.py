import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv('BASE_URL', 'https://stellarburgers.nomoreparties.site/api')


class StellarBurgersApi:
    def __init__(self):
        self.base_url = BASE_URL
    
    def register_user(self, data):
        return requests.post(f'{self.base_url}/auth/register', json=data)
    
    def login_user(self, data):
        return requests.post(f'{self.base_url}/auth/login', json=data)
    
    def update_user(self, data, token=None):
        headers = {'Authorization': f'Bearer {token}'} if token else None
        return requests.patch(f'{self.base_url}/auth/user', json=data, headers=headers)
    
    def create_order(self, ingredients, token=None):
        headers = {'Authorization': f'Bearer {token}'} if token else None
        return requests.post(f'{self.base_url}/orders', json={'ingredients': ingredients}, headers=headers)
    
    def get_user_orders(self, token):
        headers = {'Authorization': f'Bearer {token}'}
        return requests.get(f'{self.base_url}/orders', headers=headers)
    
    def delete_user(self, token):
        return requests.delete(f'{self.base_url}/auth/user', headers={'Authorization': f'Bearer {token}'})
    
    def get_ingredients(self):
        return requests.get(f'{self.base_url}/ingredients')