from flask import Flask, request, render_template, json, jsonify
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from arbolB import BTree
from ListaDobleUsuarios import DoubleListUser
app = Flask(__name__)

miarbol = BTree(5)
users = DoubleListUser()

@app.route('/')
def index():
    return render_template('hello.html', name='Estructuras De Datos')

# LogIn
#   Devuelve true si el usuario exite
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/insert/<id>', methods=['GET'])
def insert(id):
    miarbol.insert(id)
    return id, True

# Registro
@app.route('/registrarse')
def registrarse():
    return render_template('Registro.html')

@app.route('/registro_terminado', methods=['POST'])
def registro_terminado():
    correo=request.form['correo']
    password=request.form['password']
    res = users.append(correo, password)
    return render_template('RegistroTerminado.html', correo=correo, password=password, created=res)

# Usuarios
@app.route('/usuarios')
def showUsers():
    res = users.show()
    return json.dumps(res)

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=int("5000"),
        debug=True
    )
