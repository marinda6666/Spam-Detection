from flask import Flask, render_template, request, session, redirect
from dotenv import load_dotenv
import jwt
import os

# sudo docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
load_dotenv()

app = Flask(__name__)
SECRET_KEY = os.getenv("SECRET_KEY")
app.config['SECRET_KEY'] = SECRET_KEY

def get_username_from_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload.get('username')
    except Exception as e:
        return None

@app.route('/')
@app.route('/menu', methods=['GET'])
def index():
    # print(session.get('username'))
    token = request.cookies.get('jwt_token')
    username = get_username_from_jwt(token) if token else None
    if not username:
        return redirect('http://localhost:8080/login')
    return render_template('menu.html', username=username)

@app.route('/compose', methods=['GET'])
def compose():
    token = request.cookies.get('jwt_token')
    username = get_username_from_jwt(token) if token else None
    if not username:
        return redirect('http://localhost:8080/menu')
    
    return render_template('compose.html', username=username)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)