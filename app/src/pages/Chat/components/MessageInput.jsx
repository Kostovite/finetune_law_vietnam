import { useState, useRef } from 'react'; 
import axios from 'axios';
import { Box, TextField, IconButton, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';

const MessageInput = ({ onSend }) => {
  const [message, setMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [audioFilePath] = useState(null); // Audio file URL for playback
  const [isTranscribing, setIsTranscribing] = useState(false); // Track transcription state
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const MAX_ATTEMPTS = 15; // Maximum number of attempts for retry
  const RETRY_DELAY = 5000; // Delay between retry attempts in milliseconds

  const handleSend = () => {
    if (message.trim()) {
      onSend(message.trim());
      console.log('Message sent:', message.trim()); // Log sent message
      setMessage('');
    }
  };

  const handleMicClick = () => {
    console.log(`Mic button clicked. Is recording: ${isRecording}`);
    if (!isRecording) {
      startRecording();
    } else {
      stopRecording();
    }
    setIsRecording(!isRecording);
  };

  const startRecording = async () => {
    try {
      console.log('Attempting to start recording...');
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];
      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      mediaRecorderRef.current.start();
      console.log('Recording started');
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  };

  const stopRecording = () => {
    console.log('Stopping recording...');
    mediaRecorderRef.current.stop();
    mediaRecorderRef.current.onstop = async () => {
      console.log('Recording stopped');
      const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });

      // Set transcription state to true while waiting for the result
      setIsTranscribing(true);

      // Send the audio file to the FPT.AI API for transcription
      await sendToFPTAI(audioBlob);
    };
  };

  const sendToFPTAI = async (audioBlob) => {
    console.log('Sending audio to FPT.AI API...');
    for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
      try {
        console.log(`Attempting to send request... (Attempt: ${attempt}/${MAX_ATTEMPTS})`);
        const response = await axios.post(
          'https://api.fpt.ai/hmi/asr/general',
          audioBlob, // Send Blob directly
          {
            headers: {
              'Content-Type': 'application/octet-stream', // Binary format
              'api-key': 'wCFtqM0KKl1flQTuJ1iZwuIL9UwTxql4', 
            },
          }
        );

        console.log('Response from FPT.AI:', response);

        const { status, hypotheses, message } = response.data;
        console.log('API response data:', response.data);

        if (status === 0 && hypotheses && hypotheses.length > 0) {
          console.log('Transcription result:', hypotheses[0].utterance);

          setMessage(hypotheses[0].utterance); // Set message to the transcribed text

          // Set transcription state to false as the result is received
          setIsTranscribing(false);

          return;
        } else if (status === 1) {
          console.log('Error: No speech detected.');
        } else if (status === 2) {
          console.log('Error: Request was canceled.');
        } else if (status === 9) {
          console.log('System is busy. Retrying...');
        } else {
          console.log(`Unexpected error: ${message || 'No details.'}`);
        }
      } catch (error) {
        console.log('Network error or request failed:', error.message);
      }

      // Wait before retrying
      if (attempt < MAX_ATTEMPTS) {
        console.log(`Waiting 5 seconds before retrying...`);
        await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
      } else {
        console.log('Max attempts reached. Unable to process the request.');
      }
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        p: 1,
        borderTop: '1px solid #334155',
        backgroundColor: 'background.paper',
        flexDirection: 'column',
      }}
    >
      <Box sx={{ display: 'flex', width: '100%' }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <IconButton onClick={handleMicClick} color={isRecording ? 'secondary' : 'primary'}>
          {isRecording ? (
            <StopIcon />
          ) : isTranscribing ? (
            <CircularProgress size={24} color="primary" />
          ) : (
            <MicIcon />
          )}
        </IconButton>
        <IconButton onClick={handleSend} color="primary">
          <SendIcon />
        </IconButton>
      </Box>
      {audioFilePath && (
        <Box sx={{ mt: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
          <audio controls autoPlay src={audioFilePath}>
            Your browser does not support the audio element.
          </audio>
        </Box>
      )}
    </Box>
  );
};

export default MessageInput;
