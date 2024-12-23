import { useState } from "react";
import { Box, TextField, Button, Typography, Paper, Divider } from "@mui/material";

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSendMessage = async () => {
    if (input.trim() === "") return;

    // User message
    const userMessage = { text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);

    setInput("");

    // Simulate AI response
    const aiMessage = await getAIResponse(input);
    setMessages((prev) => [...prev, { text: aiMessage, sender: "ai" }]);
  };

  const getAIResponse = async (userInput) => {
    // Simulate API call to AI model (replace this with actual API call)
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(`AI Response to: "${userInput}"`);
      }, 1000);
    });
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      justifyContent="space-between"
      alignItems="center"
      height="100vh"
      bgcolor="background.default"
      padding={2}
    >
      {/* Header */}
      <Typography variant="h5" color="primary" gutterBottom>
        Chat with GPT
      </Typography>

      {/* Chat Box */}
      <Paper
        elevation={3}
        style={{
          flex: 1,
          width: "100%",
          maxWidth: 600,
          overflowY: "auto",
          marginBottom: 16,
          padding: 16,
        }}
      >
        {messages.map((message, index) => (
          <Box
            key={index}
            display="flex"
            justifyContent={message.sender === "user" ? "flex-end" : "flex-start"}
            marginY={1}
          >
            <Box
              component="span"
              padding={1.5}
              borderRadius={8}
              bgcolor={message.sender === "user" ? "primary.main" : "grey.300"}
              color={message.sender === "user" ? "white" : "black"}
              maxWidth="70%"
              wordBreak="break-word"
            >
              {message.text}
            </Box>
          </Box>
        ))}
      </Paper>

      {/* Input Box */}
      <Divider style={{ width: "100%", maxWidth: 600, marginBottom: 8 }} />
      <Box
        display="flex"
        alignItems="center"
        width="100%"
        maxWidth={600}
        padding={1}
      >
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === "Enter") handleSendMessage();
          }}
        />
        <Button
          variant="contained"
          color="primary"
          style={{ marginLeft: 8 }}
          onClick={handleSendMessage}
        >
          Send
        </Button>
      </Box>
    </Box>
  );
};

export default ChatPage;
