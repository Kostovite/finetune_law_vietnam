import React, { useState } from 'react';
import { Box, Paper, Typography, ThemeProvider } from '@mui/material';
import MessageBubble from './MessageBubble';
import MessageInput from './MessageInput';
import theme from '../../theme/theme';

const ChatWindow = () => {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Chào mừng! Tôi có thể giúp gì cho bạn?' },
  ]);

  const handleSendMessage = (message) => {
    setMessages([...messages, { sender: 'user', text: message }]);
    setTimeout(() => {
      setMessages((prev) => [...prev, { sender: 'bot', text: 'Đây là câu trả lời mẫu.' }]);
    }, 1000);
  };

  return (
    <ThemeProvider theme={theme}> {/* Sử dụng ThemeProvider để áp dụng theme */}
      <Box
        sx={{
          width: '100%',
          height: '100vh',
          display: 'flex',
          flexDirection: 'column',
          backgroundColor: theme.palette.background.default,
        }}
      >
        {/* <Box
          sx={{
            padding: 3,
            backgroundColor: 'linear-gradient(145deg, #60A5FA, #3B82F6)', // Gradient màu sắc mới
            color: '#FFFFFF', // Màu chữ trắng để tương phản tốt với nền gradient
            textAlign: 'center',
            borderRadius: '10px', // Thêm bo góc để mềm mại hơn
            boxShadow: '0 4px 10px rgba(0, 0, 0, 0.2)', // Thêm bóng đổ cho tiêu đề
          }}
        >
          <Typography
            variant="h3"
            component="h1"
            sx={{
              fontFamily: "'Poppins', sans-serif", // Sử dụng font Poppins cho tiêu đề
              fontWeight: '600', // Kiểu chữ đậm
              letterSpacing: '1px', // Thêm khoảng cách giữa các chữ
              textTransform: 'uppercase', // Chữ hoa cho tiêu đề
            }}
          >
            Lawwise
          </Typography>
        </Box> */}


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

export default ChatWindow;
