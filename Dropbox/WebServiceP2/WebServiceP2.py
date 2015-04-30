import json, random
from flask import Flask, request, abort, render_template, json, jsonify

app = Flask(__name__)

# def abort_if_user_doesnt_exist(user_id):
#     if user_id not in USERS:
#         abort(404, message="User {} doesn't exist".format(user_id))

@app.route('/')
def index():
    return render_template('hello.html', name='Estructuras De Datos')

# LogIn
#   Devuelve true si esta registrado el usuario
@app.route('/login', methods=['POST'])
def login():
    return 'True'

#   Muestra la lista completa de vuelos
@app.route('/vuelos', methods=['GET'])
def vuelos():
    # res=[]
    # avlVuelos.inorder(avlVuelos.rootNode, res)
    # return json.dumps(res)
    return True

@app.route('/vuelo/id', methods=['POST'])
def vuelosId():
    id_fly = request.form['id_fly']
    # return json.dumps(res)
    return id_fly

if __name__ == '__main__':
    app.run(
        # host="0.0.0.0",
        # port=int("5000")
        debug=True
    )
