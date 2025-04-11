import os
import binascii

from flask import Flask, request, url_for, redirect, render_template, session, flash

from src.data import data_actions
from src.data.forms import SignUpForm, LoginForm

app = Flask(__name__, template_folder="src/templates")
app.secret_key = binascii.hexlify(os.urandom(24)).decode()

# Главная страница с продуктами
@app.get("/")
def index():
    try:
        products = data_actions.get_products()
        return render_template("index.html", products=products)
    except Exception as e:
        flash(f"Ошибка загрузки продуктов: {str(e)}")
        return render_template("index.html", products=[])

# Страница продукта
@app.get("/product/<product_id>/")
def get_product(product_id):
    try:
        product = data_actions.get_product(product_id)
        if not product:
            flash("Продукт не найден")
            return redirect(url_for("index"))
        return render_template("product.html", product=product)
    except Exception as e:
        flash(f"Ошибка загрузки продукта: {str(e)}")
        return redirect(url_for("index"))

# Покупка продукта
@app.get("/buy_product/<product_id>/")
def buy_product(product_id):
    try:
        product = data_actions.get_product(product_id)
        if not product:
            flash("Продукт не найден")
            return redirect(url_for("index"))
        return f"Ви успішно придбали '{product['name']}'"
    except Exception as e:
        flash(f"Ошибка покупки продукта: {str(e)}")
        return redirect(url_for("index"))

# Личный кабинет
@app.get("/cabinet/")
def cabinet():
    try:
        user = data_actions.get_user()
        if user:
            return render_template("cabinet.html", user=user)
        else:
            return redirect(url_for("login"))
    except Exception as e:
        flash(f"Ошибка загрузки данных пользователя: {str(e)}")
        return redirect(url_for("login"))

# Регистрация
@app.route("/signup/", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            data_actions.signup(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data,
            )
            flash("Вы успешно зарегистрировались!")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Ошибка регистрации: {str(e)}")
    return render_template("signup.html", form=form)

# Авторизация
@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            message = data_actions.login(
                email=form.email.data,
                password=form.password.data,
            )
            flash(message)
            return redirect(url_for("cabinet"))
        except Exception as e:
            flash(f"Ошибка авторизации: {str(e)}")
    return render_template("login.html", form=form)

if __name__ == "__main__":
    app.run(debug=True, port=5000)