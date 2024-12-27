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
class SourceDocument(BaseModel):
    content: str
    metadata: dict

class MessageResponse(BaseModel):
    answer: str
    source_documents: list[SourceDocument]

# Define a mock AI response function
def get_mock_ai_response(user_message: str) -> dict:
    # Mock AI response
    answer = "This is a mock answer to your question."

    # Mock source documents
    source_documents = [
        {
            "content": "Cơ quan quản lý nhà nước về trẻ em;",
            "metadata": {
                "article": "Điều 10",
                "clause": "2c",
                "file_id": "52-2014-QH13",
                "id": "Điều 10.2c",
                "title": "Người có quyền yêu cầu hủy việc kết hôn trái pháp luật"
            }
        },
        {
            "content": "Cơ quan quản lý nhà nước về trẻ em;",
            "metadata": {
                "article": "Điều 84",
                "clause": "5c",
                "file_id": "52-2014-QH13",
                "id": "Điều 84.5c",
                "title": "Thay đổi người trực tiếp nuôi con sau khi ly hôn"
            }
        }
    ]

    return {"answer": answer, "source_documents": source_documents}

# Create an endpoint for receiving messages
@app.post("/send-message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    # Get the AI response based on the user input
    ai_response = get_mock_ai_response(request.message)
    return MessageResponse(**ai_response)

# Run the app (this allows the script to run with 'python app.py')
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=1111)