import { useState, useEffect } from 'react';
import { Box, Typography, IconButton, CircularProgress } from '@mui/material';
import VolumeUpIcon from '@mui/icons-material/VolumeUp'; 
import StopIcon from '@mui/icons-material/Stop';

const MessageBubble = ({ sender, text }) => {
    const [isSpeaking, setIsSpeaking] = useState(false); // Trạng thái đang phát âm thanh
    const [isLoading, setIsLoading] = useState(false); // Trạng thái loading khi gọi API
    const [audioUrl, setAudioUrl] = useState(null); // Lưu URL của file âm thanh
    const [audio, setAudio] = useState(null); // Lưu đối tượng Audio để dừng âm thanh
    const isUser = sender === 'user';

    // Gửi request khi có text
    useEffect(() => {
        if (text && !audioUrl) {
            handleGenerateAudio();
        }
    }, [text]); // Gửi request khi text thay đổi

    // Xử lý phát âm thanh khi nhấn vào volume
    const handlePlayAudio = async () => {
        if (audioUrl) {
            // Nếu đã có URL file âm thanh, chỉ phát lại
            const newAudio = new Audio(audioUrl);
            newAudio.play().catch((error) => {
                console.error('Không thể phát âm thanh:', error);
                alert('Tệp âm thanh không hợp lệ hoặc không thể phát.');
            });
            setAudio(newAudio); // Lưu đối tượng audio vào state
            setIsSpeaking(true);
            newAudio.onended = () => setIsSpeaking(false);
            return;
        }
        alert('Đang tải âm thanh...');
    };

    // Gửi request API để tạo âm thanh
    const handleGenerateAudio = async () => {
        try {
            setIsLoading(true); // Hiển thị trạng thái loading

            // Nội dung yêu cầu
            const requestBody = text; 
            const requestHeaders = {
                'api_key': 'ySSVUvXbKu86OlgU8fMg4Ine0sbynFmf', // API Key của bạn
                'voice': 'leminh', // Giọng nói
                'speed': '1', // Tốc độ nói
                'Content-Type': 'application/json', // Nội dung dạng JSON
            };

            // Ghi log nội dung yêu cầu
            console.log('Nội dung gửi đi:', {
                url: 'https://api.fpt.ai/hmi/tts/v5',
                method: 'POST',
                headers: requestHeaders,
                body: requestBody,
            });

            // Gửi yêu cầu đến API FPT.AI
            const response = await fetch('https://api.fpt.ai/hmi/tts/v5', {
                method: 'POST',
                headers: requestHeaders,
                body: requestBody,
            });

            const result = await response.json(); // Phản hồi là JSON
            console.log('Phản hồi API:', result); // Ghi log để kiểm tra phản hồi

            if (response.ok && result.error === 0 && result.async) {
                // URL file âm thanh đã sẵn sàng
                setAudioUrl(result.async);
            } else if (result.message.includes('The content will be returned')) {
                // Nếu file âm thanh chưa sẵn sàng, cần chờ và thử lại
                const audioUrl = await waitForAudio(result.async);
                if (audioUrl) {
                    setAudioUrl(audioUrl);
                } else {
                    alert('Không thể tải file âm thanh sau khi chờ.');
                }
            } else {
                console.error('API không trả về URL hợp lệ:', result);
                alert('API không trả về URL hợp lệ.');
            }
        } catch (error) {
            console.error('Lỗi khi gọi API FPT.AI:', error);
            alert('Đã xảy ra lỗi khi gọi API FPT.AI.');
        } finally {
            setIsLoading(false); // Tắt trạng thái loading
        }
    };

    const waitForAudio = async (asyncUrl) => {
        const maxRetries = 10; // Số lần thử tối đa
        const delay = 5000; // Thời gian chờ giữa các lần thử (ms)

        for (let i = 0; i < maxRetries; i++) {
            try {
                const response = await fetch(asyncUrl);
                if (response.ok) {
                    return asyncUrl; // URL sẵn sàng
                }
            } catch {
                console.log('File chưa sẵn sàng, thử lại...');
            }
            await new Promise((resolve) => setTimeout(resolve, delay)); // Chờ trước khi thử lại
        }

        return null; // Thất bại sau khi thử nhiều lần
    };

    const handleStopAudio = () => {
        // Dừng phát âm thanh nếu đang phát
        if (audio) {
            audio.pause(); // Dừng âm thanh
            audio.currentTime = 0; // Đặt lại vị trí âm thanh về đầu
            setIsSpeaking(false);
        }
    };

    return (
        <Box
            sx={{
                display: 'flex',
                justifyContent: isUser ? 'flex-end' : 'flex-start',
                mb: 1,
            }}
        >
            <Box
                sx={{
                    maxWidth: '70%',
                    p: 2,
                    borderRadius: 2,
                    backgroundColor: isUser ? 'primary.main' : 'background.paper',
                    color: isUser ? '#fff' : 'text.primary',
                    display: 'flex',
                    alignItems: 'center',
                }}
            >
                <Typography sx={{ flex: 1 }}>{text}</Typography>
            </Box>
            {/* Icon loa */}
            {!isUser && (
                <Box sx={{ ml: 1, alignSelf: 'center' }}>
                    {isLoading ? (
                        <CircularProgress size={24} color="primary" />
                    ) : (
                        <IconButton onClick={isSpeaking ? handleStopAudio : handlePlayAudio}>
                            {isSpeaking ? <StopIcon /> : <VolumeUpIcon />}
                        </IconButton>
                    )}
                </Box>
            )}
        </Box>
    );
};

export default MessageBubble;
