from flask import Flask, render_template, request, jsonify, redirect
from db import logs_table
from robot import Robot
from scanport import scanport
from tinydb import TinyDB

app = Flask(__name__, template_folder='../templates')

db = TinyDB('db.json')
robot = None  
@app.route('/')
def logs():
    logs = logs_table.all()
    return render_template('log.html', logs=logs)

@app.route('/fetch_logs')
def fetch_logs():
    logs = logs_table.all()
    return jsonify(logs)

@app.route('/control', methods=['GET', 'POST'])
def control():
    if request.method == 'GET':
        return render_template('controle.html')
    elif request.method == 'POST':
        if not robot:
            return jsonify({'status': 'error', 'message': 'Robô não conectado.'}), 503

        x = request.form.get('x', 0, type=float)
        y = request.form.get('y', 0, type=float)
        z = request.form.get('z', 0, type=float)
        r = request.form.get('r', 0, type=float)

        try:
            robot.move(x, y, z, r)
            return jsonify({'status': 'success', 'message': 'Movimento realizado com sucesso.'})
        except Exception as e:
            logs_table.insert({'action': 'move', 'status': 'error', 'details': str(e)})
            return jsonify({'status': 'error', 'message': 'Erro ao mover o robô.'}), 500

@app.route('/connect')
def connect():
    try:
        ports = scanport()
        return render_template('connect.html', ports=ports)
    except Exception as e:
        return f"Erro ao buscar portas COM: {str(e)}", 500

@app.route('/attempt-connection', methods=['POST'])
def attempt_connection():
    selected_port = request.form.get('port')
    if not selected_port:
        return "Nenhuma porta selecionada", 400

    try:
        global robot
        robot = Robot(selected_port)
        return redirect('/control')
    except Exception as e:
        logs_table.insert({'action': 'connect', 'status': 'error', 'details': str(e)})
        ports = scanport()
        return render_template('connect.html', error=str(e), ports=ports)

if __name__ == '__main__':
    app.run(debug=True)
