import os

from dotenv import load_dotenv
import requests
from flask import session, flash


import os
from dotenv import load_dotenv
import requests

import os
from dotenv import load_dotenv
import requests

load_dotenv()

PRODUCTS_URL = os.getenv("PRODUCTS_URL")
print(f"PRODUCTS_URL: {PRODUCTS_URL}")  # Отладочный вывод

def get_products():
    response = requests.get(PRODUCTS_URL)
    if response.status_code != 200:
        print(f"Ошибка: Сервер вернул статус {response.status_code}")
        print(response.text)  # Для отладки
        return []
    try:
        return response.json()
    except ValueError:
        print("Ошибка: Ответ сервера не является JSON")
        print(response.text)  # Для отладки
        return []

load_dotenv()

PRODUCTS_URL = os.getenv("PRODUCTS_URL")
print(f"PRODUCTS_URL: {PRODUCTS_URL}")  # Отладочный вывод

REVIEWS_URL = os.getenv("REVIEWS_URL")
USERS_URL = os.getenv("USERS_URL")
TOKENS_URL = os.getenv("TOKENS_URL")


def get_products(url: str = PRODUCTS_URL) -> list[dict]:
    return requests.get(url).json()


def get_product(product_id: str, url: str = PRODUCTS_URL) -> dict:
    return requests.get(url + product_id).json()


def add_product(name: str, description: str, img_url: str, price: float, url: str = PRODUCTS_URL) -> str:
    body = dict(
        name=name,
        description=description,
        img_url=img_url,
        price=price
    )
    return requests.post(url, json=body).json()


def update_product(
    product_id: str,
    name: str,
    description: str,
    img_url: str,
    price: float,
    url: str = PRODUCTS_URL
) -> str:
    body = dict(
        name=name,
        description=description,
        img_url=img_url,
        price=price
    )
    return requests.put(url + product_id, json=body).json()


def signup(first_name: str, last_name: str, email: str, password: str, url: str = USERS_URL):
    body = dict(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )

    resp = requests.post(url, json=body)
    if resp.status_code == 201:
        flash("Ви успішно зареєструвались")


def login(email: str, password: str, url: str = TOKENS_URL):
    body = dict(email=email, password=password)
    resp = requests.post(url, json=body)
    if resp.status_code == 200:
        session.update(resp.json())
        return "Вхід успішний"


def get_user(url: str = USERS_URL):
    token = session.get("access_token")
    header = dict(Authorization=f"Bearer {token}")
    resp = requests.get(url, headers=header)
    if resp.status_code == 200:
        return resp.json()
    else:
        return get_new_token()


def get_new_token(url: str = TOKENS_URL):
    token = session.get("refresh_token")
    header = dict(Authorization=f"Bearer {token}")
    resp = requests.get(url, headers=header)
    if resp.status_code == 200:
        session.update(resp.json())
        return get_user()