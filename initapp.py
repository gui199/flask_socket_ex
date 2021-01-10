from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

app = Flask(__name__, template_folder="./")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=True, engineio_logger=True)


@app.route('/')
def index():
    return render_template('initapp.html')

    
@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)    
    
@socketio.on('my response')
def handle_message2(data):
    print('received message2: ' + data)    
    
#@socketio.on('my event')
#def handle_message3(data):
#    print('received message2: ' + data['data'])   
#    emit('my response', {'data': data['data']})
    #emit('my response', {'data': 'got it!'}) 


@socketio.on('my broadcast event')
def test_messages(message):
    emit('my response', {'data': message['data']}, broadcast=True)
    print('received message2: ' + message['data'])  

#@socketio.on('message')
#def message_handler(msg):
#    send(msg)

"""Nome do Eventoo é o mesmo da função"""    
@socketio.event
def my_event(message):
#    emit('my response', {'data': 'got it!'})    
    print('my response: ' + message['data'])   
    emit('my response', {'data': message['data']})    

@socketio.on('sendMessage')
def send_message_handler(msg):
    emit('my chat', msg, broadcast=True)
    print(msg)  
    
    
@socketio.on('connect')
def test_connect():
    print('Client Connected')   
    #emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')    

#Flask-SocketIO also supports SocketIO namespaces, 
@socketio.on('my event', namespace='/test')
def handle_my_custom_namespace_event(json):
    print('received json: ' + str(json))    

def my_function_handler(data):
    pass

socketio.on_event('myevent', my_function_handler, namespace='/test1')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, port=9988)