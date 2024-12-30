import { useState } from 'react';
import MessageBubble from './MessageBubble';
import MessageInput from './MessageInput';
import theme from '../../theme/theme';
import {
  Box,
  Paper,
  ThemeProvider,
} from "@mui/material";
import axios from "axios";

const ChatPage = () => {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Chào mừng! Tôi có thể giúp gì cho bạn?' },
  ]);

  const handleSendMessage = async (message) => {
    if (!message || message.trim() === "") return;
  
    // User message
    const userMessage = { sender: "user", text: message };
    setMessages((prev) => [...prev, userMessage]);
  
    // Call API
    try {
      const aiMessage = await getAIResponse(message);
      if (aiMessage) {
        setMessages((prev) => [
          ...prev,
          { sender: "ai", text: aiMessage.answer, sourceDocuments: aiMessage.source_documents },
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
            <MessageBubble key={index} sender={msg.sender} text={msg.text} />
          ))}
        </Paper>
        <MessageInput onSend={handleSendMessage} />
      </Box>
    </ThemeProvider>
  );
};

export default ChatPage;
