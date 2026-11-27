from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from assistant import chat_with_ai
from weather import get_weather
app= FastAPI(title='"AI Personal Assistant"')

@app.get("/")
def home():
    return{
        "message": "Welcome to the AI Personal Assistant API!"
    }

@app.get("/health")
def health():
    return{
        "status": "healthy"
    }
@app.get("/weather")
def weather(city: str):

    result = get_weather(city)  # Define result first

    if "error" in result:
        raise HTTPException(
            status_code=404,
            detail=result["error"]
        )

    return result
class ChatRequest(BaseModel):
    message: str
    session_id: str


@app.post("/chat")
def chat(request: ChatRequest):

    answer = chat_with_ai(
        request.message,
        request.session_id
    )

    return {
        "question": request.message,
        "answer": answer,
        "session_id": request.session_id
    }