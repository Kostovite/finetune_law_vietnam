import React, { useState } from 'react';
import { Box, TextField, IconButton, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop'; // Import Stop icon
import './WaveAnimation.css'; // Import custom CSS for wave animation

// Giả lập API speech-to-text
const fakeSpeechToTextAPI = (audioData) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve('This is the transcribed text of your voice.');
    }, 1000); // Giả lập độ trễ 1s
  });
};

// Giả lập khi có lỗi nhận diện giọng nói
const fakeErrorSpeechToTextAPI = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve('Sorry, I couldn\'t understand your voice. Please try again.');
    }, 1000); // Giả lập độ trễ 1s cho lỗi
  });
};

const MessageInput = ({ onSend }) => {
  const [message, setMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false); // Trạng thái đang chuyển đổi speech to text
  const [transcribedText, setTranscribedText] = useState('');
  const [isTextReceived, setIsTextReceived] = useState(false); // Để theo dõi khi văn bản được nhận

  // Cài đặt SpeechRecognition (API chuyển đổi giọng nói thành văn bản)
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = 'en-US';
  recognition.continuous = false;

  const handleSend = () => {
    if (message.trim()) {
      onSend(message.trim()); // Gửi tin nhắn
      setMessage(''); // Xóa message sau khi gửi
      setIsTextReceived(false); // Đặt trạng thái là chưa nhận được văn bản
    }
  };

  const handleMicClick = () => {
    setIsRecording((prev) => !prev);

    if (!isRecording) {
      // Bắt đầu ghi âm
      console.log('Recording started...');
      recognition.start(); // Bắt đầu ghi âm
    } else {
      // Dừng ghi âm
      console.log('Recording stopped...');
      recognition.stop(); // Dừng ghi âm
    }
  };

  // Xử lý kết quả ghi âm khi dừng
  recognition.onresult = async (event) => {
    const transcript = event.results[0][0].transcript;
    console.log('Transcript:', transcript);

    setIsTranscribing(true); // Bắt đầu quá trình chuyển đổi speech to text
    const text = await fakeSpeechToTextAPI(transcript); // Gọi API giả lập
    setIsTranscribing(false); // Kết thúc quá trình chuyển đổi
    setTranscribedText(text);
    setMessage(text); // Cập nhật lại message với văn bản đã chuyển đổi
    setIsTextReceived(true); // Đánh dấu là đã nhận được văn bản từ giọng nói
  };

  // Xử lý khi có lỗi trong quá trình nhận diện giọng nói
  recognition.onerror = async (event) => {
    console.error('Speech recognition error', event);
    setIsTranscribing(false);

    // Giả lập khi có lỗi
    const errorMessage = await fakeErrorSpeechToTextAPI();
    setTranscribedText(errorMessage);
    setMessage(errorMessage); // Hiển thị thông báo lỗi
    setIsTextReceived(true); // Đánh dấu là đã nhận được thông báo lỗi
  };

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        p: 1,
        borderTop: '1px solid #334155',
        backgroundColor: 'background.paper',
      }}
    >
      {isRecording ? (
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flex: 1,
          }}
        >
          <Box className="wave-animation">
            {/* Hiển thị nhiều cột sóng */}
            {Array.from({ length: 7 }).map((_, index) => (
              <Box key={index} className="wave-bar" />
            ))}
          </Box>
        </Box>
      ) : isTranscribing ? (
        // Hiển thị loading khi đang chuyển speech to text
        <CircularProgress size={24} color="primary" />
      ) : (
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type your message..."
          value={isTextReceived ? transcribedText : message} // Hiển thị transcribedText khi có kết quả hoặc message khi người dùng nhập
          onChange={(e) => {
            setMessage(e.target.value);
            setIsTextReceived(false); // Đặt lại trạng thái khi người dùng nhập văn bản
          }}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
      )}
      <IconButton onClick={handleMicClick} color={isRecording ? 'secondary' : 'primary'}>
        {isRecording ? <StopIcon /> : <MicIcon />}
      </IconButton>
      <IconButton onClick={handleSend} color="primary">
        <SendIcon />
      </IconButton>
    </Box>
  );
};

export default MessageInput;
