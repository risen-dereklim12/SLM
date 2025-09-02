import './App.css'
import { Button, TextField, Paper, Typography } from '@mui/material'
import Box from '@mui/material/Box'
import { useState, useRef, useEffect } from 'react'

const ThinkingDots = () => {
  const [dots, setDots] = useState('');

  useEffect(() => {
    const interval = setInterval(() => {
      setDots(prev => {
        if (prev === '...') return '';
        return prev + '.';
      });
    }, 500);

    return () => clearInterval(interval);
  }, []);

  return (
    <Typography variant="body1" sx={{ textAlign: 'left' }}>
      Thinking{dots}
    </Typography>
  );
};

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! How can I help you today?' }
  ])
  const [question, setQuestion] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!question.trim()) return

    const userMessage = { role: 'user', content: question }
    setMessages(prev => [...prev, userMessage])
    setQuestion("")
    setIsLoading(true)

    try {
      const res = await fetch('http://localhost:5050/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          "question": question
        })
      })
      const data = await res.json()
      const assistantMessage = { role: 'assistant', content: data.answer }
      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      const errorMessage = { role: 'assistant', content: "Sorry, there was an error." }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Box sx={{
      height: '90vh',
      display: 'flex',
      flexDirection: 'column',
      width: '70%',
      margin: '0 auto',
      p: { xs: 1, sm: 2 }
    }}>
      <Typography
        variant={{ xs: 'h6', sm: 'h5', md: 'h4', lg: 'h3' }}
        component="h1"
        sx={{
          mb: { xs: 1, sm: 2 },
          textAlign: 'center',
          fontSize: { xs: '1.25rem', sm: '1.5rem', md: '2rem', lg: '2.5rem' },
          fontWeight: { xs: 500, sm: 400 }
        }}
      >
        Offline Chatbot
      </Typography>

      {/* Chat Messages */}
      <Box sx={{
        flex: 1,
        overflowY: 'auto',
        mb: 2,
        border: '1px solid #ddd',
        borderRadius: 1,
        p: { xs: 0.5, sm: 1 },
        backgroundColor: '#f9f9f9'
      }}>
        {messages.map((message, index) => (
          <Box key={index} sx={{
            display: 'flex',
            justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
            mb: 1
          }}>
            <Paper sx={{
              p: { xs: 1, sm: 2 },
              maxWidth: { xs: '85%', sm: '70%' },
              backgroundColor: message.role === 'user' ? '#1976d2' : '#fff',
              color: message.role === 'user' ? 'white' : 'black'
            }}>
              <Typography variant="body1" sx={{ textAlign: 'left', wordBreak: 'break-word', whiteSpace: 'pre-wrap' }}>
                {message.content}
              </Typography>
            </Paper>
          </Box>
        ))}

        {isLoading && (
          <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 1 }}>
            <Paper sx={{ p: { xs: 1, sm: 2 }, backgroundColor: '#fff' }}>
              <ThinkingDots />
            </Paper>
          </Box>
        )}
        <div ref={messagesEndRef} />
      </Box>

      {/* Input Area */}
      <Box display="flex" alignItems="center" gap={{ xs: 1, sm: 2 }}>
        <TextField
          label="Ask me about PDPA"
          variant="outlined"
          size="small"
          fullWidth
          value={question}
          onChange={e => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              e.preventDefault();
              handleSend();
            }
          }}
          disabled={isLoading}
          sx={{
            '& .MuiInputLabel-root': {
              fontSize: { xs: '0.875rem', sm: '1rem' }
            }
          }}
        />
        <Button
          variant="contained"
          size="small"
          color='primary'
          sx={{
            height: '40px',
            minWidth: { xs: '60px', sm: '80px' },
            fontSize: { xs: '0.75rem', sm: '0.875rem' }
          }}
          onClick={handleSend}
          disabled={isLoading || !question.trim()}
        >
          Send
        </Button>
      </Box>
    </Box>
  )
}

export default App
