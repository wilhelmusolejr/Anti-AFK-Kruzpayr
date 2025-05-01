# server.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import uvicorn

app = FastAPI()
bot_states: Dict[str, str] = {}

class BotStatus(BaseModel):
    bot_id: str
    state: str

@app.post("/update")
def update_status(status: BotStatus):
    bot_states[status.bot_id] = status.state
    return {"message": "✅ Status updated", "current": bot_states}

@app.get("/status")
def get_status():
    return bot_states

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
