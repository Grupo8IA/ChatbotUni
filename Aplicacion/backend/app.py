from flask import Flask, render_template, request, json, jsonify
from bson import json_util,objectid
from datetime import datetime
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_bcrypt import Bcrypt
import time
from model import ejecutar, enviarEntrada

voc, encoder, decoder = ejecutar()
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
bcrypt = Bcrypt(app)

@app.route('/',methods=['POST'])
def sign_in():
    print("")

# ENVIAR MENSAJE
@socketio.on('send_message')
def handle_send_message_event(data):
    print("MENSAJE_SOCKET")
    cadena = enviarEntrada(data['message'], voc, encoder, decoder)
    respuesta = {
        "message": cadena,
        "roomId": data['roomId'],
        "sender": 1,
        "createdAt": time.strftime('%d-%m-%Y %H:%M:%S'),
    }
    emit('receive_message', respuesta, room=data['roomId'])

#UNIR LA SALA
@socketio.on('join_room')
def handle_join_room_event(data):
    print("UNIDO A LA SALA")
    print(data)
    join_room(data)

#DEJAR LA SALA
@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['roomId']))
    leave_room()

@socketio.on('connect')
def test_connect():
   print("CONNECTED")

@socketio.on('keep_alive')
def keep_alive():
   print("KEEPING ALIVE") 