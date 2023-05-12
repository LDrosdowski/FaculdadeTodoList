from flask import Flask, render_template, request, redirect
import requests as rs

app = Flask(__name__)

# URL da API
api_url = 'https://localhost:8000'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    login_data = {
        'username': username,
        'password': password
    }

    response = rs.post(api_url + '/auth', json=login_data)
    data = response.json()

    if 'token' in data:
        return redirect('/tasks?token=' + data['token'])
    else:
        error = data.get('error', 'Erro de autenticação')
        return render_template('login.html', error=error)

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    signup_data = {
        'username': username,
        'password': password
    }

    response = rs.post(api_url + '/signup', json=signup_data)
    data = response.json()

    if 'token' in data:
        return redirect('/tasks?token=' + data['token'])
    else:
        error = data.get('error', 'Erro ao criar conta')
        return render_template('signup.html', error=error)

@app.route('/tasks')
def tasks():
    token = request.args.get('token')

    headers = {
        'Authorization': 'Bearer ' + token
    }

    response = rs.get(api_url + '/tasks', headers=headers)
    data = response.json()

    tasks = data.get('tasks', [])

    return render_template('tasks.html', tasks=tasks)

if __name__ == '__main__':
    app.run()
