import React, { useState, useEffect } from 'react';
import {
    Box, Typography, IconButton, CircularProgress, Dialog, DialogTitle, DialogContent, List, ListItem, Button,
} from '@mui/material';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import StopIcon from '@mui/icons-material/Stop';

const MessageBubble = ({ sender, text, sourceDocuments }) => {
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [audioUrl, setAudioUrl] = useState(null);
    const [audio, setAudio] = useState(null);
    const [openDialog, setOpenDialog] = useState(false);
    const [selectedDocument, setSelectedDocument] = useState(null);
    const [popupContent, setPopupContent] = useState('');
    const [isPopupOpen, setIsPopupOpen] = useState(false);

    const isUser = sender === 'user';

    useEffect(() => {
        if (text && !audioUrl) {
            handleGenerateAudio();
        }
    }, [text]);

    const fetchDocumentContent = async (data) => {
        try {
            const content = data["content"];
            const metadata = data["metadata"];
        
            console.log("content", content);
            console.log("metadata", metadata);
        
            const currentLaw = await import(`../../../utils/law/${metadata.file_id}.json`);
            console.log("currentLaw", currentLaw);
        
            const articleContent = currentLaw.content.find(
                (item) => item.id === metadata.article
            );
        
            // Add the appropriate key based on metadata.file_id
            if (metadata.file_id === "52-2014-QH13") {
                articleContent.lawName = "Luật hôn nhân gia đình";
            } else if (metadata.file_id === "91-2015-QH13") {
                articleContent.lawName = "Luật dân sự";
            }
        
            console.log("articleContent", articleContent);
        
            if (articleContent) {
                const highlightPart = metadata.clause; // e.g., "2c"
        
                // Use a regular expression to capture the number part and the letter part
                const sectionPattern = new RegExp(`(\\d+)([a-zA-Z]+)`, 'i'); // Captures number and letter
        
                const match = highlightPart.match(sectionPattern);
        
                if (match) {
                    const numberPart = match[1]; // e.g., "2"
                    const letterPart = match[2]; // e.g., "c"
        
                    // Go through content and highlight if matches number and letter part
                    articleContent.content = articleContent.content.map((item) => {
                        // Check if the number part matches
                        const numberMatch = item.number === numberPart;
        
                        // Now handle sub_clauses: if letterPart matches any sub_clause letter, highlight it
                        const subClauseMatch = item.sub_clauses.some(subClause => subClause.letter === letterPart);
        
                        if (numberMatch && (letterPart ? subClauseMatch : true)) {
                            return {
                                ...item,
                                highlighted: true, // Mark this part as highlighted
                                sub_clauses: item.sub_clauses.map(subClause => {
                                    // Highlight the sub-clause if its letter matches the letterPart
                                    if (subClause.letter === letterPart) {
                                        return { ...subClause, highlighted: true };
                                    }
                                    return subClause;
                                })
                            };
                        }
                        return item;
                    });
                }
            }
        
            setPopupContent(articleContent || { title: "No content found", content: [] });
            setIsPopupOpen(true);
        } catch (error) {
            console.error("Error fetching law content:", error);
            setPopupContent({ title: "Failed to load content", content: [] });
            setIsPopupOpen(true);
        }
    };
    
    



    const handleOpenDialog = async (document) => {
        setSelectedDocument(document);
        await fetchDocumentContent(document);
        setOpenDialog(true);
    };

    const handleCloseDialog = () => {
        setOpenDialog(false);
        setSelectedDocument(null);
    };

    const handlePlayAudio = async () => {
        if (audioUrl) {
            const newAudio = new Audio(audioUrl);
            newAudio.play().catch((error) => {
                console.error('Không thể phát âm thanh:', error);
                alert('Tệp âm thanh không hợp lệ hoặc không thể phát.');
            });
            setAudio(newAudio);
            setIsSpeaking(true);
            newAudio.onended = () => setIsSpeaking(false);
            return;
        }
        alert('Đang tải âm thanh...');
    };

    const handleGenerateAudio = async () => {
        try {
            setIsLoading(true);
            const requestBody = text;
            const requestHeaders = {
                'api_key': 'ySSVUvXbKu86OlgU8fMg4Ine0sbynFmf',
                'voice': 'leminh',
                'speed': '1',
                'Content-Type': 'application/json',
            };

            const response = await fetch('https://api.fpt.ai/hmi/tts/v5', {
                method: 'POST',
                headers: requestHeaders,
                body: requestBody,
            });

            const result = await response.json();

            if (response.ok && result.error === 0 && result.async) {
                setAudioUrl(result.async);
            } else {
                console.error('API không trả về URL hợp lệ:', result);
                alert('API không trả về URL hợp lệ.');
            }
        } catch (error) {
            console.error('Lỗi khi gọi API FPT.AI:', error);
            alert('Đã xảy ra lỗi khi gọi API FPT.AI.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleStopAudio = () => {
        if (audio) {
            audio.pause();
            audio.currentTime = 0;
            setIsSpeaking(false);
        }
    };

    return (
        <Box sx={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start', mb: 1 }}>
            <Box
                sx={{
                    maxWidth: '70%',
                    p: 2,
                    borderRadius: 2,
                    backgroundColor: isUser ? 'primary.main' : 'background.paper',
                    color: isUser ? '#fff' : 'text.primary',
                }}
            >
                <Typography>{text}</Typography>
                {!isUser && sourceDocuments?.length > 0 && (
                    <Box sx={{ mt: 1 }}>
                        <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                            Tài liệu liên quan:
                        </Typography>
                        <List>
                            {sourceDocuments.map((doc, index) => (
                                <ListItem key={index}>
                                    <Button onClick={() => handleOpenDialog(doc)}>
                                        {doc.metadata?.title || `Tài liệu ${index + 1}`}
                                    </Button>
                                </ListItem>
                            ))}
                        </List>
                    </Box>
                )}
            </Box>
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
            <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="lg" fullWidth>
                <DialogTitle>
                    {popupContent ? (
                        <>
                            <Typography variant="h6" component="div">{popupContent.lawName}</Typography>
                            <Typography variant="h6">{`${popupContent.id}: ${popupContent.title}`}</Typography>
                        </>
                    ) : (
                        "Chi tiết tài liệu"
                    )}
                </DialogTitle>

                <DialogContent>
    {popupContent?.content && popupContent.content.length > 0 ? (
        popupContent.content.map((item, index) => (
            <Box key={index} sx={{ mb: 2 }}>
                <Typography variant="subtitle1">
                    {item.number !== "0" ? `Khoản ${item.number}:` : "Điều khoản chính:"}
                </Typography>
                <Typography
                    sx={{
                        backgroundColor: item.highlighted ? '#60A5FA' : 'transparent', // Highlighted sections
                        fontWeight: item.highlighted ? 'bold' : 'normal', // Bold for highlighted parts
                    }}
                >
                    {item.text}
                </Typography>
                {item.sub_clauses && item.sub_clauses.length > 0 && (
                    <Box sx={{ pl: 2, mt: 1 }}>
                        {item.sub_clauses.map((sub, subIndex) => (
                            <Typography
                                key={subIndex}
                                sx={{
                                    backgroundColor: sub.highlighted ? '#60A5FA' : 'transparent',
                                    fontWeight: sub.highlighted ? 'bold' : 'normal',
                                }}
                            >
                                {sub.letter}. {sub.text}
                            </Typography>
                        ))}
                    </Box>
                )}
            </Box>
        ))
    ) : (
        <Typography>Không có nội dung để hiển thị.</Typography>
    )}
</DialogContent>

            </Dialog>



        </Box>
    );
};

export default MessageBubble;
