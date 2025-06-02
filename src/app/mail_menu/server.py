from flask import Flask, render_template, request

# sudo docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest

app = Flask(__name__)
@app.route('/')
@app.route('/menu', methods=['GET'])
def index():
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)