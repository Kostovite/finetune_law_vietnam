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
    answer = "Trẻ em là người tuyệt vời nhất thế giới."

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

    # return {"answer": answer, "source_documents": source_documents}

    return {
  "answer": "Con ở với mẹ hoặc cha tùy theo thỏa thuận của ba mẹ.",
  "source_documents": [
    {
      "content": "Đối với hợp đồng đơn vụ, bên có nghĩa vụ phải thực hiện nghĩa vụ đúng như đã thoả thuận, chỉ được thực hiện trước hoặc sau thời hạn nếu được bên có quyền đồng ý.",
      "metadata": {
        "article": "Điều 409",
        "clause": "0",
        "file_id": "91-2015-QH13",
        "id": "Điều 409.0",
        "title": "Thực hiện hợp đồng đơn vụ"
      }
    },
    {
      "content": "Đối với hợp đồng vay có kỳ hạn và không có lãi thì bên vay có quyền trả lại tài sản bất cứ lúc nào, nhưng phải báo trước cho bên cho vay một thời gian hợp lý, còn bên cho vay chỉ được đòi lại tài sản trước kỳ hạn, nếu được bên vay đồng ý.",
      "metadata": {
        "article": "Điều 470",
        "clause": "1",
        "file_id": "91-2015-QH13",
        "id": "Điều 470.1",
        "title": "Thực hiện hợp đồng vay có kỳ hạn"
      }
    },
    {
      "content": "Đối với hợp đồng vay có kỳ hạn và có lãi thì bên vay có quyền trả lại tài sản trước kỳ hạn, nhưng phải trả toàn bộ lãi theo kỳ hạn, trừ trường hợp có thoả thuận khác hoặc luật có quy định khác.",
      "metadata": {
        "article": "Điều 470",
        "clause": "2",
        "file_id": "91-2015-QH13",
        "id": "Điều 470.2",
        "title": "Thực hiện hợp đồng vay có kỳ hạn"
      }
    },
    {
      "content": "Theo yêu cầu của người có quyền, lợi ích liên quan, Tòa án giao tài sản của người vắng mặt tại nơi cư trú cho người sau đây quản lý:",
      "metadata": {
        "article": "Điều 65",
        "clause": "1",
        "file_id": "91-2015-QH13",
        "id": "Điều 65.1",
        "title": "Quản lý tài sản của người vắng mặt tại nơi cư trú"
      }
    },
    {
      "content": "Đối với tài sản đã được người vắng mặt uỷ quyền quản lý thì người được uỷ quyền tiếp tục quản lý;",
      "metadata": {
        "article": "Điều 65",
        "clause": "1a",
        "file_id": "91-2015-QH13",
        "id": "Điều 65.1a",
        "title": "Quản lý tài sản của người vắng mặt tại nơi cư trú"
      }
    },
    {
      "content": "Đối với tài sản chung thì do chủ sở hữu chung còn lại quản lý;",
      "metadata": {
        "article": "Điều 65",
        "clause": "1b",
        "file_id": "91-2015-QH13",
        "id": "Điều 65.1b",
        "title": "Quản lý tài sản của người vắng mặt tại nơi cư trú"
      }
    },
    {
      "content": "Đối với tài sản do vợ hoặc chồng đang quản lý thì vợ hoặc chồng tiếp tục quản lý; nếu vợ hoặc chồng chết hoặc mất năng lực hành vi dân sự, có khó khăn trong nhận thức, làm chủ hành vi, bị hạn chế năng lực hành vi dân sự thì con thành niên hoặc cha, mẹ của người vắng mặt quản lý.",
      "metadata": {
        "article": "Điều 65",
        "clause": "1c",
        "file_id": "91-2015-QH13",
        "id": "Điều 65.1c",
        "title": "Quản lý tài sản của người vắng mặt tại nơi cư trú"
      }
    },
    {
      "content": "Trường hợp không có những người được quy định tại khoản 1 Điều này thì Tòa án chỉ định một người trong số những người thân thích của người vắng mặt tại nơi cư trú quản lý tài sản; nếu không có người thân thích thì Tòa án chỉ định người khác quản lý tài sản.",
      "metadata": {
        "article": "Điều 65",
        "clause": "2",
        "file_id": "91-2015-QH13",
        "id": "Điều 65.2",
        "title": "Quản lý tài sản của người vắng mặt tại nơi cư trú"
      }
    },
    {
      "content": "Đối với hợp đồng vay có kỳ hạn và không có lãi thì bên vay có quyền trả lại tài sản bất cứ lúc nào, nhưng phải báo trước cho bên cho vay một thời gian hợp lý, còn bên cho vay chỉ được đòi lại tài sản trước kỳ hạn, nếu được bên vay đồng ý.",
      "metadata": {
        "article": "Điều 470",
        "clause": "1",
        "file_id": "91-2015-QH13",
        "id": "Điều 470.1",
        "title": "Thực hiện hợp đồng vay có kỳ hạn"
      }
    },
    {
      "content": "Đối với hợp đồng vay có kỳ hạn và có lãi thì bên vay có quyền trả lại tài sản trước kỳ hạn, nhưng phải trả toàn bộ lãi theo kỳ hạn, trừ trường hợp có thoả thuận khác hoặc luật có quy định khác.",
      "metadata": {
        "article": "Điều 470",
        "clause": "2",
        "file_id": "91-2015-QH13",
        "id": "Điều 470.2",
        "title": "Thực hiện hợp đồng vay có kỳ hạn"
      }
    },
    {
      "content": "Đối với hợp đồng vay có kỳ hạn và không có lãi thì bên vay có quyền trả lại tài sản bất cứ lúc nào, nhưng phải báo trước cho bên cho vay một thời gian hợp lý, còn bên cho vay chỉ được đòi lại tài sản trước kỳ hạn, nếu được bên vay đồng ý.",
      "metadata": {
        "article": "Điều 470",
        "clause": "1",
        "file_id": "91-2015-QH13",
        "id": "Điều 470.1",
        "title": "Thực hiện hợp đồng vay có kỳ hạn"
      }
    },
    {
      "content": "Đối với hợp đồng vay có kỳ hạn và có lãi thì bên vay có quyền trả lại tài sản trước kỳ hạn, nhưng phải trả toàn bộ lãi theo kỳ hạn, trừ trường hợp có thoả thuận khác hoặc luật có quy định khác.",
      "metadata": {
        "article": "Điều 470",
        "clause": "2",
        "file_id": "91-2015-QH13",
        "id": "Điều 470.2",
        "title": "Thực hiện hợp đồng vay có kỳ hạn"
      }
    },
    {
      "content": "Đối với hợp đồng vay có kỳ hạn và không có lãi thì bên vay có quyền trả lại tài sản bất cứ lúc nào, nhưng phải báo trước cho bên cho vay một thời gian hợp lý, còn bên cho vay chỉ được đòi lại tài sản trước kỳ hạn, nếu được bên vay đồng ý.",
      "metadata": {
        "article": "Điều 470",
        "clause": "1",
        "file_id": "91-2015-QH13",
        "id": "Điều 470.1",
        "title": "Thực hiện hợp đồng vay có kỳ hạn"
      }
    },
    {
      "content": "Đối với hợp đồng vay có kỳ hạn và có lãi thì bên vay có quyền trả lại tài sản trước kỳ hạn, nhưng phải trả toàn bộ lãi theo kỳ hạn, trừ trường hợp có thoả thuận khác hoặc luật có quy định khác.",
      "metadata": {
        "article": "Điều 470",
        "clause": "2",
        "file_id": "91-2015-QH13",
        "id": "Điều 470.2",
        "title": "Thực hiện hợp đồng vay có kỳ hạn"
      }
    },
    {
      "content": "Đối với hợp đồng vay có kỳ hạn và không có lãi thì bên vay có quyền trả lại tài sản bất cứ lúc nào, nhưng phải báo trước cho bên cho vay một thời gian hợp lý, còn bên cho vay chỉ được đòi lại tài sản trước kỳ hạn, nếu được bên vay đồng ý.",
      "metadata": {
        "article": "Điều 470",
        "clause": "1",
        "file_id": "91-2015-QH13",
        "id": "Điều 470.1",
        "title": "Thực hiện hợp đồng vay có kỳ hạn"
      }
    },
    {
      "content": "Đối với hợp đồng vay có kỳ hạn và có lãi thì bên vay có quyền trả lại tài sản trước kỳ hạn, nhưng phải trả toàn bộ lãi theo kỳ hạn, trừ trường hợp có thoả thuận khác hoặc luật có quy định khác.",
      "metadata": {
        "article": "Điều 470",
        "clause": "2",
        "file_id": "91-2015-QH13",
        "id": "Điều 470.2",
        "title": "Thực hiện hợp đồng vay có kỳ hạn"
      }
    },
    {
      "content": "Đối với hợp đồng vay có kỳ hạn và không có lãi thì bên vay có quyền trả lại tài sản bất cứ lúc nào, nhưng phải báo trước cho bên cho vay một thời gian hợp lý, còn bên cho vay chỉ được đòi lại tài sản trước kỳ hạn, nếu được bên vay đồng ý.",
      "metadata": {
        "article": "Điều 470",
        "clause": "1",
        "file_id": "91-2015-QH13",
        "id": "Điều 470.1",
        "title": "Thực hiện hợp đồng vay có kỳ hạn"
      }
    },
    {
      "content": "Đối với hợp đồng vay có kỳ hạn và có lãi thì bên vay có quyền trả lại tài sản trước kỳ hạn, nhưng phải trả toàn bộ lãi theo kỳ hạn, trừ trường hợp có thoả thuận khác hoặc luật có quy định khác.",
      "metadata": {
        "article": "Điều 470",
        "clause": "2",
        "file_id": "91-2015-QH13",
        "id": "Điều 470.2",
        "title": "Thực hiện hợp đồng vay có kỳ hạn"
      }
    },
    {
      "content": "Đối với hợp đồng vay có kỳ hạn và không có lãi thì bên vay có quyền trả lại tài sản bất cứ lúc nào, nhưng phải báo trước cho bên cho vay một thời gian hợp lý, còn bên cho vay chỉ được đòi lại tài sản trước kỳ hạn, nếu được bên vay đồng ý.",
      "metadata": {
        "article": "Điều 470",
        "clause": "1",
        "file_id": "91-2015-QH13",
        "id": "Điều 470.1",
        "title": "Thực hiện hợp đồng vay có kỳ hạn"
      }
    },
    {
      "content": "Đối với hợp đồng vay có kỳ hạn và có lãi thì bên vay có quyền trả lại tài sản trước kỳ hạn, nhưng phải trả toàn bộ lãi theo kỳ hạn, trừ trường hợp có thoả thuận khác hoặc luật có quy định khác.",
      "metadata": {
        "article": "Điều 470",
        "clause": "2",
        "file_id": "91-2015-QH13",
        "id": "Điều 470.2",
        "title": "Thực hiện hợp đồng vay có kỳ hạn"
      }
    }
  ]
}

# Create an endpoint for receiving messages
@app.post("/send-message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    # Get the AI response based on the user input
    ai_response = get_mock_ai_response(request.message)
    return MessageResponse(**ai_response)

# Run the app (this allows the script to run with 'python app.py')
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=1111)