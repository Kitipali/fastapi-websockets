from typing import Dict

from fastapi import FastAPI,WebSocket, WebSocketDisconnect

app = FastAPI()

class ConnectionManager:
    """Clase para administrar conexiones"""
    def __init__(self):
        self.active_connections: Dict[WebSocket, str] = {}
        # Inicializamos un diccionario de Web Socket
    async def connect(self, websocket: WebSocket, username: str):
        """Método para conexión"""
        await websocket.accept()
        # acepta la conexión
        self.active_connections[websocket] = username
        # Registra al usuario en el diccionario.
        await self.broadcast(f"🔵{username} se ha conectado")
        # Comunica a todos los usuarios que alguien se ha conectado.
        
    async def disconnect(self, websocket: WebSocket):
        """Método para desconexión"""
        username = self.active_connections.get(websocket, "Usuario")
        # get(websocket, "Usuario") recupera el nombre asociado a la conexión. Si no existe, devuelve "Usuario".
        self.active_connections.pop(websocket, None)
        # pop(websocket, None) elimina esa conexión del diccionario. El None evita un error si la clave no existe.
        await self.broadcast(f"🔴{username} se ha desconectado")
        # informa a los usuarios restantes de la desconexión.
    async def broadcast(self, message: str):
        """Método que envía mensajes a todos"""
        for connection in list(self.active_connections.keys()):
            await connection.send_text(message)
            # Recorre todas las conexiones registradas y envía el mismo mensaje a cada una.
            
            
manager = ConnectionManager()
# Creamos una instancia global de ConnectionManager


# El endpoint del chat

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket, username: str):
    """Maneja la conexión individual en un usuario"""
    # ws://.../ws/chat?username=Ricardo
    await manager.connect(websocket, username)
    
    try:
        while True:
            data = await websocket.receive_text()
            # mientras la conexión esté activa vamos a recibir mensajes de texto
            
            await manager.broadcast(f"{username}: {data}")
    
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    
    
    

