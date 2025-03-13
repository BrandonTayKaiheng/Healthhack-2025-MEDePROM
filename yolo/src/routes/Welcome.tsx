import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, Send, ArrowLeft, Share2, Check, Copy, Loader2 } from 'lucide-react';
import { useNavigate } from "react-router";


function WelcomeScreen() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-500 to-indigo-700 flex flex-col items-center justify-center p-6">
      <div className="bg-white/10 p-6 rounded-full mb-8">
        <MessageCircle size={64} className="text-white" />
      </div>
      <h1 className="text-3xl font-bold text-white mb-4 text-center">
        Welcome to MEDePROM
      </h1>
      <p className="text-indigo-100 mb-8 text-center">
        Start a new conversation and connect instantly
      </p>
      <button
        onClick={() => navigate("/chat")}
        className="bg-white text-indigo-600 px-8 py-3 rounded-full font-semibold shadow-lg hover:bg-indigo-50 transition-colors transform hover:scale-105 duration-200"
      >
        Start Session
      </button>
    </div>
  )
}



export default WelcomeScreen;
