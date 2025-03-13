import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, Send, ArrowLeft, Share2, Check, Copy, Loader2 } from 'lucide-react';
import { useNavigate } from "react-router";

type Message = {
  id: string;
  content: string;
  isBot: boolean;
  timestamp: Date;
};

const MessageInput = ({ onSend, isTyping }: { onSend: (message: string) => void; isTyping: boolean }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    if (!inputValue.trim()) return;
    onSend(inputValue.trim());
    setInputValue('');
  };

  return (
    <div className="flex items-center gap-2">
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        placeholder="Type a message..."
        className="flex-1 border rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        autoFocus
      />
      <button
        onClick={handleSend}
        disabled={!inputValue.trim() || isTyping}
        className={`p-2 rounded-full transition-colors ${
          inputValue.trim() && !isTyping
            ? 'bg-indigo-600 text-white hover:bg-indigo-700'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        }`}
      >
        <Send size={20} />
      </button>
    </div>
  );
};

function Chatbot() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [showShareMenu, setShowShareMenu] = useState(false);
  const [copySuccess, setCopySuccess] = useState(false);
  const [sessionId, setSessionId] = useState("");
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const navigate = useNavigate();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const words = [
    "apple", "banana", "cherry", "dragon", "elephant", "forest", "guitar", "hammer",
    "island", "jungle", "kitten", "lantern", "mountain", "notebook", "ocean", "penguin",
    "quantum", "river", "sunset", "tiger", "umbrella", "volcano", "whisper", "xylophone",
    "yogurt", "zeppelin"
  ];

  function generateMemorableString() {
    return Array.from({ length: 4 }, () => words[Math.floor(Math.random() * words.length)]).join("-");
  }

  useEffect(() => {
    const start = async () => {
      setIsTyping(true);

      // const session_id = generateMemorableString();
      // setSessionId(session_id);

      const response = await fetch('http://localhost:8000/session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ session_id : sessionId }),
      })
        .then(r => r.json());

      setSessionId(response.session_id)
      // Add initial bot message
      setMessages([{
        id: '1',
        content: response.message,
        isBot: true,
        timestamp: new Date()
      }])
      setIsTyping(false);
    }
    start()
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const get_response = async (message: string) => {
    setIsTyping(true);
    // Simulate API delay
    const response = await fetch('http://localhost:8000/message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        session_id : sessionId,
        message : message
      }),
    }).then(r => r.json());   
    setMessages(prev => [...prev, {
      id: Date.now().toString(),
      content: response.message,
      isBot: true,
      timestamp: new Date()
    }]);
    setIsTyping(false);
  };

  const handleSendMessage = async (message: string) => {
    // Add user message
    const userMessage = {
      id: Date.now().toString(),
      content: message,
      isBot: false,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);

    await get_response(message);
  };

  const handleShare = async () => {
    const conversationText = messages
      .map(msg => `${msg.isBot ? 'Bot' : 'You'}: ${msg.content}`)
      .join('\n');
    
    try {
      await navigator.clipboard.writeText(conversationText);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    } catch (err) {
      console.error('Failed to copy conversation:', err);
    }
  };

  const ChatInterface = () => (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Chat Header */}
      <div className="bg-indigo-600 text-white px-4 py-3 flex items-center justify-between shadow-md">
        <div className="flex items-center">
          <button 
            onClick={() => navigate("/")}
            className="p-1 hover:bg-indigo-700 rounded-full transition-colors"
          >
            <ArrowLeft size={24} />
          </button>
          <div className="ml-3">
            <h1 className="text-lg font-semibold">Chat Session</h1>
            <p className="text-xs text-indigo-200">Online</p>
          </div>
        </div>
        <div className="relative">
          <button
            onClick={() => setShowShareMenu(!showShareMenu)}
            className="p-2 hover:bg-indigo-700 rounded-full transition-colors"
          >
            <Share2 size={20} />
          </button>
          {showShareMenu && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-1 z-10">
              <button
                onClick={handleShare}
                className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100 flex items-center"
              >
                {copySuccess ? (
                  <>
                    <Check size={16} className="mr-2 text-green-500" />
                    <span>Copied!</span>
                  </>
                ) : (
                  <>
                    <Copy size={16} className="mr-2" />
                    <span>Copy conversation</span>
                  </>
                )}
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Chat Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.isBot ? 'justify-start' : 'justify-end'}`}
          >
            <div
              className={`rounded-lg p-3 max-w-[80%] shadow ${
                message.isBot
                  ? 'bg-white text-gray-800'
                  : 'bg-indigo-600 text-white'
              }`}
            >
              <p>{message.content}</p>
              <span className="text-xs opacity-70 mt-1 block">
                {message.timestamp.toLocaleTimeString([], { 
                  hour: '2-digit', 
                  minute: '2-digit' 
                })}
              </span>
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-white rounded-lg p-3 shadow flex items-center">
              <Loader2 className="w-4 h-4 animate-spin mr-2" />
              <span className="text-gray-500 text-sm">Bot is typing...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Message Input */}
      <div className="bg-white border-t p-4">
        <MessageInput onSend={handleSendMessage} isTyping={isTyping} />
      </div>
    </div>
  );

  // return sessionStarted ? <ChatInterface /> : <WelcomeScreen onButtonClick={() => setSessionStarted(true)} />;
  return <ChatInterface />;
}

export default Chatbot;
