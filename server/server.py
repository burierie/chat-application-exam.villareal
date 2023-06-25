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
rooms = {}


@app.websocket("/ws/{roomname}")
async def websocket_endpoint(websocket: WebSocket, roomname: str, user_id: str):
    await websocket.accept()

    room = rooms.get(roomname)
    if room is None:
        return JSONResponse({"message": "Room does not exist"}, status_code=404)

    room["participants"].add(websocket)
    await broadcast_message(roomname, f"User {user_id} joined the room")

    try:
        while True:
            message = await websocket.receive_text()
            await broadcast_message(roomname, f"User {user_id}: {message}")
    finally:
        room["participants"].remove(websocket)
        await broadcast_message(roomname, f"User {user_id} left the room")


async def broadcast_message(roomname: str, message: str):
    room = rooms.get(roomname)
    if room is None:
        return

    for participant in room["participants"]:
        await participant.send_text(message)


@app.post("/create_room/{roomname}")
async def create_room(roomname: str):
    if roomname in rooms:
        return JSONResponse({"message": "Room already exists"}, status_code=400)

    rooms[roomname] = {"participants": set()}
    return {"message": "Room created"}

@app.post("/join_room/{roomname}")
async def join_room(roomname: str):
    room = rooms.get(roomname)
    if room is None:
        return JSONResponse({"message": "Room does not exist"}, status_code=404)

    room["participants"].add("New Participant")  # Replace "New Participant" with the actual participant you want to add

    return {"message": "Joined the room"}


@app.get("/")
async def index():
    return {"message": "Welcome to the chat room API"}


if __name__ == "_main_":
    uvicorn.run(app, host="0.0.0.0", port=8000)