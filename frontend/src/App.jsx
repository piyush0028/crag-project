import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(false)

  const askAgent = async () => {
    if (!question.trim()) return;
    
    setLoading(true);
    setAnswer('');
    setLogs([]);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
      const response = await axios.post(`${apiUrl}/ask`, {
        question: question
      });
      
      setLogs(response.data.logs);
      setAnswer(response.data.answer);
    } catch (error) {
      console.error("Error:", error);
      setAnswer("The backend encountered an error. Is FastAPI running?");
    }
    
    setLoading(false);
  };

  return (
    <div className="app-wrapper">
      <div className="container">
        <header className="header">
          <h1>CRAG Agent</h1>
          <p>Your intelligent, corrective retrieval assistant</p>
        </header>
        
        <div className="input-container">
          <input 
            type="text" 
            className="input-field"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && askAgent()}
            placeholder="Ask about internships, attendance, or fees..."
            autoFocus
          />
          <button 
            className="submit-btn" 
            onClick={askAgent} 
            disabled={loading || !question.trim()}
          >
            {loading ? 'Thinking...' : 'Ask'}
            {!loading && (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            )}
          </button>
        </div>

        {loading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <span>Analyzing your question...</span>
          </div>
        )}

        {(answer || logs.length > 0) && (
          <div className="results-section">
            {answer && (
              <div className="answer-card">
                <h3>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                  </svg>
                  Final Answer
                </h3>
                <p>{answer}</p>
              </div>
            )}

            {logs.length > 0 && (
              <div className="logs-card">
                <h3>Agent Reasoning Logs</h3>
                <ul className="logs-list">
                  {logs.map((log, index) => (
                    <li key={index} className="log-item">
                      {log}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
