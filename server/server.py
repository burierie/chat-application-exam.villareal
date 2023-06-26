import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:19006"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Store the active rooms
chatRooms = {}

@app.websocket("/ws/{roomName}")
async def websocket_endpoint(websocket: WebSocket, roomName: str):
    await websocket.accept()

    room = chatRooms.get(roomName)
    if room is None:
        return JSONResponse({"message": "Room does not exist"}, status_code=404)

    room["participants"].add(websocket)
    await broadcast_message(roomName, "A user joined the room")

    try:
        while True:
            message = await websocket.receive_text()
            await broadcast_message(roomName, message)
    finally:
        room["participants"].remove(websocket)
        await broadcast_message(roomName, "A user left the room")


async def broadcast_message(roomName: str, message: str):
    room = chatRooms.get(roomName)
    if room is None:
        return

    for participant in room["participants"]:
        await participant.send_text(message)


@app.post("/create_room/{roomName}")
async def create_room(roomName: str):
    if not roomName:
        return JSONResponse({"message": "Room ID cannot be empty"}, status_code=400)

    if roomName in chatRooms:
        return JSONResponse({"message": "Room already exists"}, status_code=400)

    chatRooms[roomName] = {"participants": set()}
    return {"message": "Room created.."}

@app.post("/join_room/{roomName}")
async def join_room(roomName: str):
    if not roomName:
        return JSONResponse({"message": "Room ID cannot be empty"}, status_code=400)

    room = chatRooms[roomName]
    if room is None:
        return JSONResponse({"message": "Room does not exist"}, status_code=404)
    
    room["participants"].add("New Participant")
    return {"message": "Joined the room"}

@app.get("/")
async def index():
    return {"message": "Welcome to the chat room API"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 