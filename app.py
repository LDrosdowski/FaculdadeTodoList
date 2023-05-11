from flask import Flask, render_template, request, redirect, session
import requests as rs
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# URL da API
api_url = 'https://todolist-api.edsonmelo.com.br'

@app.route('/')
def index():
    return redirect('login')

@app.route('/login', methods=['GET'])
def loginPage():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
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

    if 'token' in status:
        token = status['token']
        session['token'] = token
        return redirect ('tasks/list')
    else:
        error = status.get('error', 'Incorrect username and/or password')
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

@app.route('/tasks/list')
def tasksPage():
    return render_template('list.html')

@app.route('/tasks/list', methods=['POST'])
def newTask():
    taskName = request.form['taskName']

    signup_data = {
        'name': taskName
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': session['token']
    }

    response = rs.post(api_url + '/api/task/new/', json=signup_data, headers=headers)
    status = response.json()
    message = status['message']

    if message == "Task Successfully Added":
        success = status.get('success', 'Task Successfully Added')
        return render_template('list.html', success=success)
    else:
        error = status.get('error', 'Could Not Add Task')
        return render_template('list.html', error=error)

@app.route('/delete')
def deleteTaskPage():
    return render_template('delete.html')

@app.route('/delete', methods=['DELETE'])
def deleteTask():
    taskId = request.form['taskId']
    
    signup_data = {
         'taskId': taskId
     }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': session['token']
    }

    response = rs.delete(api_url + '/api/task/delete/', json=taskId, headers=headers)
    status = response.json()
    message = status['message']
    print(message)

    if message == "Task deleted Successfully":
        success = status.get('success', 'Task deleted Successfully')
        return render_template('delete.html', success=success)
    else:
        error = status.get('error', 'Task not exist')
        return render_template('delete.html', error=error)

@app.route('/edit')
def editTaskPage():
    return render_template('edit.html')

@app.route('/edit', methods=['PUT'])
def editTask():
    taskId = request.form['taskId']
    name = request.form['name']
    realized = request.form['realized']
    
    signup_data = {
        'taskId': taskId,
        'name': name,
        'realized': realized
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': session['token']
    }

    response = rs.put(api_url + '/api/task/update/', json=signup_data, headers=headers)
    status = response.json()
    message = status['message']

    if message == "Task Successfully Updated":
        success = status.get('success', 'Task Successfully Updated')
        return render_template('edit.html', success=success)
    else:
        error = status.get('error', 'Task(s) not found')
        return render_template('edit.html', error=error)

if __name__ == '__main__':
    app.run()
