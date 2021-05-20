#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 22:52:57 2021

@author: gui
"""
import PySimpleGUI as sg
import socketio

uri = "http://0.0.0.0:9988"

sio = socketio.Client()

messages = []

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')
  
@sio.on('my response')
def on_message(data):
    print('I received a message! ', data)    
    messages.append(data)

@sio.event
def my_event(data):
    print('message Send with ', data)
    sio.emit('my_event', {'data': data})
    


layout = [
           [sg.Input(default_text = uri, key='-CON-'), sg.Button('Conect to', key='-BUTTONC-')],
           [sg.Input(disabled = True, key='-IN-'), sg.Button('Send Message', key='-BUTTONS-')],
           [sg.Input(disabled = True, key='-INB-'), sg.Button('Send Message Broad.', key='-BUTTONSB-')],
           [sg.Multiline('', disabled = True, size=(50,6),  key='-MULTIOUT-', font='Courier 12',  autoscroll = True)],
           [sg.Button('Disconnect',  key='-BUTTOND-'), sg.OK('Limpar', key='-CLEAR-', button_color=('white', 'red')) ]
        ]        
        

window = sg.Window('Socket GUI', layout)

while True:     # Event Loop
    
    if not len(messages) == 0:
        text = messages[0]
        window['-MULTIOUT-'].update(str(text) + '\n', text_color = 'black', append=True)
        messages.clear()
        
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED:
        break
    if event == '-BUTTONC-': #Connect
        text = values['-CON-']
        window['-MULTIOUT-'].update('Conect to '+str(text) + '\n', text_color = 'black', append=True)
        window['-CON-'].Update(disabled = True)
        window['-IN-'].Update(disabled = False)
        window['-INB-'].Update(disabled = False)
        window['-BUTTONC-'].Update(disabled = True)
        try:
            sio.connect(text)
        except socketio.exceptions.ConnectionError:
            window['-MULTIOUT-'].update(str('ConnectionError') + '\n', append=True)
    if event == '-BUTTOND-': #Disconnect
        window['-CON-'].Update(disabled = False)
        window['-IN-'].Update(disabled = True)
        window['-INB-'].Update(disabled = True)
        window['-BUTTONC-'].Update(disabled = False)
        window['-MULTIOUT-'].update('Disconnected'+ '\n', text_color = 'black', append=True)
        sio.disconnect()
    if event == '-BUTTONS-':#Send Message
        text = values['-IN-']
        #window['-MULTIOUT-'].update(str(text) + '\n', text_color = 'black', append=True)        
        sio.emit('my_event', {'data': str(text)})
    if event == '-BUTTONSB-':#Send broadcast messager
        text = values['-INB-']
        #window['-MULTIOUT-'].update(str(text) + '\n', text_color = 'black', append=True)        
        sio.emit('my broadcast event', {'data': str(text)})
    if event == '-CLEAR-':
        window['-MULTIOUT-'].update('')
        window['-IN-'].update('')
        window['-INB-'].update('')

window.close()

