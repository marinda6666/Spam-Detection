from flask import Flask, render_template, request, redirect, url_for

# sudo docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest

app = Flask(__name__)

@app.route('/login', methods=['POST', 'GET'])
@app.route('/')
def login():
    if request.method == 'POST':
        print(request.form.get('username'))
        return redirect('http://localhost:8000/menu')
    return render_template('login.html')

def index():
    return 'hai'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)