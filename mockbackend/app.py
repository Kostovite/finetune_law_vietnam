from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import uvicorn

# Create an instance of FastAPI
app = FastAPI()

# Add CORS middleware to allow requests from localhost:5173
origins = [
    "http://localhost:5173",  # Allow React dev server to connect
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows only these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Define the request model
class MessageRequest(BaseModel):
    message: str

# Define a response model
class MessageResponse(BaseModel):
    message: str

# Define a mock AI response function
def get_mock_ai_response(user_message: str) -> str:
    # You can use any logic here for your mock response
    responses = [
        "Hello! How can I assist you today?",
        "I'm here to help you with your questions!",
        "Let's chat! What can I do for you?",
        "Tell me more about what you're looking for!"
    ]
    return random.choice(responses)

# Create an endpoint for receiving messages
@app.post("/send-message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    # Get the AI response based on the user input
    ai_response = get_mock_ai_response(request.message)
    return MessageResponse(message=ai_response)

# Run the app (this allows the script to run with 'python app.py')
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
