from flask import Flask, request, render_template, json
from arbolBCarpetas import BTree
from arbolAVLArchivos import AVLTree
from ListaDobleUsuarios import DoubleListUser
app = Flask(__name__)

miarbol = BTree(5)
archivos = AVLTree()
users = DoubleListUser()

@app.route('/')
def index():
    return render_template('hello.html', name='Estructuras De Datos')

# LogIn
#   Devuelve true si el usuario exite
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/carpetas', methods=['GET'])
def insert():
    miarbol.insertar(5)
    miarbol.insertar(6)
    miarbol.insertar(7)
    miarbol.insertar(8)
    # miarbol.insertar(10)
    # miarbol.insertar(11)
    # miarbol.insertar(12)
    # miarbol.insertar(14)
    # miarbol.insertar(15)
    # miarbol.insertar(16)
    # miarbol.insertar(18)
    # miarbol.insertar(19)
    # miarbol.insertar(20)
    # miarbol.insertar(21)
    # miarbol.insertar(30)
    # miarbol.insertar(35)
    # miarbol.insertar(39)
    # miarbol.insertar(46)
    # miarbol.insertar(56)
    # miarbol.insertar(66)
    # miarbol.insertar(70)
    # miarbol.insertar(71)
    # miarbol.insertar(72)
    # miarbol.insertar(75)
    # miarbol.insertar(81)
    # miarbol.insertar(82)

    res = miarbol.getDot()

    return str(res)

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
    # res = users.show()
    res = users.getDot()
    print(res)
    return str(res)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        # port=int("5000"),
        debug=True
    )
