import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, Send, ArrowLeft, Share2, Check, Copy, Loader2 } from 'lucide-react';
import { BrowserRouter, Routes, Route } from "react-router";
import WelcomeScreen from './routes/Welcome.tsx';
import Chatbot from './routes/Chatbot.tsx';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<WelcomeScreen />} />
        <Route path="/chat" element={<Chatbot />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
