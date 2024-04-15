from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Секретный ключ для защиты сессий
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Путь к файлу базы данных
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Модель для таблицы пользователей
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        # Хешируем пароль
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Создаем нового пользователя
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Вы успешно зарегистрировались!', 'success')
        return redirect('/')
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)