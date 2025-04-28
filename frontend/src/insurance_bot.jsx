// src/insurance_bot.jsx
import React, { useState, useEffect, useRef } from 'react';
import './insurance_bot.css';
import { FaMicrophone, FaMicrophoneSlash } from 'react-icons/fa';

function InsuranceBot() {
  const [messages, setMessages] = useState([
    { type: 'bot', text: "👋 Welcome! How can I assist you with insurance or healthcare plans in the United States 🇺🇸 today?" }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [memory, setMemory] = useState([]);
  const [listening, setListening] = useState(false);
  const recognitionRef = useRef(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (!('webkitSpeechRecognition' in window)) {
      alert("Your browser does not support speech recognition.");
      return;
    }
    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInputMessage(transcript);
    };
    recognitionRef.current = recognition;
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const toggleListening = () => {
    if (listening) {
      recognitionRef.current.stop();
      setListening(false);
    } else {
      recognitionRef.current.start();
      setListening(true);
    }
  };

  const sendMessage = async () => {
    if (inputMessage.trim() === '') return;

    const userMessage = inputMessage;
    setMessages(prev => [...prev, { type: 'user', text: userMessage }]);
    setMemory(prev => [...prev, userMessage]);
    setInputMessage('');

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
      });
      const data = await response.json();
      const botMessage = data.response;

      setMessages(prev => [...prev, { type: 'bot', text: botMessage }]);
    } catch (error) {
      console.error("Error:", error);
      setMessages(prev => [...prev, { type: 'bot', text: "⚠️ Sorry, an error occurred." }]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  return (
    <div className="full-container">
      <div className="memory-sidebar">
        <h2>🧠 Memory</h2>
        {memory.map((item, idx) => (
          <div key={idx} className="memory-item">{item}</div>
        ))}
      </div>

      <div className="chat-container">
        <div className="chat-header">🤖 Health Insurance Assistant (United States) 🇺🇸</div>

        <div className="chat-messages">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.type}`}>
              <div dangerouslySetInnerHTML={{ __html: msg.text }} />
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input">
          <input
            type="text"
            placeholder="Type your message..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <button onClick={sendMessage} className="send-button">Send</button>
          <button onClick={toggleListening} className={`mic-button ${listening ? 'listening' : ''}`}>
            {listening ? <FaMicrophoneSlash /> : <FaMicrophone />}
          </button>
        </div>
      </div>
    </div>
  );
}

export default InsuranceBot;
