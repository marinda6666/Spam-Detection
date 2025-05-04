from flask import Flask, request, render_template_string

app = Flask(__name__)

# Хранилище сообщений (в памяти, при перезапуске сервера пропадут)
messages = {}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Простая почта</title>
</head>
<body>
    <h1>Отправить сообщение</h1>
    <form method="POST">
        <p>Ваше имя: <input type="text" name="sender" required></p>
        <p>Кому: <input type="text" name="recipient" required></p>
        <p>Сообщение: <textarea name="message" required></textarea></p>
        <button type="submit">Отправить</button>
    </form>

    <h1>Ваши сообщения ({{ username }})</h1>
    <form method="GET">
        <p>Показать сообщения для: <input type="text" name="username" value="{{ username }}">
        <button type="submit">Показать</button></p>
    </form>
    
    {% if user_messages %}
        <ul>
        {% for msg in user_messages %}
            <li><strong>От {{ msg.sender }}:</strong> {{ msg.message }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>Нет сообщений</p>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    username = request.args.get('username', '')
    
    if request.method == 'POST':
        sender = request.form['sender']
        recipient = request.form['recipient']
        message = request.form['message']
        
        if recipient not in messages:
            messages[recipient] = []
        messages[recipient].append({
            'sender': sender,
            'message': message
        })
    
    user_messages = messages.get(username, [])
    return render_template_string(HTML, username=username, user_messages=user_messages)

if __name__ == '__main__':
    app.run(debug=True) 