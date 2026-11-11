"""Importaciones de FastAPI"""
from fastapi import FastAPI, WebSocket
# FastAPI: permite crear nuestra aplicación, como ya conocemos.
# WebSocket: representa la conexión WebSocket establecida con un cliente.

app=FastAPI()

# declaramos una ruta del websocket
@app.websocket("/ws/echo")
async def websocket_echo(websocket: WebSocket): # funci. asincrona porque la respuesta no depende de nosotros
    """Función que maneja los websockets"""
    # Hacemos handshake:
    await websocket.accept() # aceptamos conexión del websocket
    
    while True: # abrimos canal de comunicación_  ciclo infinito mientras tenemos abierta la sesión. No sabemos cuánto va a durar
        data = await websocket.receive_text() 
        # esperamos texto del lado del cliente
        await websocket.send_text(f"Echo: {data}")
        # Preparamos respuesta del lado del servidor.  si un cliente me envñía un mensaje, le respondo 
        # con su mismo mensaje pero con prefijo echo