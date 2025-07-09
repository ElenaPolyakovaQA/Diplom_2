import random
import string


def generate_random_user_data():
    """Генерация случайных данных пользователя"""
    username = ''.join(random.choices(string.ascii_lowercase, k=8))
    return {
        'email': f'{username}@example.com',
        'password': ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
        'name': username.capitalize()
    }