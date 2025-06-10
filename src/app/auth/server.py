from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, make_response
from dotenv import load_dotenv
from hashlib import sha256
import os
import jwt
import datetime

from extensions import db
from models import User

# sudo docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@host.docker.internal:{DB_PORT}/{DB_NAME}"
)

db.init_app(app)

def validate_password(password):
    if len(password) < 8:
        return False, 'Пароль слишком короткий, \
он должен содержать минимум 8 символов.'
    if not any(c.isupper() for c in password):
        return False, 'Пароль должен содержать хотя бы одну заглавную букву.'
    if not any(c.islower() for c in password):
        return False, 'Пароль должен содержать хотя бы одну строчную букву.'
    if not any(c.isdigit() for c in password):
        return False, 'Пароль должен содержать хотя бы одну цифру.'
    if not any(c in '@#$%^& * ()_+-=!?' for c in password):
        return False, 'Пароль должен содержать \
хотя бы один специальный символ.'
    return True, ''

def generate_jwt(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.now() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def get_username_from_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload.get('username')
    except Exception as e:
        return None


@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    get_flashed_messages()
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        p_and_u = password + username
        crypto_password = sha256(p_and_u.encode('utf-8')).hexdigest()
        finded = User.query.filter_by(name=username).first()
        usr_psw = ''
        if finded != None:
            usr_psw = finded.password
        if len(usr_psw) != 0:
            if usr_psw == crypto_password:
                flash('вы вошли в аккаунт', category='success')
                token = generate_jwt(username)
                response = make_response(redirect('http://localhost:8080/menu'))
                response.set_cookie(
                                    'jwt_token', 
                                    token,
                                    httponly=True,
                                    secure=False,      
                                    samesite='Lax',   
                                    domain='localhost',
                                    path='/',         
                                    max_age=86400     
                                )

                return response
            else:
                flash('ошибка', category='error')
        else:
            flash('такого аккаунта нет', category='error')
            pass
    return render_template('login.html')



@app.route('/registerr', methods=['POST', 'GET'])
def registerr():
    get_flashed_messages()

    if request.method == 'POST':
        error = False
        username = request.form['username']
        if username == '':
            error = True
            flash('введите никнейм', category='error')
        password = request.form['password']
        if password == '':
            error = True
            flash('введите пароль', category='error')

        p_and_u = password + username
        crypto_password = sha256(p_and_u.encode('utf-8')).hexdigest()
        finded = User.query.filter_by(name=username).first()
        if finded is None and error is False and validate_password(password)[0] is True:
            user = User(id=User.query.count() + 1, name=username, password=crypto_password)
            db.session.add(user)
            flash('аккаунт создан', category='success')
            db.session.commit()
        elif validate_password(password)[0] is False:
            flash(validate_password(password)[1], category='error')
        if finded is not None and error is False:
            flash('такой аккаунт уже существует', category='error')
    return render_template('register.html')

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5001)