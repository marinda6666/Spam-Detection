from flask import Flask, render_template, request, session, redirect
from dotenv import load_dotenv
import requests
import random
import jwt
import os

from models import Message, Spam
from extensions import db

# sudo docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
load_dotenv()
emoji = ['🙃', '🥶', '🤠', '🤡', '😋', '😼', '🦜', '🐶', '🐨', '🐧']


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


def get_username_from_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload.get('username')
    except Exception as e:
        return None


@app.route('/')
@app.route('/menu', methods=['GET'])
def index():
    print('menu')
    token = request.cookies.get('jwt_token')
    username = get_username_from_jwt(token) if token else None
    if not username:
        return redirect('http://localhost:8080/login')
    
    messages = Message.query.filter_by(to_name=username).all()[::-1]

    return render_template('menu.html', 
                           username=username, 
                           icon=random.choice(emoji),
                           messages=messages)


@app.route('/compose', methods=['GET', 'POST'])
def compose():
    token = request.cookies.get('jwt_token')
    username = get_username_from_jwt(token) if token else None
    if not username:
        return redirect('http://localhost:8080/login')
    if request.method == 'POST':
        recipient = request.form['recipient']
        subject = request.form['subject']
        body = request.form['body']

        response = requests.get('http://spam_detector:8001/get_prediction', params={'msg': subject + ' ' + body}, timeout=5)
        if response.status_code == 200:
            result = response.json()
            is_spam = result.get('is_spam', 0)
            if is_spam:
                db.session.add(Spam(from_name=username,
                                       to_name=recipient,
                                       subject=subject,
                                       body=body))
                db.session.commit()
            else:
                db.session.add(Message(from_name=username,
                                    to_name=recipient,
                                    subject=subject,
                                    body=body))
                db.session.commit()
    return render_template('compose.html', username=username, icon=random.choice(emoji))


@app.route('/sentmsg', methods=['GET'])
def sentmsg():
    token = request.cookies.get('jwt_token')
    username = get_username_from_jwt(token) if token else None
    if not username:
        return redirect('http://localhost:8080/login')
    messages = Message.query.filter_by(from_name=username).all()[::-1]

    return render_template('sent.html', 
                           username=username, 
                           icon=random.choice(emoji),
                           messages=messages)


@app.route('/spam', methods=['GET'])
def spam():
    token = request.cookies.get('jwt_token')
    username = get_username_from_jwt(token) if token else None
    if not username:
        return redirect('http://localhost:8080/login')
    messages = Spam.query.filter_by(to_name=username).all()[::-1]

    return render_template('spam.html', 
                           username=username, 
                           icon=random.choice(emoji),
                           messages=messages)


@app.route('/message/<int:message_id>')
def message(message_id: int):
    token = request.cookies.get('jwt_token')
    username = get_username_from_jwt(token) if token else None
    if not username:
        return redirect('http://localhost:8080/login')
    
    message = Message.query.get(message_id)
    if not message:
        return redirect('/menu')
    
    
    return render_template('message.html',
                            username=username,
                            icon=random.choice(emoji),
                            message=message)

@app.route('/spam_message/<int:message_id>')
def spam_message(message_id: int):
    token = request.cookies.get('jwt_token')
    username = get_username_from_jwt(token) if token else None
    if not username:
        return redirect('http://localhost:8080/login')
    
    message = Spam.query.get(message_id)
    if not message:
        return redirect('/spam')
    
    
    return render_template('message.html',
                            username=username,
                            icon=random.choice(emoji),
                            message=message)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)