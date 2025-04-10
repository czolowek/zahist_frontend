import os
import binascii

from flask import Flask, request, url_for, redirect, render_template, session, flash

from src.data import data_actions
from src.data.forms import SignUpForm, LoginForm

URL = "https://rozetka.com.ua/ua/igrovie-mishi/c4673278/producer=logitech/"

app = Flask(__name__, template_folder="src/templates")
app.secret_key = binascii.hexlify(os.urandom(24))


@app.get("/")
def index():
    products = data_actions.get_products()
    return render_template("index.html", products=products)


@app.get("/product/<product_id>/")
def get_product(product_id):
    product = data_actions.get_product(product_id)
    return render_template("product.html", product=product)


@app.get("/buy_product/<product_id>/")
def buy_product(product_id):
    product = data_actions.get_product(product_id)
    return f"Ви успішно придбали '{product['name']}'"


@app.get("/cabinet/")
def cabinet():
    user = data_actions.get_user()
    if user:
        return render_template("cabinet.html", user=user)
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)