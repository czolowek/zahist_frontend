from flask_wtf import FlaskForm
import wtforms


class SignUpForm(FlaskForm):
    first_name = wtforms.StringField("Введіть ім'я")
    last_name = wtforms.StringField("Введіть прізвище")
    email = wtforms.EmailField("Email", validators=[wtforms.validators.DataRequired(), wtforms.validators.Email()])
    password = wtforms.PasswordField("Пароль", validators=[wtforms.validators.length(6)])
    submit = wtforms.SubmitField("Зареєструватись")


class LoginForm(FlaskForm):
    email = wtforms.EmailField("Email", validators=[wtforms.validators.DataRequired(), wtforms.validators.Email()])
    password = wtforms.PasswordField("Пароль", validators=[wtforms.validators.length(6)])
    submit = wtforms.SubmitField("Увійти")