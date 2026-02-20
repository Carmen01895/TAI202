from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
API_URL = "http://localhost:5000/v1/usuarios"

@app.route('/')
def index():
    response = requests.get(API_URL)
    data = response.json()
    usuarios = data["usuarios"]
    return render_template('index.html', usuarios=usuarios)

@app.route('/add', methods=['POST'])
def agregar_usuario():
    nuevo_usuario = {
        "id": int(request.form['id']),
        "nombre": request.form['nombre'],
        "edad": int(request.form['edad'])
    }
    requests.post(API_URL, json=nuevo_usuario)
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    requests.delete(f"{API_URL}/{id}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5010, debug=True)