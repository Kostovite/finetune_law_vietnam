import { useState } from 'react';
import MessageBubble from './components/MessageBubble';
import MessageInput from './components/MessageInput';
import theme from '../../theme/theme';
import {
  Box,
  Paper,
  ThemeProvider,
} from "@mui/material";
import axios from "axios";

const ChatPage = () => {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Chào mừng! Tôi có thể giúp gì cho bạn?', sourceDocuments: [] },
  ]);

  const handleSendMessage = async (message) => {
    if (!message || message.trim() === "") return;

    // User message
    const userMessage = { sender: "user", text: message };
    setMessages((prev) => [...prev, userMessage]);

    // Call API
    try {
      const aiMessage = await getAIResponse(message);
      console.log("aiMessage", aiMessage);
      if (aiMessage) {

        const uniqueDocuments = aiMessage.source_documents.filter(
          (doc, index, self) =>
            index === self.findIndex((d) => d.metadata.id === doc.metadata.id)
        );

        const filteredDocuments = uniqueDocuments.filter((doc, _, allDocs) => {
          const { article, clause } = doc.metadata;

          // Kiểm tra nếu clause chỉ chứa số
          if (/^\d+$/.test(clause)) {
            // Tìm các mục trùng article và clause dạng "1a", "1b", ...
            const relatedClauses = allDocs.filter(otherDoc => {
              return (
                otherDoc.metadata.article === article &&
                new RegExp(`^${clause}[a-zA-Z]$`).test(otherDoc.metadata.clause)
              );
            });

            // Nếu tồn tại các clause dạng "1a", "1b", ... thì loại bỏ clause chỉ chứa số
            if (relatedClauses.length > 0) {
              return false;
            }
          }

          // Giữ lại nếu không thuộc trường hợp trên
          return true;
        });

        console.log(uniqueDocuments);
        setMessages((prev) => [
          ...prev,
          { sender: "ai", text: aiMessage.answer, sourceDocuments: filteredDocuments },
        ]);
      } else {
        // Fallback for cases where the AI doesn't return a valid response
        setMessages((prev) => [
          ...prev,
          { sender: "bot", text: "Đây là câu trả lời mẫu." },
        ]);
      }
    } catch (error) {
      console.error("Error while fetching AI response:", error);
      // Handle API errors gracefully
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Đã xảy ra lỗi, vui lòng thử lại sau." },
      ]);
    }
  };


  const getAIResponse = async (userInput) => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:1111/send-message",
        { message: userInput },
        { headers: { "Content-Type": "application/json" } }
      );
      return response.data;
    } catch (error) {
      console.error("Error:", error);
      return null;
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <Box
        sx={{
          width: '100%',
          height: '100vh',
          display: 'flex',
          flexDirection: 'column',
          backgroundColor: theme.palette.background.default,
        }}
      >
        <Paper
          elevation={3}
          sx={{
            flex: 1,
            overflowY: 'auto',
            padding: 2,
            backgroundColor: theme.palette.background.paper,
          }}
        >
          {messages.map((msg, index) => (
            <MessageBubble key={index} sender={msg.sender} text={msg.text} sourceDocuments={msg.sourceDocuments} />
          ))}
        </Paper>
        <MessageInput onSend={handleSendMessage} />
      </Box>
    </ThemeProvider>
  );
};

export default ChatPage;
