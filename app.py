from flask import Flask, render_template, request, redirect, session
import requests as rs

app = Flask(__name__)

# URL da API
api_url = 'https://todolist-api.edsonmelo.com.br'

@app.route('/login')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    login_data = {
        'username': username,
        'password': password
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = rs.post(api_url + '/api/user/login/', json=login_data, headers=headers)
    status = response.json()
    token = status['token']
    session['token'] = token

    if 'token' in status:
        redirect ('tasksPage')
    else:
        error = status.get('error', 'Erro de autenticação')
        return render_template('login.html', error=error)

@app.route('/signup', methods=['GET'])
def signupPage():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    signup_data = {
        'name': name,
        'email': email,
        'username': username,
        'password': password
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = rs.post(api_url + '/api/user/new/', json=signup_data, headers=headers)
    status = response.json()
    message = status['message']

    if message == "User Successfully Added":
        success = status.get('success', 'User Successfully Added')
        return render_template('signup.html', success=success)
    else:
        error = status.get('error', 'User Already Exists')
        return render_template('signup.html', error=error)

@app.route('/tasks/list', methods=['GET'])
def tasksPage():
    return render_template('list.html')

@app.route('/tasks')
def newTask():
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
