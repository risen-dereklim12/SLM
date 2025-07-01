import './App.css'
import { Button, TextField } from '@mui/material'
import Box from '@mui/material/Box'
import { useState } from 'react'

function App() {
  const [response, setResponse] = useState("Hello! How can I help you today?")
  const [question, setQuestion] = useState("")

  const handleSend = async () => {
    if (!question.trim()) return
    setResponse("Thinking...")
    try {
      const res = await fetch('http://localhost:5000/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          "question": question
        })
      })
      const data = await res.json()
      setResponse(data.answer)
    } catch (err) {
      setResponse("Sorry, there was an error.")
    }
  }

  return (
    <>
      <h1>PDPA Chatbot</h1>
      <div>
        <TextField
          id="chat"
          label="Chatbot Response"
          variant="outlined"
          multiline
          value={response}
          InputProps={{
            readOnly: true,
          }}
          fullWidth
          minRows={4}
          sx={{ backgroundColor: 'lightgray' }}
        />
      </div>
      <div className="card">
        <Box display="flex" alignItems="center" gap={2}>
          <TextField
            id="outlined-basic"
            label="Ask me about PDPA"
            variant="outlined"
            margin="dense"
            size="small"
            multiline
            rows={4}
            sx={{ height: 'auto', width: '777px' }}
            value={question}
            onChange={e => setQuestion(e.target.value)}
          />
          <Button
            variant="contained"
            size="small"
            color='secondary'
            sx={{ height: '40px' }}
            onClick={handleSend}
          >
            Send
          </Button>
        </Box>
      </div>
    </>
  )
}

export default App
