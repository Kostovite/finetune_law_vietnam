import { useState } from "react";
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  Divider,
  Link,
  Dialog,
  DialogTitle,
  DialogContent,
} from "@mui/material";
import axios from "axios";
import law52 from '../../utils/law/Luật-52-2014-QH13.json';
import law91 from '../../utils/law/Bộ luật-91-2015-QH13.json';


const jsonFile = {
  "Bộ luật-91-2015-QH13" : law91,
  "Luật-52-2014-QH13": law52
}

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [popupContent, setPopupContent] = useState(null);
  const [isPopupOpen, setIsPopupOpen] = useState(false);

  const handleSendMessage = async () => {
    if (input.trim() === "") return;

    // User message
    const userMessage = { text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    // Call API
    const aiMessage = await getAIResponse(input);
    if (aiMessage) {
      setMessages((prev) => [
        ...prev,
        { text: aiMessage.answer, sender: "ai", sourceDocuments: aiMessage.source_documents },
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

  const fetchDocumentContent = async (data) => {
    try {
      // const a = await axios.get(`../../utils/law/${fileId}.json`);
      // console.log(a);
      // const lawContenta = a.data[article];
      // console.log(lawContenta); 
      // const response = await import(`../../utils/law/${fileId}.json`);

      const content = data["content"]
      const metadata = data["metadata"]
      console.log("content", content)
      console.log("metadata", metadata)

      const currentLaw = jsonFile[metadata.file_id]
      console.log(currentLaw)

      const articleContent = currentLaw.content.find(
        (item) => item.id === metadata.article
      )

      console.log(articleContent)

      
      // console.log(fileId)
      // const law = jsonFile[fileId]
      // console.log(law)
      // console.log(law52["content"])
      // console.log(article)

      // const articleContent = law.content.find(
      //   (item) => item.id === article
      // );
      // console.log(articleContent)
      // console.log(articleContent.title)
      
      setPopupContent(articleContent.title || "No content found.");
      setIsPopupOpen(true);
    } catch (error) {
      console.error("Error fetching law content:", error);
      setPopupContent("Failed to load content.");
      setIsPopupOpen(true);
    }
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
          <Box key={index} marginBottom={2}>
            {/* Display User or AI Message */}
            <Typography
              style={{
                color: message.sender === "user" ? "primary.main" : "black",
                fontWeight: message.sender === "user" ? "bold" : "normal",
              }}
            >
              {message.text}
            </Typography>

            {/* Display Source Documents */}
            {message.sender === "ai" &&
              message.sourceDocuments &&
              message.sourceDocuments.map((doc, i) => (
                <Box key={i} marginTop={1}>
                  <Link
                    href="#"
                    onClick={(e) => {
                      e.preventDefault();
                      fetchDocumentContent(doc);
                    }}
                  >
                    {doc.metadata.title}
                  </Link>
                </Box>
              ))}
          </Box>
        ))}
      </Paper>

      {/* Input Box */}
      <Divider style={{ width: "100%", maxWidth: 600, marginBottom: 8 }} />
      <Box display="flex" alignItems="center" width="100%" maxWidth={600} padding={1}>
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
        <Button variant="contained" color="primary" style={{ marginLeft: 8 }} onClick={handleSendMessage}>
          Send
        </Button>
      </Box>

      {/* Popup Dialog */}
      <Dialog open={isPopupOpen} onClose={() => setIsPopupOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Law Document Content</DialogTitle>
        <DialogContent>
          <Typography>{popupContent}</Typography>
        </DialogContent>
      </Dialog>
    </Box>
  );
};

export default ChatPage;
